#!/usr/bin/env python
"""Ponto de entrada para comandos administrativos do Django."""
import os
import sys

def main() -> None:
    """Executa tarefas administrativas."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
