import subprocess # Para poder recabar los inputs y errores
import tarfile # Para poder manera .tar
from pathlib import Path # Para poder darle una ruta especifica
import os # Para poder ejecutar codigo en terminal

# Funcion para compilar el .tar
class ToolCompiler:
    # Se definen los paths del .tar 
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.src_dir = base_dir / "tools" / "tools_src"
        self.bin_dir = base_dir / "tools" / "tools_bin"

    # Se confirma si ya esta compilado con aterioridad
    def compile_nmap(self):
        bin_path = self.bin_dir / "nmap" / "nmap"
        if bin_path.exists():
            return  # ya compilado
        
        # Se busca el .tar, se descomprime y se compila (.make)
        src_tar = self.src_dir / "nmap" / "nmap-7.98.tar.bz2"
        build_dir = self.src_dir / "nmap" / "build"

        build_dir.mkdir(parents = True, exist_ok = True)

        with tarfile.open(src_tar, "r:bz2") as tar:
            tar.extractall(build_dir)

        extracted = next(build_dir.iterdir())

        os.chdir(extracted)

        # No se usa zenmap (UI de nmap)
        subprocess.run([
            "./configure",
            f"--prefix={self.bin_dir / 'nmap'}",
            "--without-zenmap",
            "--with-libpcap=included",
            "--with-liblua=included",
        ], check=True)

        subprocess.run(["make", "-j4"], check=True)
        subprocess.run(["make", "install"], check=True)
