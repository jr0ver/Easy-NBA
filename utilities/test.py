from bs4 import BeautifulSoup, Tag
import requests
import re

url = "https://www.basketball-reference.com/players/j/jamesle01.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

player_info = soup.find('div', id='info')

position_tag = player_info.find('strong', string=lambda text: text and 'Position' in text)

position=""
if position_tag:
    position = position_tag.parent
    position = position.text
start = position.find(":")
end = position.find("▪")
position = position.strip()[start:end]
position = position.split('\n')[1].strip()

p_dict={"Point Guard":"SF",
        "Shooting Guard":"SF",
        "Small Forward":"SF",
        "Power Forward": "PF",
        "Center": "C"}


position_list = [pos.strip() for part in position.split(',') for pos in part.split('and')]

abbreviated_positions = [p_dict.get(pos, pos) for pos in position_list]
abbreviated_positions.remove('')
print(abbreviated_positions)
position = '/'.join(abbreviated_positions)
print(position)

