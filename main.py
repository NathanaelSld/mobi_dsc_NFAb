from time import time 
from enum import Enum
"""
USB Drive Inserted → File Copied → Device Ejected
Process events of a computer to secure it and monitor possible intrusion of exfiltration of data
"""

class Event_type(Enum):
    DEVICE_in=1
    DEVICE_out=2
    FILE_copy=3
    FILE_write=4


class Event:
    id: str
    timestamp: float #seconds from epoch
    event_type: Event_type
    def __init__(self, id: str = "", timestamp: float = 0.0, event_type: Event_type = None):
        self.id = id
        self.timestamp = timestamp
        self.event_type = event_type


class Query:
    patterns : list[lambda e: bool]
    time_window: float #seconds
    def __init__(self, patterns: list[lambda e: bool], time_window: float):
        self.patterns = patterns
        self.time_window = time_window


def initialize_event_stream(file_path: str="events.log") -> list[Event]:
    stream = []
    with open(file_path, 'r') as f:
        for line in f:
            id, timestamp, event_type_str = line.strip().split(',')
            event = Event(
                id=id,
                timestamp=float(timestamp),
                event_type=Event_type[event_type_str]
            )
            stream.append(event)
    return stream

def process_event(stream: list[Event], query : Query):
    event_index = 0
    match_buffer  = [] 
    for pattern in query.patterns:
        if pattern(stream[event_index]):
            match_buffer.append(stream[event_index])
            event_index += 1
        else:
            stream = stream[1:]
            return False, [], stream
    if (match_buffer[-1].timestamp - match_buffer[0].timestamp)< query.time_window:
        return True, match_buffer , stream
    else:
        stream = stream[1:]
        return False, [], stream


def main():
    stream= initialize_event_stream("events.log")
    query_check_intrusive_behavior = Query(
        patterns=[
            lambda e: e.event_type == Event_type.DEVICE_in,
            lambda e: e.event_type == Event_type.FILE_copy,
            lambda e: e.event_type == Event_type.DEVICE_out,
        ],
        time_window=300.0 #5 minutes
    )

    matches = []

    while (len(stream)!=0):
        print(f"Processing stream with {len(stream)} events")
        match,events, stream = process_event(stream, query_check_intrusive_behavior )
        if match:
            matches.append(events)
        # Remove processed events from stream
        stream = stream[len(events):]
    print(f"Total matches found: {len(matches)}")
    print("Matches detail:")
    for match in matches:
        for event in match:
            print(f"Event ID: {event.id}, Type: {event.event_type}, Timestamp: {event.timestamp}")
        print("-----")




if __name__=="__main__":
    main()