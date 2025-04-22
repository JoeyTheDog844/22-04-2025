import winreg
from tkinter import messagebox

REG_PATH = r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"
REG_NAME = "AutoShareWks"

def get_admin_share_status():
    """
    Returns True if default admin shares are disabled (AutoShareWks = 0),
    False if enabled (1 or key missing).
    """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_READ) as reg:
            value, _ = winreg.QueryValueEx(reg, REG_NAME)
            return value == 0
    except FileNotFoundError:
        # Key or value doesn't exist: shares are enabled by default
        return False
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read registry:\n{e}")
        return False

def set_admin_share_status(disable=True):
    """
    Sets AutoShareWks value to disable or enable default admin shares.
    Returns a string message indicating success or error.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_SET_VALUE) as reg:
            winreg.SetValueEx(reg, REG_NAME, 0, winreg.REG_DWORD, 0 if disable else 1)
        return "Default Admin Shares successfully " + ("disabled." if disable else "enabled.")
    except PermissionError:
        return "❌ Permission Denied: Please run the app as Administrator."
    except Exception as e:
        return f"❌ Error updating registry:\n{e}"
