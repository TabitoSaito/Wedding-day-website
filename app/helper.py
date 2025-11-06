from app.constants import MIN_SPACING
import datetime

class RangeScaler:
    def __init__(self, lower_range, upper_range, values: list):
        self.values = values
        self.lower = lower_range
        self.upper = upper_range
        self.max = max(values)
        self.min = min(values)

    def get_scaled_list(self) -> list:
        scaled_list = [self.lower + (v - self.min) * (self.upper - self.lower) / (self.max - self.min) for v in
                       self.values]
        return scaled_list

    def scale_item(self, item):
        return self.lower + (item - self.min) * (self.upper - self.lower) / (self.max - self.min)


def add_rel_position(data: dict) -> list:
    cur_year = datetime.datetime.now().year
    events: list = data["events"]
    events.append(
        {
            "id": len(events),
            "event": "Heute",
            "date": cur_year
        }
    )
    events.sort(key=lambda x: x["date"])

    scaler = RangeScaler(MIN_SPACING, 100 - MIN_SPACING, [event["date"] for event in events])

    cid = 1
    for event in events:
        event["rel_pos"] = scaler.scale_item(event["date"])
        event["id"] = cid
        cid += 1

    for i in range(len(events) - 1):
        event1 = events[i]
        event2 = events[i + 1]

        pos1 = event1["rel_pos"]
        pos2 = event2["rel_pos"]

        if pos2 - pos1 < MIN_SPACING and pos2 < 100 - MIN_SPACING * 2:
            event2["rel_pos"] = pos2 + MIN_SPACING - (pos2 - pos1)

    return events