import os
import sys

if __name__ == "__main__":p
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CA.settings")  # 这里的 "CA.settings" 是你项目中的 settings.py 文件路径
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        )
    execute_from_command_line(sys.argv)
