import math
import psutil


class Disk:
    # Existing methods...

    def bytes_to_readable(self, size_in_bytes):
        # Define the suffixes for each size unit
        suffixes = ["B", "KB", "MB", "GB", "TB", "PB"]

        # Calculate the logarithm of the size to determine the suffix index
        i = int(math.floor(math.log(size_in_bytes, 1024))) if size_in_bytes else 0

        # Convert the size to the appropriate unit and round up
        readable_size = math.ceil(size_in_bytes / math.pow(1024, i))

        # Format and return the readable size with the appropriate suffix
        return f"{readable_size} {suffixes[i]}"

    def get_disks(self):
        disk_lists = psutil.disk_partitions()

        # Converting to list of dictionaries
        disk_dicts = [
            {
                "device": part.device[:1],
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "opts": part.opts,
                "disk_usage": {
                    "total": self.bytes_to_readable(d_info.total),
                    "used": self.bytes_to_readable(d_info.used),
                    "free": self.bytes_to_readable(d_info.free),
                    "percent": d_info.percent,
                },
            }
            for part in disk_lists
            for d_info in [psutil.disk_usage(part.mountpoint)]
        ]
        return disk_dicts
