from main import *
import random
"""
Improvements:
- More coherent data generation with realistic timestamps and event sequences
- Exemple : a device should be inserted before file copy events, and ejected afterwards
- Add more attributes to events for richer data (e.g., user id, file size
- Implement different distributions for event types based on realistic usage patterns
- Etc ... Etc...
"""

def data_generation() -> list[Event]:
    """ 
    Generate a data set to mock the behavior of a stream of events of a computer system.
    """
    events = []
    for i in range(1000):
        """Randomly generate events"""
        event = Event()
        event.id = f"event_{i}"
        event.timestamp = i * 10.0  # every 10 seconds
        rand_event_type = random.choices(
            population=[Event_type.DEVICE_in, Event_type.DEVICE_out, Event_type.FILE_copy, Event_type.FILE_write],
            weights=[0.25, 0.25, 0.25, 0.25],
            k=1
        )[0]
        event.event_type = rand_event_type
        events.append(event)
        print(f"Generated event: {event.id}, type: {event.event_type}, timestamp: {event.timestamp}")
    return events



def write_to_log_file(file_path: str, events: list[Event]):
    with open(file_path, 'w') as f:
        for event in events:
            f.write(f"{event.id},{event.timestamp},{event.event_type.name}\n")

if __name__ == "__main__":
    events = data_generation()
    write_to_log_file("events.log", events)