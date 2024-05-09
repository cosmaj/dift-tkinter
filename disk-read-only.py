import time
import winreg
import sys
import os
import ctypes
import subprocess
import wmi


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_disk_number(disk_letter):
    try:
        w = wmi.WMI()
        disk_list = w.query(f"SELECT * FROM Win32_DiskDrive")
        print(disk_list)
        if len(disk_list) > 0:
            return int(disk_list[0].Index)
        else:
            raise Exception(f"No disk found with letter '{disk_letter}'")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def set_disk_read_only(disk_num):
    try:
        # Create diskpart command
        commands = [f"select disk {disk_num}", "attributes disk set readonly"]

        with open("temp_script.txt", "w") as file:
            for command in commands:
                file.write(command + "\n")

        # Open the registry key for the specified disk
        # registry_key = winreg.OpenKey(
        #     winreg.HKEY_LOCAL_MACHINE,
        #     f"SYSTEM\\CurrentControlSet\\Control\\StorageDevicePolicies",
        #     0,
        #     winreg.KEY_ALL_ACCESS,
        # )

        subprocess.check_output(
            "diskpart /s " + os.path.abspath("temp_script.txt"),
            shell=True,
            universal_newlines=True,
        )
        # Set the 'NtfsDisableLastAccessUpdate' value to 1 (read-only)
        # winreg.SetValueEx(registry_key, f"{disk_letter}:", 0, winreg.REG_DWORD, 1)

        print(f"Disk '{disk_letter}' set to read-only.")

        # Wait for 1 minutes
        time.sleep(60)

        commands = [f"select disk {disk_num}", "attributes disk clear readonly"]

        with open("temp_script.txt", "w") as file:
            for command in commands:
                file.write(command + "\n")

        subprocess.check_output(
            "diskpart /s " + os.path.abspath("temp_script.txt"),
            shell=True,
            universal_newlines=True,
        )

        # Set the 'NtfsDisableLastAccessUpdate' value back to 0 (read-write)
        # winreg.SetValueEx(registry_key, f"{disk_letter}", 0, winreg.REG_DWORD, 0)

        print(f"Disk '{disk_letter}' set back to read-write.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )

    disk_letter = input("Enter the disk letter (e.g., C, D, E): ").upper()
    disk_number = get_disk_number(disk_letter)
    if disk_number is not None:
        set_disk_read_only(disk_number)
