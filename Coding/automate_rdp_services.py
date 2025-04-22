import subprocess
import time

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def disable_services():
    """Disables selected services."""
    services = [
        "bthserv",  # Bluetooth Support Service
        "lfsvc",  # Geolocation Service
        "TermService",  # Remote Desktop Services
        "RemoteAccess",  # Routing and Remote Access
        "WFDSConMgrSvc",  # Wi-Fi Direct Services
        "xbgm",  # Xbox Game Monitoring
        "XblAuthManager",  # Xbox Live Auth Manager
        "XboxNetApiSvc",  # Xbox Live Networking Service
        "XblGameSave",
        "LanmanServer"  # Default Share Status
    ]
    
    disabled_services = []
    failed_services = []
    
    for service in services:
        result = subprocess.run(["sc", "config", service, "start=", "disabled"], capture_output=True, text=True, startupinfo=startupinfo)
        if "SUCCESS" in result.stdout:
            disabled_services.append(service)
        else:
            failed_services.append(service)
    
    return disabled_services, failed_services

def enable_services():
    """Enables and starts selected services."""
    services = [
        "bthserv", "lfsvc", "TermService", "RemoteAccess", "WFDSConMgrSvc", "xbgm", "XblAuthManager", "XboxNetApiSvc", "XblGameSave", "LanmanServer"
    ]

    enabled_services = []
    failed_services = []

    for service in services:
        try:
            # Step 1: Set to manual (or auto)
            config_result = subprocess.run(
                ["sc", "config", service, "start=", "auto"],
                capture_output=True,
                text=True,
                timeout=10,
                startupinfo=startupinfo
            )

            if "SUCCESS" not in config_result.stdout:
                failed_services.append(f"{service} (config failed)")
                continue

            # Step 2: Start service
            subprocess.run(
                ["sc", "start", service],
                capture_output=True,
                text=True,
                timeout=10,
                startupinfo=startupinfo
            )

            # Step 3: Wait and verify status
            for _ in range(5):
                time.sleep(1)
                status_check = subprocess.run(["sc", "query", service], capture_output=True, text=True, startupinfo=startupinfo)
                if "RUNNING" in status_check.stdout:
                    enabled_services.append(service)
                    break
            else:
                failed_services.append(f"{service} (didn't confirm running)")

        except Exception as e:
            failed_services.append(f"{service} (error: {e})")

    return enabled_services, failed_services

def check_services_status():
    services = {
        "bthserv": "Bluetooth Support Service",
        "lfsvc": "Geolocation Service",
        "TermService": "Remote Desktop Services",
        "RemoteAccess": "Routing and Remote Access",
        "WFDSConMgrSvc": "Wi-Fi Direct Services",
        "xbgm": "Xbox Game Monitoring",
        "XblAuthManager": "Xbox Live Auth Manager",
        "XboxNetApiSvc": "Xbox Live Networking Service",
        "XblGameSave": "Xbox Live Game Save",
        "LanmanServer": "Default Share Status"
    }

    statuses = {}

    for service, service_name in services.items():
        # First check config for DISABLED
        config_result = subprocess.run(["sc", "qc", service], capture_output=True, text=True, startupinfo=startupinfo)
        if "DISABLED" in config_result.stdout:
            statuses[service_name] = "Disabled"
            continue

        # Then check actual running/stopped state
        result = subprocess.run(["sc", "query", service], capture_output=True, text=True, startupinfo=startupinfo)
        
        if "RUNNING" in result.stdout:
            statuses[service_name] = "Running"
        elif "STOPPED" in result.stdout:
            statuses[service_name] = "Stopped"
        else:
            statuses[service_name] = "Unknown"

    return statuses

