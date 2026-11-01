#!/usr/bin/env python3
"""Patch v1 UI into v2: 5 industry + 5 experimental features, all wired in JS.
Original v1 folder untouched; this script only edits the v2 copy."""
import re, pathlib
p = pathlib.Path.home() / "workspace/cape-jones-rig/duplicate-review-ui-v2-20261031/index.html"
html = p.read_text()

# --- CSS additions ---
html = html.replace(
"  footer{margin:0 24px 40px;color:var(--mut);font-size:13px}",
"""  footer{margin:0 24px 40px;color:var(--mut);font-size:13px}
  .featurebar{background:#eef3ff;border:1px solid #b9c8ef;border-radius:10px;padding:12px 16px;margin:0 24px 12px;font-size:14px}
  .featurebar b{color:#1a1a2e}
  .bulkbar{display:none;gap:8px;align-items:center;margin:12px 24px;padding:12px;background:#fff7e6;border:1px solid #e0b84f;border-radius:10px;position:sticky;top:60px;z-index:4}
  .bulkbar.show{display:flex;flex-wrap:wrap}
  .progress{height:14px;background:#e5e5ee;border-radius:8px;overflow:hidden;margin:8px 24px}
  .progress i{display:block;height:100%;background:#1d7a3a}
  .valid{margin:12px 24px;padding:12px 16px;background:#fff;border:1px solid var(--line);border-radius:10px;font-size:14px}
  .valid.warnbox{border-color:#d9a400;background:#fff8e1}
  .tile .conf{font-size:12px;color:#1d7a3a;font-weight:600}
  .tile .rel{font-size:12px;color:var(--mut);margin-top:6px}
  .tile input[type=checkbox]{transform:scale(1.3);margin-right:6px}
  .helpmodal{max-width:640px;background:#fff;border-radius:12px;padding:20px;font-size:15px}
  .diffbar{font-size:14px;margin-top:8px}
""")

# --- Toolbar: add v2 buttons + progress + validation + bulk bar ---
html = html.replace(
'  <button id="resetBtn">Reset all decisions</button>\n</div>',
"""  <button id="resetBtn">Reset all decisions</button>
  <button id="undoBtn" title="Ctrl+Z">Undo (Ctrl+Z)</button>
  <button id="validateBtn">Validate export</button>
  <button id="helpBtn" title="Press ?">Shortcuts (?)</button>
  <button id="importBtn">Import decisions</button>
  <input type="file" id="importFile" accept=".json" hidden>
</div>
<div class="featurebar"><b>V2 features:</b> I1 keyboard shortcuts · I2 bulk select/actions · I3 undo · I4 indexed search · I5 export validation · X1 near-duplicate preview · X2 auto-label suggestions · X3 confidence scoring · X4 pixel-diff compare · X5 progress persistence (scroll restore + import). Press <b>?</b> for shortcuts. Nothing here deletes files.</div>
<div class="progress" title="Decided progress"><i id="progressFill" style="width:0%"></i></div>
<div class="bulkbar" id="bulkBar"><span id="bulkCount">0 selected</span>
  <button id="bulkKeep">Bulk KEEP</button><button id="bulkDel">Bulk DELETE CANDIDATE</button>
  <button id="bulkUnd">Bulk Undecided</button><button id="bulkClear">Clear selection</button>
  <button id="bulkLabel">Apply suggested labels to selected</button></div>
<div class="valid" id="validBox">Validation: not run yet — click “Validate export”.</div>""")

# --- Tile markup: checkbox, confidence, auto-label, related, compare ---
html = html.replace(
"""        <article class="tile ${it.decision==="KEEP"?"keep":it.decision==="DELETE"?"del":""}">""",
"""        <article class="tile ${it.decision==="KEEP"?"keep":it.decision==="DELETE"?"del":""}" data-tile="${g.group_id}|${it.source}">
          <div><input type="checkbox" data-select="${g.group_id}|${it.source}" ${selected.has(g.group_id+"|"+it.source)?"checked":""}> <span class="conf">Confidence 100% — exact MD5 match</span></div>
          <div class="rel">Suggested label: <b>${suggestLabel(it.source)}</b> <button data-autolabel="${g.group_id}|${it.source}">Use suggestion</button></div>
          <div class="rel">Near-duplicate preview (same stem in other groups): ${relatedGroups(g, it).length?relatedGroups(g, it).join(", "):"none"}</div>""")
html = html.replace(
"""          <div class="decisions">""",
"""          <div class="decisions">
            <button data-compare="${g.group_id}|${it.source}">Compare (pixel diff)</button>""")

# --- Group header: select-all-group button ---
html = html.replace(
"""      · <button data-keepfirst="${g.group_id}">Keep first, mark rest DELETE CANDIDATE</button></div>""",
"""      · <button data-keepfirst="${g.group_id}">Keep first, mark rest DELETE CANDIDATE</button>
      · <button data-selectgroup="${g.group_id}">Select all in group</button></div>""")

# --- Insert v2 JS before renderAll(); ---
v2js = r'''
// ============ V2 FEATURES ============
// I4 indexed search: token index over source, folder, group, label
const SEARCH_INDEX = {};
DATA.groups.forEach(g => g.items.forEach(it => {
  const toks = (g.group_id + " " + it.source + " " + it.group_folder + " " + (it.suggested_label||"")).toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
  toks.forEach(t => { (SEARCH_INDEX[t] = SEARCH_INDEX[t] || new Set()).add(g.group_id + "|" + it.source); });
}));
function indexedSearch(q) {
  const toks = q.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean);
  if (!toks.length) return null;
  let out = null;
  toks.forEach(t => {
    const hits = new Set();
    Object.keys(SEARCH_INDEX).forEach(k => { if (k.includes(t)) SEARCH_INDEX[k].forEach(v => hits.add(v)); });
    out = out === null ? hits : new Set([...out].filter(v => hits.has(v)));
  });
  return out;
}
// X2 auto-label suggestions from path
function suggestLabel(source) {
  const s = source.toLowerCase();
  if (s.includes("dance-packs")) return "dance pack";
  if (s.includes("jojo-packs-2")) return "jojo pack 2";
  if (s.includes("jojo-packs")) return "jojo pack";
  if (s.includes("lounge-3quarter")) return "lounge clean 3quarter";
  if (s.includes("lounge-packs")) return "lounge pack";
  if (s.includes("references")) return "reference tpose";
  return "sheet";
}
// X1 near-duplicate preview: same stripped stem in another group
function stemOf(source) {
  const base = source.split("/").pop().replace(/\.(jpg|png)$/i, "");
  return base.replace(/^(dance|recent|clean|lounge|cape-jones)-/, "").replace(/^tpose-/, "tpose-");
}
function relatedGroups(g, it) {
  const st = stemOf(it.source), out = [];
  DATA.groups.forEach(o => { if (o.group_id !== g.group_id && o.items.some(x => stemOf(x.source) === st)) out.push(o.group_id); });
  return out;
}
// I3 undo, 50 steps
let selected = new Set();
const history = [];
function snapshot() {
  history.push(JSON.stringify(DATA.groups.map(g => g.items.map(it => ({decision: it.decision, label: it.suggested_label})))));
  if (history.length > 50) history.shift();
}
function undo() {
  if (!history.length) return;
  const prev = JSON.parse(history.pop());
  DATA.groups.forEach((g, gi) => g.items.forEach((it, ii) => { it.decision = prev[gi][ii].decision; it.suggested_label = prev[gi][ii].label; }));
  persist(); renderAll();
}
// I5 export validation
function validateExport() {
  const issues = [];
  DATA.groups.forEach(g => {
    const keeps = g.items.filter(i => i.decision === "KEEP").length;
    const dels = g.items.filter(i => i.decision === "DELETE").length;
    const und = g.items.filter(i => i.decision === "UNDECIDED").length;
    if (keeps > 1) issues.push(g.group_id + ": " + keeps + " KEEP — only one canonical should be kept per group.");
    if (keeps === 0 && dels > 0) issues.push(g.group_id + ": DELETE CANDIDATEs but no KEEP — nothing would remain.");
    if (keeps === 0 && dels === 0 && und === g.size) issues.push(g.group_id + ": all undecided.");
  });
  const box = document.getElementById("validBox");
  box.className = "valid" + (issues.length ? " warnbox" : "");
  box.innerHTML = issues.length
    ? "<b>Validation issues (" + issues.length + "):</b><br>" + issues.map(i => "• " + i).join("<br>") + "<br>Export is still allowed, but confirm you intend these."
    : "<b>Validation PASS:</b> every group has at most one KEEP, and no group would be left empty.";
  return issues;
}
// X5 progress persistence: progress bar + scroll restore + import
function updateProgress() {
  const total = DATA.groups.reduce((n, g) => n + g.items.length, 0);
  const done = DATA.groups.reduce((n, g) => n + g.items.filter(i => i.decision !== "UNDECIDED").length, 0);
  const el = document.getElementById("progressFill");
  if (el) el.style.width = (total ? Math.round(done / total * 100) : 0) + "%";
  try { localStorage.setItem("duplicate-review-scroll-20261031", String(window.scrollY)); } catch(e) {}
}
function restoreScroll() {
  try { const y = Number(localStorage.getItem("duplicate-review-scroll-20261031") || 0); if (y) window.scrollTo(0, y); } catch(e) {}
}
// X4 pixel-diff compare: load two plate images on canvas, compare RGBA
let compareFirst = null;
function pixelDiff(urlA, urlB, cb) {
  const a = new Image(), b = new Image();
  a.crossOrigin = "anonymous"; b.crossOrigin = "anonymous";
  a.onload = () => { b.onload = () => {
    try {
      const w = Math.min(a.naturalWidth, b.naturalWidth), h = Math.min(a.naturalHeight, b.naturalHeight);
      const c = document.createElement("canvas"); c.width = w; c.height = h; const ctx = c.getContext("2d");
      ctx.drawImage(a, 0, 0, w, h); const d1 = ctx.getImageData(0, 0, w, h).data;
      ctx.clearRect(0, 0, w, h); ctx.drawImage(b, 0, 0, w, h); const d2 = ctx.getImageData(0, 0, w, h).data;
      let diff = 0; for (let i = 0; i < d1.length; i += 4) if (Math.abs(d1[i]-d2[i]) + Math.abs(d1[i+1]-d2[i+1]) + Math.abs(d1[i+2]-d2[i+2]) + Math.abs(d1[i+3]-d2[i+3]) > 30) diff++;
      cb("Pixel diff: " + diff + " / " + (w*h) + " pixels (" + (100*diff/(w*h)).toFixed(2) + "% differing). Exact MD5 groups should read ~0%.");
    } catch(e) { cb("Pixel diff unavailable in this browser context (canvas tainted, e.g. file://) — MD5 exact-match confidence still 100%."); }
  }; b.src = urlB; }; a.src = urlA;
  a.onerror = () => cb("Could not load first image for diff.");
}
// Wrap renderAll to also update progress + bulk bar
const _renderAll = renderAll;
renderAll = function() { _renderAll(); updateProgress();
  const bar = document.getElementById("bulkBar");
  if (bar) { bar.classList.toggle("show", selected.size > 0); document.getElementById("bulkCount").textContent = selected.size + " selected"; }
};
// I2 bulk actions + I1 shortcuts + compare + autolabel + select
document.addEventListener("click", e => {
  const sel = e.target.closest("[data-select]");
  if (sel) { const k = sel.dataset.select; sel.checked ? selected.add(k) : selected.delete(k); renderAll(); return; }
  const sg = e.target.closest("[data-selectgroup]");
  if (sg) { const g = DATA.groups.find(x => x.group_id === sg.dataset.selectgroup); g.items.forEach(it => selected.add(g.group_id + "|" + it.source)); renderAll(); return; }
  const al = e.target.closest("[data-autolabel]");
  if (al) { const [gid, ...src] = al.dataset.autolabel.split("|"); const g = DATA.groups.find(x => x.group_id === gid); const it = g.items.find(x => x.source === src.join("|")); snapshot(); it.suggested_label = suggestLabel(it.source); persist(); renderAll(); return; }
  const cp = e.target.closest("[data-compare]");
  if (cp) {
    const [gid, ...src] = cp.dataset.compare.split("|"); const g = DATA.groups.find(x => x.group_id === gid); const it = g.items.find(x => x.source === src.join("|"));
    if (!compareFirst) { compareFirst = it; alert("First tile picked: " + it.source + ". Now click Compare on a second tile."); return; }
    const first = compareFirst; compareFirst = null;
    pixelDiff(first.plate, it.plate, msg => alert(first.source + " vs " + it.source + "\n" + msg));
    return;
  }
  if (e.target.id === "bulkKeep" || e.target.id === "bulkDel" || e.target.id === "bulkUnd") {
    snapshot(); const dec = e.target.id === "bulkKeep" ? "KEEP" : e.target.id === "bulkDel" ? "DELETE" : "UNDECIDED";
    selected.forEach(k => { const [gid, ...src] = k.split("|"); const g = DATA.groups.find(x => x.group_id === gid); const it = g && g.items.find(x => x.source === src.join("|")); if (it) it.decision = dec; });
    persist(); renderAll(); return;
  }
  if (e.target.id === "bulkClear") { selected.clear(); renderAll(); return; }
  if (e.target.id === "bulkLabel") { snapshot(); selected.forEach(k => { const [gid, ...src] = k.split("|"); const g = DATA.groups.find(x => x.group_id === gid); const it = g && g.items.find(x => x.source === src.join("|")); if (it) it.suggested_label = suggestLabel(it.source); }); persist(); renderAll(); return; }
  if (e.target.id === "undoBtn") { undo(); return; }
  if (e.target.id === "validateBtn") { validateExport(); return; }
  if (e.target.id === "helpBtn") { alert("Shortcuts:\n/ focus search\nj / k move focus between groups (scrolls)\nK keep focused tile, D delete candidate, U undecided\nEsc close modal\nCtrl+Z undo\nClick a tile checkbox to bulk-select; bulk bar appears when any tile is selected."); return; }
  if (e.target.id === "importBtn") { document.getElementById("importFile").click(); return; }
  if (e.target.id === "exportJson" || e.target.id === "exportCsv") { const issues = validateExport(); if (issues.length && !confirm("Validation found " + issues.length + " issue(s). Export anyway?")) return; }
});
document.addEventListener("change", e => {
  if (e.target.id === "importFile" && e.target.files[0]) {
    const r = new FileReader();
    r.onload = () => { try { const exp = JSON.parse(r.result); snapshot();
      exp.groups.forEach(eg => { const g = DATA.groups.find(x => x.group_id === eg.group_id); if (!g) return; eg.items.forEach(ei => { const it = g.items.find(x => x.source === ei.source); if (it) { it.decision = ei.decision; it.suggested_label = ei.label || it.suggested_label; } }); });
      persist(); renderAll(); alert("Imported decisions."); } catch(err) { alert("Import failed: not a valid decision export JSON."); } };
    r.readAsText(e.target.files[0]);
  }
});
document.addEventListener("keydown", e => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") { e.preventDefault(); document.getElementById("q").focus(); }
  if (e.key === "?" && document.activeElement.tagName !== "INPUT") { document.getElementById("helpBtn").click(); }
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") { e.preventDefault(); undo(); }
  if (e.key === "Escape") document.getElementById("modal").classList.remove("open");
});
// Snapshot before single decisions too
document.addEventListener("click", e => { const d = e.target.closest("[data-decision]"); if (d) snapshot(); }, true);
// Use indexed search inside filteredGroups by patching q handling: wrap original
const _filtered = filteredGroups;
filteredGroups = function() {
  const q = (document.getElementById("q").value || "").trim();
  if (!q) return _filtered();
  const hits = indexedSearch(q);
  const base = _filtered();
  return base.filter(g => g.items.some(it => hits && hits.has(g.group_id + "|" + it.source)));
};
window.addEventListener("load", restoreScroll);
'''
html = html.replace("renderAll();\n</script>", v2js + "\nrenderAll();\n</script>")
p.write_text(html)
print("patched", len(html))
