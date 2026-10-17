// rig.cpp — headless Pinocchio auto-rigger CLI.
//
// Uses the Pinocchio library (LGPL, Baran & Popovic 2007) to embed a
// skeleton template into a static character mesh and compute skinning
// weights, with NO GUI / NO manual steps.
//
// Usage:
//   rig <mesh.obj|ply|off|stl> <out_prefix> [--skel human|horse|quad|centaur] [--scale s]
//
// Outputs:
//   <out_prefix>_skeleton.json  joints: name, parent, pos (original mesh units)
//   <out_prefix>_weights.bin     int32 nverts, int32 njoints, float32[nverts*njoints] row-major
//
// Notes:
// * Pinocchio internally normalizes the mesh into a unit cube. We replicate
//   that deterministic transform (Mesh::scale / Mesh::toAdd) to map the
//   fitted joints back into the ORIGINAL mesh coordinate space, so the
//   model is NEVER rescaled.
// * If the mesh has multiple connected components, the largest one is kept
//   (Pinocchio requires a single connected component).
// * Vertex order is preserved by prepareMesh, so weight row i == vertex i
//   of the input mesh.

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <vector>
#include <ctime>

#include "pinocchioApi.h"
#include "skeleton.h"
#include "attachment.h"

using namespace std;

static const char *HUMAN_JOINTS[18] = {
    "shoulders","back","hips","head",
    "lthigh","lknee","lankle","lfoot",
    "rthigh","rknee","rankle","rfoot",
    "lshoulder","lelbow","lhand",
    "rshoulder","relbow","rhand"
};

Mesh largestComponent(const Mesh &m)
{
    int nv = (int)m.vertices.size();
    vector<vector<int> > adj(nv);
    for (size_t e = 0; e + 2 < m.edges.size(); e += 3) {
        int a = m.edges[e].vertex, b = m.edges[e+1].vertex, c = m.edges[e+2].vertex;
        adj[a].push_back(b); adj[a].push_back(c);
        adj[b].push_back(a); adj[b].push_back(c);
        adj[c].push_back(a); adj[c].push_back(b);
    }
    vector<int> comp(nv, -1);
    int ncomp = 0, best = -1;
    size_t bestSize = 0;
    vector<int> sz;
    for (int i = 0; i < nv; ++i) {
        if (comp[i] >= 0) continue;
        queue<int> q; q.push(i); comp[i] = ncomp;
        size_t s = 0;
        while (!q.empty()) { int v = q.front(); q.pop(); ++s;
            for (size_t k = 0; k < adj[v].size(); ++k) {
                int w = adj[v][k];
                if (comp[w] < 0) { comp[w] = ncomp; q.push(w); }
            }
        }
        sz.push_back((int)s);
        if (s > bestSize) { bestSize = s; best = ncomp; }
        ++ncomp;
    }
    if (ncomp <= 1) return m;
    cerr << "[rig] mesh has " << ncomp << " components; keeping largest ("
         << bestSize << "/" << nv << " verts)" << endl;

    vector<int> remap(nv, -1);
    Mesh out;
    for (int i = 0; i < nv; ++i)
        if (comp[i] == best) { remap[i] = (int)out.vertices.size(); out.vertices.push_back(m.vertices[i]); }
    for (size_t e = 0; e + 2 < m.edges.size(); e += 3) {
        int a = m.edges[e].vertex, b = m.edges[e+1].vertex, c = m.edges[e+2].vertex;
        if (comp[a] == best && comp[b] == best && comp[c] == best) {
            MeshEdge ea, eb, ec;
            ea.vertex = remap[a]; eb.vertex = remap[b]; ec.vertex = remap[c];
            out.edges.push_back(ea); out.edges.push_back(eb); out.edges.push_back(ec);
        }
    }
    out.scale = 1.;
    return out;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        cerr << "Usage: rig <mesh.obj|ply|off|stl> <out_prefix> [--skel human|horse|quad|centaur] [--scale s]" << endl;
        return 2;
    }
    string meshFile = argv[1], prefix = argv[2];
    string skelName = "human";
    double skelScale = 1.0;
    for (int i = 3; i < argc; ++i) {
        if (!strcmp(argv[i], "--skel") && i + 1 < argc) skelName = argv[++i];
        else if (!strcmp(argv[i], "--scale") && i + 1 < argc) skelScale = atof(argv[++i]);
    }

    clock_t t0 = clock();
    Mesh m(meshFile);
    if (m.vertices.empty()) { cerr << "[rig] ERROR: failed to load mesh " << meshFile << endl; return 1; }
    cerr << "[rig] loaded " << m.vertices.size() << " verts, "
         << m.edges.size() / 3 << " tris from " << meshFile << endl;

    Mesh work = largestComponent(m);

    Skeleton skel;
    if (skelName == "human") skel = HumanSkeleton();
    else if (skelName == "horse") skel = HorseSkeleton();
    else if (skelName == "quad") skel = QuadSkeleton();
    else if (skelName == "centaur") skel = CentaurSkeleton();
    else { cerr << "[rig] ERROR: unknown skeleton " << skelName << endl; return 1; }
    if (skelScale != 1.0) skel.scale(skelScale);

    // Deterministic unit-cube transform, so we can invert it afterwards.
    // autorig() runs the exact same prepareMesh internally.
    Mesh pm = prepareMesh(work);
    if (pm.vertices.empty()) { cerr << "[rig] ERROR: prepareMesh failed (not a single connected component?)" << endl; return 1; }

    PinocchioOutput po = autorig(skel, work);
    if (po.embedding.empty() || !po.attachment) {
        cerr << "[rig] ERROR: autorig failed (embedding empty)" << endl;
        return 1;
    }

    int nj = (int)po.embedding.size();
    int nv = (int)work.vertices.size();
    const vector<int> &parents = skel.fPrev();

    // Map joints back to original mesh coordinates: orig = (prep - toAdd)/scale
    vector<Vector3> jointsOrig(nj);
    for (int j = 0; j < nj; ++j)
        jointsOrig[j] = (po.embedding[j] - pm.toAdd) / pm.scale;

    // ---- write skeleton.json ----
    {
        ofstream js((prefix + "_skeleton.json").c_str());
        js << "{\n  \"mesh\": \"" << meshFile << "\",\n";
        js << "  \"skeleton\": \"" << skelName << "\",\n";
        js << "  \"nverts\": " << nv << ",\n";
        js << "  \"units\": \"original mesh units (model NOT rescaled)\",\n";
        js << "  \"joints\": [\n";
        for (int j = 0; j < nj; ++j) {
            string name = (skelName == "human" && j < 18) ? HUMAN_JOINTS[j]
                          : ("j" + to_string(j));
            int p = (j < (int)parents.size()) ? parents[j] : -1;
            js << "    {\"name\": \"" << name << "\", \"parent\": " << p
               << ", \"pos\": [" << jointsOrig[j][0] << ", "
               << jointsOrig[j][1] << ", " << jointsOrig[j][2] << "]}"
               << (j + 1 < nj ? "," : "") << "\n";
        }
        js << "  ]\n}\n";
    }

    // ---- write weights.bin ----
    {
        ofstream wf((prefix + "_weights.bin").c_str(), ios::binary);
        int32_t h[2] = { (int32_t)nv, (int32_t)nj };
        wf.write((char*)h, sizeof(h));
        vector<float> row(nv * nj);
        double wsum = 0; int wcount = 0;
        for (int i = 0; i < nv; ++i) {
            Vector<double, -1> w = po.attachment->getWeights(i);
            for (int j = 0; j < nj; ++j) {
                float v = (j < (int)w.size()) ? (float)w[j] : 0.f;
                row[i * nj + j] = v;
                wsum += v;
            }
            ++wcount;
        }
        wf.write((char*)row.data(), row.size() * sizeof(float));
        cerr << "[rig] mean weight/vertex (should be ~1.0): " << (wsum / wcount) << endl;
    }

    delete po.attachment;
    double secs = double(clock() - t0) / CLOCKS_PER_SEC;
    cerr << "[rig] DONE in " << secs << "s: " << nj << " joints, " << nv
         << " verts -> " << prefix << "_skeleton.json / " << prefix << "_weights.bin" << endl;
    return 0;
}
