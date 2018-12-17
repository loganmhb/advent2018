import re
from collections import defaultdict

data = open('day4_input_sorted', 'r').readlines()

stats = defaultdict(lambda: {'total_slept': 0, 'slept_by_minute': defaultdict(int)})
current_elf = None
slept_at = None
guard_regex = re.compile(r'.*Guard \#(\d+) begins shift')
sleep_regex = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (falls asleep|wakes up)')

for line in data:
    guard_match = guard_regex.match(line)
    if guard_match:
        current_elf = guard_match.group(1)
        continue
    else:
        status_match = sleep_regex.match(line)
        (y, m, d, h, minute, change) = status_match.groups()
        if change == 'falls asleep':
            slept_at = minute
        else:
            for t in range(int(slept_at), int(minute)):
                stats[current_elf]['total_slept'] += 1
                stats[current_elf]['slept_by_minute'][t] += 1

sleepiest_elf = max(stats.items(), key=(lambda item: item[1]['total_slept']))
sleepiest_minute = max(sleepiest_elf[1]['slept_by_minute'].items(), key=(lambda entry: entry[1]))[0]
sleepiest_elf_id = sleepiest_elf[0]

print(f'Elf {sleepiest_elf_id} is sleepiest at minute {sleepiest_minute}')
answer = int(sleepiest_minute) * int(sleepiest_elf_id)
print(f'id * minute: {answer}')

def sleepiest_minute(guard_entry):
    return (guard_entry[0], max(guard_entry[1]['slept_by_minute'].items(), key=(lambda item: item[1])))

consistently_sleepy_elf = max(stats.items(), key=(lambda item: sleepiest_minute(item)[1][1]))
print(f'Consistently sleepiest elf: {sleepiest_minute(consistently_sleepy_elf)}')
