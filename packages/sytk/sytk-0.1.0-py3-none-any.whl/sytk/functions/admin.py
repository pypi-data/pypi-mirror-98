import ctypes
import sys


def _is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_as_admin():
    if _is_admin():
        return
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
