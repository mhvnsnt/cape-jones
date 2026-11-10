import json, sys, urllib.request, urllib.error
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args): raise RuntimeError("redirect refused")
def get(path):
    url="https://api.github.com"+path
    req=urllib.request.Request(url)
    req.add_header("Accept","application/vnd.github+json"); req.add_header("X-GitHub-Api-Version","2022-11-28"); req.add_header("User-Agent","Muse-GitHub-Api")
    add_surrogate_to_request(req,"custom.github-api",allowed_hosts=["api.github.com"])
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=60) as r:
            b=r.read(); return json.loads(b.decode()) if b else {}
    except urllib.error.HTTPError as e:
        print(json.dumps({"error":e.code,"path":path,"body":e.read().decode(errors="replace")[:500]})); sys.exit(1)
if __name__=="__main__":
    print(json.dumps(get(sys.argv[1]),indent=1)[:12000])
