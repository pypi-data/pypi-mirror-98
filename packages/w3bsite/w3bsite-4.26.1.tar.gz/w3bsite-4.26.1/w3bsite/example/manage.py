#!/usr/bin/env python3
import os,sys
from dev0s import *
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__defaults__.django.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
if __name__ == '__main__':
    os.chdir(gfp.base(__file__, back=1))
    main()