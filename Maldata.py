"""
This is Code made to parse your MAL data, go to https://myanimelist.net/panel.php?go=export to get your data as an xml file, 
right now I haven't added the option to dynamically add your animelist, but simply replace the source with the xml file
Be sure to compile with the command "python -X utf8 Maldata.py" to make sure it accurately parases utf-8 encoded character
"""
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
"""
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
"""

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
    interacted = dataf[dataf['status'] != 'Plan to Watch']
    percentage = (interacted["watched"].mean()/interacted["episodes"].mean())
    average_episodes = tv_shows["watched"].mean()
    finished_percentage = percentage * 100
    average_movie_score = movies["score"].mean()
    average_tv_score = tv_shows["score"].mean()
    total_episodes_watched = dataf["watched"].sum()
    result = (
            f"The average amount of episodes you watch per anime is {average_episodes:.2f}\n"
            f"Out of the shows you've watched, you've finished {finished_percentage:.2f}% of their episodes\n"
            f"The average score you give to movies is {average_movie_score:.2f} and to tv shows {average_tv_score:.2f}\n"
            f"And the total amount of episodes you've watched is {total_episodes_watched}\n"
            )
    return result
    
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

def longest(dataf):
   

     sorted_df = dataf.sort_values(by='watched', ascending=False)
     top_ten_longest = sorted_df.head(10)
     count = 1
     print("Your 10 longest shows are\n")
     resultStr = ""
     for _, row in top_ten_longest.iterrows():
        resultStr += f"Number {count} {row['title']} at {row['watched']} episodes watched with a status of {row['status']}\n\n"
        count += 1
     return resultStr
        
def toprated(dataf):
    sorted_df = dataf.sort_values(by='score', ascending=False)
    top_score =sorted_df['score'].max()
    top_scores = sorted_df[sorted_df['score'] == top_score]
    resultStr = ""
    for _, row in top_scores.iterrows():
        resultStr += f"{row['title']} at a rating of {top_score}\n\n"
    return resultStr
   
        
            
        



