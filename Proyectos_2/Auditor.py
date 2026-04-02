# This is the beginning of the Auditor project
from core import executor
from frontend import CLI
import sys
import subprocess
from pathlib import Path

def main ():
    CLI.cli()
    if executor.confirm == True:
        print("\n Confirmamos \n")

main()