import re
import random

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None
    
def random_id() -> int:
    output = ""
    for i in range(10):
        output += str(random.randint(0, 9))
    return int(output)