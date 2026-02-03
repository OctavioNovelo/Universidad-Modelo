# tools/nmap.py
class NmapCommands:

    COMMANDS = {
        1: lambda target: ["-F", target],
        2: lambda target: ["-sV", target],
        3: lambda target: ["-O", target],
        4: lambda target: ["-A", "-p-", target],
    }

    @classmethod
    def build(cls, option: int, target: str):
        if option not in cls.COMMANDS:
            raise ValueError("Opción inválida")

        return cls.COMMANDS[option](target)
