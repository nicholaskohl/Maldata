"""
This is the main File that the main.py uses all it's logic for, it's using Pandas and the built in MAL xml to parse it 
you can get your MAL xml file at https://myanimelist.net/panel.php?go=export
To run this file properly you need Pandas, matplotlib, and Numpy

"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

#This is a Scatter plot that gets Episode Scores and compares them to how long the show is, it takes in user put in watch values. 
def ScoreEpisode(dataf) -> None:
    print("Showing Scatter plot")
    #These two calls are made into varibles to make it easier to read
    watched = dataf['watched']
    scores = dataf['score']
    #constructing the graph
    plt.figure(figsize=(10,6))
    plt.scatter(watched ,scores,alpha=0.6)
    #this are using NUMPY to add a trending line
    line = np.polyfit(watched, scores,1)
    addto = np.poly1d(line)
    plt.title('Score vs Episode Count')
    plt.xlabel('Number of episodes')
    plt.ylabel('Score')
    plt.grid(True)
    plt.plot(watched,addto(watched))
    plt.show()

#This gets a Summary of the data, being Average episode count, how many they finish and average scores for movies and tv with total episodes as well
def summary(dataf):
    print("Showing summary")
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
    

#this makes a pi chart that shows the user their scores by percentage
def scorepie(dataf):
    print("showing Pie chart")
    scores = dataf['score'].value_counts()

    plt.figure(figsize=(10,6))
    scores.plot.pie(autopct='%1.1f%%')
    plt.title('Distribution of scores')
    plt.ylabel('')
    plt.show()

#This code makes a Bar graph of your shows by statuses, such as completed or watching
def barstat(dataf):
    print("Showing Bargraph")
    statuses = dataf['status'].value_counts()
    plt.figure(figsize=(10,6))
    statuses.plot.bar()
    plt.title('status by number of shows')
    plt.xlabel('statuses')
    plt.ylabel('Amount')
    plt.show()


#This code gets the user's 10 Longests shows by geting the head of the file after sorting by watched
def longest(dataf):
   
    print("Showing longest shows")
    sorted_df = dataf.sort_values(by='watched', ascending=False)
    top_ten_longest = sorted_df.head(10)
    count = 1
    print("Your 10 longest shows are\n")
    resultStr = ""
    for _, row in top_ten_longest.iterrows():
       resultStr += f"Number {count} {row['title']} at {row['watched']} episodes watched with a status of {row['status']}\n\n"
       count += 1
    return resultStr

#Retrives the User's highest score given then prints out shows given that score
def toprated(dataf):
    print("Showing top rated shows")
    sorted_df = dataf.sort_values(by='score', ascending=False)
    top_score =sorted_df['score'].max()
    top_scores = sorted_df[sorted_df['score'] == top_score]
    resultStr = ""
    for _, row in top_scores.iterrows():
        resultStr += f"{row['title']} at a rating of {top_score}\n\n"
    return resultStr
   
        
            
        



