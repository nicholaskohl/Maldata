"""
This is Code made to parse your MAL data, go to https://myanimelist.net/panel.php?go=export to get your data as an xml file, 
right now I haven't added the option to dynamically add your animelist, but simply replace the source with the xml file
Be sure to compile with the command "python -X utf8 Maldata.py" to make sure it accurately parases utf-8 encoded character
"""
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import matplotlib.pyplot as plt
import pandas as pd

# Ensure proper encoding handling
xmlp = ET.XMLParser(encoding="UTF-8")
tree = ET.parse(source='', parser=xmlp)
root = tree.getroot()
data = []
for anime in root.findall('anime'):#id,title,tpye,episodes,wathced episodes, score, status
    data.append({
        "series_id": anime.find('series_animedb_id').text,
        "title": anime.find('series_title').text,
        "type": anime.find('series_type').text,
        "episodes": int(anime.find('series_episodes').text),
        "watched": int(anime.find('my_watched_episodes').text),
        "score": int(anime.find('my_score').text),
        "status": anime.find('my_status').text
        })

dataf = pd.DataFrame(data)
def ScoreEpisode(dataf) -> None:
    plt.figure(figsize=(10,6))
    plt.scatter(dataf['watched'],dataf['score'],alpha=0.6)
    plt.title('Score vs Episode Count')
    plt.xlabel('Number of episodes')
    plt.ylabel('Score')
    plt.grid(True)
    plt.show()
def summary(dataf):
    tv_shows = dataf[dataf['type'] == 'TV']
    movies = dataf[dataf['type'] == 'Movie']
    print(f"the average amount of episodes you watch per anime is {tv_shows["watched"].mean():.2f}")
    print(f"the average score you give to movies is {movies["score"].mean():.2f} and to tv shows {tv_shows["score"].mean():.2f}")
    print(f"And the total amount of episodes you've watched is {dataf["watched"].sum()}")
def scorepie(dataf):
    scores = dataf['score'].value_counts()

    plt.figure(figsize=(10,6))
    scores.plot.pie(autopct='%1.1f%%')
    plt.title('Distribution of scores')
    plt.ylabel('')
    plt.show()
def barstat(dataf):
    print("hello world")
    statuses = dataf['status'].value_counts()
    plt.figure(figsize=(10,6))
    statuses.plot.bar()
    plt.title('status by number of shows')
    plt.xlabel('statuses')
    plt.ylabel('Amount')
    plt.show()
scorepie(dataf)
