from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
import requests

URL = "https://www.basketball-reference.com/players/b/butleji01.html"


response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')
table_html = soup.find('table', {'id': 'per_game_stats'})
if table_html:
    # Use pandas to read the table
    tables = pd.read_html(StringIO(str(table_html)))
    print(tables)
else:
    print("no")