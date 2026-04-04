# This is the beginning of the Auditor project
import core.executor
import frontend.CLI
import sys
import subprocess


def main ():
    subprocess.run(["clear"])
    frontend.CLI.cli()

main()