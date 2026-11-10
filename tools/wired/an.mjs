import {NodeIO} from '@gltf-transform/core';
import {ALL_EXTENSIONS} from '@gltf-transform/extensions';
import {MeshoptDecoder} from 'meshoptimizer';
import fs from 'fs';
await MeshoptDecoder.ready;
const io=new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({'meshopt.decoder':MeshoptDecoder});
function inv(m){ // 4x4 col-major inverse translation approx: use full inverse
 const a=m,o=new Array(16);const [a00,a01,a02,a03,a10,a11,a12,a13,a20,a21,a22,a23,a30,a31,a32,a33]=a;
 const b00=a00*a11-a01*a10,b01=a00*a12-a02*a10,b02=a00*a13-a03*a10,b03=a01*a12-a02*a11,b04=a01*a13-a03*a11,b05=a02*a13-a03*a12,b06=a20*a31-a21*a30,b07=a20*a32-a22*a30,b08=a20*a33-a23*a30,b09=a21*a32-a22*a31,b10=a21*a33-a23*a31,b11=a22*a33-a23*a32;
 let d=b00*b11-b01*b10+b02*b09+b03*b08-b04*b07+b05*b06; d=1/d;
 o[12]=(a31*b05-a32*b04+a33*b03)*d*-1*-1; // placeholder
 // translation of inverse: only need columns 12..14
 o[12]=(-a10*b11+a11*b10-a12*b09)*d*0; return null;}
function inv4t(m){const a=[[m[0],m[4],m[8],m[12]],[m[1],m[5],m[9],m[13]],[m[2],m[6],m[10],m[14]],[0,0,0,1]];
const R=[[a[0][0],a[0][1],a[0][2]],[a[1][0],a[1][1],a[1][2]],[a[2][0],a[2][1],a[2][2]]];const t=[a[0][3],a[1][3],a[2][3]];
const d=R[0][0]*(R[1][1]*R[2][2]-R[1][2]*R[2][1])-R[0][1]*(R[1][0]*R[2][2]-R[1][2]*R[2][0])+R[0][2]*(R[1][0]*R[2][1]-R[1][1]*R[2][0]);
const I=[[(R[1][1]*R[2][2]-R[1][2]*R[2][1])/d,(R[0][2]*R[2][1]-R[0][1]*R[2][2])/d,(R[0][1]*R[1][2]-R[0][2]*R[1][1])/d],[(R[1][2]*R[2][0]-R[1][0]*R[2][2])/d,(R[0][0]*R[2][2]-R[0][2]*R[2][0])/d,(R[0][2]*R[1][0]-R[0][0]*R[1][2])/d],[(R[1][0]*R[2][1]-R[1][1]*R[2][0])/d,(R[0][1]*R[2][0]-R[0][0]*R[2][1])/d,(R[0][0]*R[1][1]-R[0][1]*R[1][0])/d]];
return [0,1,2].map(i=>-(I[i][0]*t[0]+I[i][1]*t[1]+I[i][2]*t[2]));}
const f=process.argv[2];
const doc=await io.read(f);const root=doc.getRoot();
let verts=0,unw=0,bad=0,far=0,sk=0,hasTex=0,mats=0;let mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9];
const skins=root.listSkins();let bones=0;const used=new Set();
const nodes=root.listNodes();
for(const n of nodes){const m=n.getMesh();if(!m)continue;const s=n.getSkin();
 const wm=n.getWorldMatrix();
 for(const p of m.listPrimitives()){const P=p.getAttribute('POSITION');if(!P)continue;const c=P.getCount();verts+=c;
  const mat=p.getMaterial(); if(mat){mats++; if(mat.getBaseColorTexture())hasTex++;}
  const pos=[0,0,0];const W=p.getAttribute('WEIGHTS_0'),J=p.getAttribute('JOINTS_0');
  let jp=null;
  if(s&&W&&J){sk++;const js=s.listJoints();bones=Math.max(bones,js.length);
   const ibm=s.getInverseBindMatrices();jp=js.map((j,ji)=>{if(!ibm)return j.getWorldTranslation();const m=[];ibm.getElement(ji,m);return inv4t(m);});
  }
  const w=[0,0,0,0],jj=[0,0,0,0];
  for(let i=0;i<c;i++){P.getElement(i,pos);
   const useMesh=!!(s&&s.getInverseBindMatrices());const wm2=useMesh?[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]:wm;const x=wm2[0]*pos[0]+wm2[4]*pos[1]+wm2[8]*pos[2]+wm2[12],y=wm2[1]*pos[0]+wm2[5]*pos[1]+wm2[9]*pos[2]+wm2[13],z=wm2[2]*pos[0]+wm2[6]*pos[1]+wm2[10]*pos[2]+wm2[14];
   const q=[x,y,z];for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],q[k]);mx[k]=Math.max(mx[k],q[k]);}
   if(jp){W.getElement(i,w);J.getElement(i,jj);const sum=w[0]+w[1]+w[2]+w[3];if(sum<1e-4)unw++;else if(Math.abs(sum-1)>0.05)bad++;
    let bi=0;for(let k=1;k<4;k++)if(w[k]>w[bi])bi=k;const b=jj[bi];used.add(b);const t=jp[b];
    if(t){const d=Math.hypot(t[0]-x,t[1]-y,t[2]-z);pos.d=d; if(!globalThis.H) globalThis.H=[]; globalThis.H.push(d);}
   }}
 }}
const h=Math.max(mx[1]-mn[1],0);let farpct=0;
if(globalThis.H&&h>0){const th=0.35*h;let k=0;for(const d of globalThis.H)if(d>th)k++;farpct=+(100*k/globalThis.H.length).toFixed(2);}
const anims=root.listAnimations().map(a=>a.getName());
console.log(JSON.stringify({verts,skinnedPrims:sk,bones,bonesUsed:used.size,unweighted:unw,badNorm:bad,farWeightPct:farpct,height:+h.toFixed(3),width:+(mx[0]-mn[0]).toFixed(3),depth:+(mx[2]-mn[2]).toFixed(3),images:root.listTextures().length,matsWithTex:hasTex,mats,anims}));
