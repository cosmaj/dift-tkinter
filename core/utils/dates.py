import datetime


class Utils:
    @staticmethod
    def get_current_time(self):

        now = datetime.datetime.now()
        day_number, day_suffix = now.day, (
            "th"
            if 10 <= now.day <= 20
            else {1: "st", 2: "nd", 3: "rd"}.get(now.day % 10, "th")
        )
        curret_time = now.strftime(f"%A {day_number}{day_suffix} %B %Y %H:%M:%S")
        return curret_time
