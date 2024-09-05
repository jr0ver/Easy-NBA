from bs4 import BeautifulSoup, Tag
import requests
import re

def get_br_page(player: str) -> str:
    if not player:
        return
    br_template = "https://www.basketball-reference.com"
    
    last_initial = player.split()

    if len(last_initial) > 1:
        last_initial = last_initial[1][0].lower()
    else:
        return

    new_url = br_template + "/players/" + last_initial + "/"
    response = requests.get(new_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # for edge cases like 'DeMar DeRozan'
    regex = re.compile(player, re.IGNORECASE)
    player_link = soup.find("a", string=regex)
    p_name = player_link.text
    if player_link:
        br_page = br_template + player_link["href"] + "/"
        response = requests.get(br_page)
        soup = BeautifulSoup(response.content, "html.parser")
        return [soup, p_name]
    print("Player not found")
    return

def get_br_img(soup: BeautifulSoup) -> str:
    temp_img = soup.find_all("img")
    if temp_img:
        return temp_img[1]["src"]
    return ""

def get_br_info(soup: BeautifulSoup) -> str:
    """Given a a BeautifulSoup object, locates the player name and 
    returns it
    """
    player_info = soup.find('div', id='info')
    if player_info:
        return player_info
    return

def get_position(tag: Tag) -> str:
    #given an HTML tag, returns the position
    position_tag = tag.find('strong', string=lambda text: text and 'Position' in text)
    position=""
    if position_tag:
        position = position_tag.parent
        position = position.text
        start = position.find(":")
        end = position.find("▪")
        position = position.strip()[start:end]
        position = position.split('\n')[1].strip()

        #formatting jargon
        p_dict={"Point Guard":"PG",
        "Shooting Guard":"SG",
        "Small Forward":"SF",
        "Power Forward": "PF",
        "Center": "C"}

        pos = []
        for item in p_dict.keys():
            if item in position:
                pos.append(p_dict[item])
        position = '/'.join(pos)
    return position