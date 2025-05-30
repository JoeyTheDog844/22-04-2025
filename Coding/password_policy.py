import subprocess

def get_current_policy():
    """ ✅ Retrieve the current password policy as a dictionary """
    try:
        result = subprocess.run(["net", "accounts"], capture_output=True, text=True)
        lines = result.stdout.strip().splitlines()
        policy = {}

        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                policy[key.strip()] = value.strip()
        return policy

    except Exception as e:
        return {"Error": f"Error retrieving policy: {e}"}

def set_password_policy():
    """ ✅ Modify Windows Password Policy """
    try:
        subprocess.run(["net", "accounts", "/MAXPWAGE:45"], capture_output=True, text=True)
        subprocess.run(["net", "accounts", "/MINPWAGE:0"], capture_output=True, text=True)
        subprocess.run(["net", "accounts", "/MINPWLEN:10"], capture_output=True, text=True)

        subprocess.run(["reg", "add", "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Netlogon\\Parameters", 
                        "/v", "PasswordComplexity", "/t", "REG_DWORD", "/d", "1", "/f"], capture_output=True, text=True)

        return "Password policy successfully updated."

    except Exception as e:
        return f"Error updating password policy: {e}"
