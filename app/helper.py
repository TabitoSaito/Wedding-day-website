from app.constants import MIN_SPACING
import datetime

class RangeScaler:
    def __init__(self, lower_range: int, upper_range: int, values: list[int]):
        """scale list of numbers to be in a specified range. lower and upper bound included

        Args:
            lower_range (int): lower bound of range
            upper_range (int): upper bound of range
            values (list[int]): numbers to scale
        """
        self.values = values
        self.lower = lower_range
        self.upper = upper_range
        self.max = max(values)
        self.min = min(values)

    def get_scaled_list(self) -> list[float]:
        """scale all numbers in value list

        Returns:
            list[float]: list of scaled numbers
        """
        scaled_list = [self.lower + (v - self.min) * (self.upper - self.lower) / (self.max - self.min) for v in
                       self.values]
        return scaled_list

    def scale_item(self, number: int) -> float:
        """scale single number. Has to be inside the specified range

        Args:
            item (int): number to scale

        Returns:
            float: scaled number
        """
        return self.lower + (number - self.min) * (self.upper - self.lower) / (self.max - self.min)


def add_rel_position(data: dict) -> list[dict]:
    """map relative position to corresponding event by event date.

    Args:
        data (dict): loaded 'events.json' converted to python dictionary

    Returns:
        list[dict]: sorted list containing event dictionaries modified with relative position
    """
    cur_year = datetime.datetime.now().year
    events: list = data["events"]
    events.append(
        {
            "id": len(events),
            "event": "Heute",
            "date": cur_year
        }
    )
    events.sort(key=lambda x: x["date"]) # sort events by date

    scaler = RangeScaler(MIN_SPACING, 100 - MIN_SPACING, [event["date"] for event in events])

    # add relative position and update id
    cid = 1
    for event in events:
        event["rel_pos"] = scaler.scale_item(event["date"])
        event["id"] = cid
        cid += 1

    # enforce minimum spacing between events
    for i in range(len(events) - 1):
        event1 = events[i]
        event2 = events[i + 1]

        pos1 = event1["rel_pos"]
        pos2 = event2["rel_pos"]

        if pos2 - pos1 < MIN_SPACING and pos2 < 100 - MIN_SPACING * 2:
            event2["rel_pos"] = pos2 + MIN_SPACING - (pos2 - pos1)

    return events