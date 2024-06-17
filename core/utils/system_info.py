from datetime import datetime
import tzlocal
from datetime import datetime, timezone
import psutil


def get_system_timezone():
    local_timezone = tzlocal.get_localzone()
    return local_timezone


def get_utc_time():
    utc_time = datetime.now(timezone.utc)
    return utc_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")


def get_all_mac_addresses():
    mac_addresses = []
    interfaces = psutil.net_if_addrs()
    for interface_name, addresses in interfaces.items():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                mac_addresses.append((interface_name, address.address))
    return mac_addresses


if __name__ == "__main__":
    system_timezone = get_system_timezone()
    utc_time = get_utc_time()
    mac_addresses = get_all_mac_addresses()

    print(f"System Timezone: {system_timezone}")
    print(f"UTC Time: {utc_time}")

    for interface, mac in mac_addresses:
        print(f"[{interface}: {mac}]", end=" ")
