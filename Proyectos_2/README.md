This project is a **modular network auditing frontend written in Python**.
Its goal is to allow users to run well-known open-source security tools **without directly using commands or a terminal**, by interacting
with a structured interface.

The software acts as an **orchestrator**:
- It collects user input through a UI
- Validates and sanitizes that input
- Executes security tools internally
- Captures and processes their output

In later stages, the output will be analyzed using AI (DeepSeek) to provide
focused and actionable insights for network auditing.

## Current Scope
Implemented / In progress:
- Project structure
- CLI-based user interface
- Input validation layer
- Tool execution layer (starting with Nmap)


I am using a structure that make the software a full modular architecture. 

    config:
    This folder contains the main configuration for global variables.
    The config folder contains the following files:
        __init__.py
        This file contain main configuration (at the moment this file is in blank).

    core:
    Core logic that **protects the system from invalid or unsafe execution**. Basically is our protect layer for inputs, flags ando UI abuse.
    The core folder contains the following files:
        __init__.py
        This file contain declares the first variables used by validator.py.

        input_validator.py
        This file validates the input structure and validate if the command can run or if is a dangerous operation.

    This layer does not execute tools directly, only verify if the input is correct. 

    frontend:
    This contains the UI stuff, at the moment we use the terminal as a UI, but whit time we're going to add a user friendly UI.
    The frontend folder contains the following files:
        __init__.py
        This file contain declares the firsts variables used by command_line.py.

        command_line.py
        Collects user input and display the result.

    The frontend communicates only with 'core' and 'tools'.
    This layer does not execute tools directly.

    tools:
    This folder contains the tools from that we going to use.
    The tools folder contains the followings files:
        __init__.py
        This file contain declares the firsts variables used by the diferents tools.

    utils:
    This folder contains extra functions like a logger that allows to register, events, errors, executions, etc.
    The utils folder contains the followings files:
        __init__.py
        This file contain declares the firsts variables used by logger.py and validation.py.

        logger.py
        This file allows to tracks executions, errors, and audit history.

        validation.py
        This file check the security.

## Execution Flow

1. User selects the option in the UI.
2. The input is sent to 'core' for validation.
3. Validated parameters are passed to the tool handler.
4. The tool is executed internally.
5. Output is capture and returned.
6. (Future) AI analyzes the output and provides insights.
7. Results are displayed to the user.

## Ethical Notice

No one follow me in github but i think is important to declare that This software must only be used on systems you own and ystems you have explicit permission to audit.

Unauthorized network scanning is illegal.