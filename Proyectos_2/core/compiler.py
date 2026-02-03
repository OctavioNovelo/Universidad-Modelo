# core/compiler.py
import subprocess
import tarfile
from pathlib import Path
import os

class ToolCompiler:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.src_dir = base_dir / "tools" / "tools_src"
        self.bin_dir = base_dir / "tools" / "tools_bin"

    def compile_nmap(self):
        bin_path = self.bin_dir / "nmap" / "nmap"
        if bin_path.exists():
            return  # ya compilado

        src_tar = self.src_dir / "nmap" / "nmap-7.98.tar.bz2"
        build_dir = self.src_dir / "nmap" / "build"

        build_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(src_tar, "r:bz2") as tar:
            tar.extractall(build_dir)

        extracted = next(build_dir.iterdir())

        os.chdir(extracted)

        subprocess.run([
            "./configure",
            f"--prefix={self.bin_dir / 'nmap'}",
            "--without-zenmap",
            "--with-libpcap=included",
            "--with-liblua=included",
        ], check=True)

        subprocess.run(["make", "-j4"], check=True)
        subprocess.run(["make", "install"], check=True)
