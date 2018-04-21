from datetime import datetime

cleaned_lines = []
with open('data/raw_data', 'r') as f:
    for line in f:
        if '\t' in line:
            if 'T00' not in line:
                cleaned_lines.append(line.replace('\n', ''))
            continue
        line = " ".join(line.split())
        if len(line.split(' ')) == 4:
            if 'T00' not in line:
                entries = [x.strip() for x in line.rsplit(' ', 2)]
                cleaned_lines.append('\t'.join(entries))
        elif len(line.split(' ')) == 6:
            if 'T00' not in line:
                entries = [x.strip() for x in line.rsplit(' ', 4)]
                entries[3:5] = [' '.join(entries[3:5])]
                cleaned_lines.append('\t'.join(entries))
        else:
            break

count = 0
known_events = []
sensors, activities = [], []
for line in cleaned_lines:
    if len(line.split('\t')) == 4:
        events = line.split('\t')
        event = events[3]
        event = " ".join(event.split())
        if event == "ON" or event == "OFF":
            continue
        
        sensors.append(events[1])
        activities.append(event)
        events[3] = event
        FMT = "%Y-%m-%d %H:%M:%S.%f"
        timestamp = datetime.strptime(events[0],FMT)
        events.pop(0)
        events = [str(timestamp.weekday())] + events
        known_events.append(events)

count = 1
sensors_dict = {}

for sensor in list(set(sensors)):
    sensors_dict[sensor] = count
    count += 1

count = 1
activities_dict = {}

for activity in list(set(activities)):
    activities_dict[activity] = count
    count += 1

readings_dict = {"OFF": 0, "ON": 1, "CLOSE": 2, "OPEN": 3}

for i in range(2,len(known_events)):
    known_events[i] += [known_events[i-1][1], known_events[i-1][2], known_events[i-2][1], known_events[i-2][2]]

with open('data/cleaned_data.csv', 'w') as f:
    f.write("weekday,sensor,reading,activity,sensor-1,reading-1,sensor-2,reading-2\n")
    for line in known_events:
        try:
            line[1] = str(sensors_dict[line[1]])
            line[2] = str(readings_dict[line[2]])
            line[3] = str(activities_dict[line[3]])
            line[4] = str(sensors_dict[line[4]])
            line[5] = str(readings_dict[line[5]])
            line[6] = str(sensors_dict[line[6]])
            line[7] = str(readings_dict[line[7]])
            f.write(','.join(line)+'\n')
        except:
            pass

lines = []
with open('data/cleaned_data.csv', 'r') as f:
    for line in f:
        lines.append(line.strip())

split = int(0.8*len(lines))

with open('data/training.csv', 'w') as f:
    f.write("weekday,sensor,reading,activity,sensor-1,reading-1,sensor-2,reading-2\n")
    for i in range(1, split):
        f.write(lines[i]+'\n')

with open('data/testing.csv', 'w') as f:
    f.write("weekday,sensor,reading,activity,sensor-1,reading-1,sensor-2,reading-2\n")
    for i in range(split, len(lines)):
        f.write(lines[i]+'\n')