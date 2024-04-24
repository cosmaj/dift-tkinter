import psutil


class Disk:
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
                    "total": d_info.total,
                    "used": d_info.used,
                    "free": d_info.free,
                    "percent": d_info.percent,
                },
            }
            for part in disk_lists
            for d_info in [psutil.disk_usage(part.mountpoint)]
        ]
        return disk_dicts
