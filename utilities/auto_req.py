import random
from time import sleep
import requests

file = "all_players_list.txt"

with open(file, "r") as file:
    names = file.readlines()

names = [name.rstrip("\n") for name in names]
# print(names)

url = "http://127.0.0.1:5000/"

# send POST requests
for name in names:
    delay_time = random.uniform(5, 7)
    sleep(delay_time)

    response = requests.post(url, data={"player": name})
    
    if response.status_code == 200:
        print(f"Successfully sent: {name}")
    else:
        print(f"Failed to send: {name}, Status Code: {response.status_code}")