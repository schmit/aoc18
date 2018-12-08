from utils import read_input
import attr
from datetime import datetime
import collections
import enum

class Action(enum.Enum):
    SHIFT = 1
    SLEEP = 2
    WAKE = 3

@attr.s()
class Event:
    ts = attr.ib()
    action = attr.ib()
    guard_id = attr.ib()


def parse_ts(ts_string):
    return datetime.strptime(ts_string.replace('[','').replace(']',''),
                             '%Y-%m-%d %H:%M')


def sort_lines(lines):
    return sorted(lines, key=lambda line: parse_ts(line.split(']')[0]))


def parse_events(lines):
    guard_id = None
    events = []
    for line in lines:
        if 'Guard' in line:
            event = parse_guard_event(line)
            guard_id = event.guard_id
        else:
            event = parse_action_event(line, guard_id)
        events.append(event)

    return events
            

def parse_guard_event(line):
    ts_str, id_str = line.split('#')
    ts = parse_ts(ts_str.split(']')[0])
    guard_id = int(id_str.split(' ')[0])
    return Event(ts, Action.SHIFT, guard_id)


def parse_action_event(line, guard_id):
    if 'wake' in line:
        action = Action.WAKE
    else:
        action = Action.SLEEP
    ts_str = line.split(']')[0]
    return Event(parse_ts(ts_str), action, guard_id)


def get_guard_sleeping_hours(events):
    guard_sleeping_hours = collections.defaultdict(collections.Counter)
    for begin, end in zip(events, events[1:]):
        if begin.guard_id is None:
            # guard unknown
            continue
        
        if begin.action == Action.SLEEP:
            # guard has fallen asleep; find out how long
            if end.action == Action.SHIFT:
                guard_sleeping_hours[begin.guard_id].update(
                    range(begin.ts.minute, 60))
            else:
                guard_sleeping_hours[begin.guard_id].update(
                    range(begin.ts.minute, end.ts.minute))

    return guard_sleeping_hours

def total_sleeping_minutes(sleep_counter):
    return sum(sleep_counter.values())

def most_asleep_minute(sleep_counter):
    minute, times = sleep_counter.most_common(1)[0]
    return minute

def get_sleepiest_guard(guard_sleeping_hours):
    return max(guard_sleeping_hours,
               key=lambda guard: total_sleeping_minutes(guard_sleeping_hours[guard]))

def get_events():
    sorted_lines = sort_lines(read_input(4))
    all_events = parse_events(sorted_lines)
    return all_events
    

"""
Find the guard G who is most asleep.
Find M, the minute that guard G is most asleep.
Return G * M
"""
all_events = get_events()
guard_sleeping_hours = get_guard_sleeping_hours(all_events)
sleepiest_guard = get_sleepiest_guard(guard_sleeping_hours)
sleep_counter = guard_sleeping_hours[sleepiest_guard]
solution_part_1 = sleepiest_guard * most_asleep_minute(sleep_counter)

"""
Find the guard G who is most frequently asleep on the same minute M,
return G * M
"""
guard_most_asleep_minute = [(guard, counter.most_common(1)[0])
                            for guard, counter in guard_sleeping_hours.items()]

guard, (minute, sleep_count) = max(guard_most_asleep_minute,
                                      key=lambda x: x[1][1])

solution_part_2 = guard * minute
