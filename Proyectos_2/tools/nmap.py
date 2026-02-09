class NmapCommands:

# Comandos de nmap.
    commands = {
        1: lambda target: ["-F", target],
        2: lambda target: ["-sV", target],
        3: lambda target: ["-O", target],
        4: lambda target: ["-A", "-p-", target],
    }

# Se verifica si la opcion se encuentra en commands
    @classmethod
    def build(cls, option: int, target: str):
        if option not in cls.commands:
            raise ValueError("Opción inválida")

        return cls.commands[option](target)
