import json
import re


def save_cookies(data,filename='local_storage_data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file) 


def load_cookies(filename='local_storage_data.json'):
    with open(filename, 'r') as file:
        local_storage_data = json.load(file)
    
    return local_storage_data

def is_smaller_than_9_hours(time_string):
    pattern = r'Total Work Time\n(\d{2}:\d{2}) hr\(s\)'
    match = re.search(pattern, time_string)

    if match:
        work_time = match.group(1)
        hours, minutes = map(int, work_time.split(':'))
        total_minutes = hours * 60 + minutes
        
        return total_minutes < 540
    else:
        print("Unable To Extract Current Work Time")

