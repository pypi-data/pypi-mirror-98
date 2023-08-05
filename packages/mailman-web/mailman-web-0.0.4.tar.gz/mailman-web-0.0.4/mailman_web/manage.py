#!/usr/bin/env python
import os
import sys
from pathlib import Path

def setup():
    """Setup environment for Mailman web."""
    if os.getenv('DJANGO_SETTINGS_MODULE') is not None:
        return

    MAILMAN_WEB_CONFIG = os.getenv('MAILMAN_WEB_CONFIG', '/etc/mailman3/settings.py')

    if not os.path.exists(MAILMAN_WEB_CONFIG):
        print('Mailman web configuration file at {} does not exist'.format(
              MAILMAN_WEB_CONFIG), file=sys.stderr)
        print('Modify "MAILMAN_WEB_CONFIG" environment variable to point at '
              'settings.py', file=sys.stderr)
        sys.exit(1)

    config_path = Path(MAILMAN_WEB_CONFIG).resolve()
    sys.path.append(str(config_path.parent))

    os.environ['DJANGO_SETTINGS_MODULE'] = config_path.stem

def main():
    setup()

    os.environ['DJANGO_IS_MANAGEMENT_COMMAND'] = '1'
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
