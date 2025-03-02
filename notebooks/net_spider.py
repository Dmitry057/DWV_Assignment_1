import json
import requests
from bs4 import BeautifulSoup # web scraping tool
import sqlite3 as sql # for databases

targetWikiPage = "https://en.wikipedia.org/wiki/List_of_highest-grossing_films" # wikipedia page url
baseWikiPage = "https://en.wikipedia.org" # base url for accessing additional pages

def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

soup = get_soup(targetWikiPage)
tables = soup.find_all("table", class_="wikitable")
films_table = tables[0]

rows = films_table.find_all("tr")
films = []

# function to convert string representing revenue to int
def str2int(string: str) -> int:
    numeric = 

# iterate through rows (except header row) and extract film data
for row in rows[1:]:
    cells = row.find_all("td")
    headers = row.find_all("th")
    film_href = headers[0].find_all("a")[0]
    
    # collect all available data from the row
    film = {
        "year": cells[3].text.strip(),
        "title": film_href.text.strip(),
        "revenue": int("".join([char for char in cells[2].text.strip() if char.isnumeric()])),
        "href": film_href["href"], # we will use this to access director and country data
    }

    films.append(film)
films




# this function will parse film page and extract country data
@retry()
def get_country(href: str) -> str:
    response = requests.get(baseWikiPage + href)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.select_one("table", class_="infobox")
    try:
        country = data.find("th", string="Country").find_next("td").text.strip()
    except Exception:
        country_td = data.find("th", string="Countries").find_next("td")
        ul = country_td.find("ul")
        country = (
            ", ".join([li.text.strip() for li in ul.find_all("li")])
            if ul
            else country_td.text.strip()
        )
    return country


# this function will parse film page and extract director data
@retry()
def get_director(href: str) -> str:
    response = requests.get(baseWikiPage + href)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.select_one("table", class_="infobox")
    director_td = data.find("th", string="Directed by").find_next("td")
    director_list = director_td.find("ul")
    director = (
        ", ".join([li.text.strip() for li in director_list.find_all("li")])
        if director_list
        else director_td.text.strip()
    )
    return director


# parse film pages and extract additional data
# if our script fails to parse the page, we will set the value to "NONE"
# and print the name of problematic film
for film in films:
    try:
        film["country"] = get_country(film["href"])
    except Exception:
        film["country"] = "NONE"
        print(f"Failed to get country for {film['title']}")

    try:
        film["director"] = get_director(film["href"])
    except Exception:
        film["director"] = "NONE"
        print(f"Failed to get director for {film['title']}")
        
        
for film in films:
    if film["title"] == "Ne Zha 2":
        film["country"] = "China"
        film["director"] = "Jiaozi"
        
        
# We will use SQLite to store our data
conn = sql.connect("data/films.db")
cursor = conn.cursor()

# This command is needed to make it possible to rerun this cell
cursor.execute("DROP TABLE IF EXISTS films")

# Schema is the same is in assignment instruction
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS films (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_year INTEGER,
        director TEXT,
        box_office REAL,
        country TEXT
    )
    """
)

# Insert film data one by one
for film in films:
    cursor.execute(
        """
        INSERT INTO films (title, release_year, director, box_office, country)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            film["title"],
            film["year"],
            film["director"],
            film["revenue"],
            film["country"],
        ),
    )

conn.commit()

# check if data was inserted correctly
cursor.execute("SELECT * FROM films").fetchall()



# For ease of deployment to GitHub pages, we will also save the data in JSON format
with open("data/films.json", "w") as file:
    json.dump(films, file)