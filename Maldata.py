"""
This is Code made to parse your MAL data, go to https://myanimelist.net/panel.php?go=export to get your data as an xml file, 
right now I haven't added the option to dynamically add your animelist, but simply replace the source with the xml file
Be sure to compile with the command "python -X utf8 Maldata.py" to make sure it accurately parases utf-8 encoded character
"""
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
# Ensure proper encoding handling
xmlp = ET.XMLParser(encoding="UTF-8")
tree = ET.parse(source='', parser=xmlp)
root = tree.getroot()


def printMovie(root):
    # Iterate over the child elements starting from the second one
    for child in root[1:]:
        series_type = child.find('series_type')
        series_title = child.find('series_title')

    # Check if series_type is found and not None
        if series_type is not None and series_type.text == "TV":

        # Check if series_title is found and not None before printing
            if series_title is not None:

                print(series_title.text)

def longestSeries(root):
    max = -1 #setting max to -1 because no values would be negative
    showName = ""
    for child in root[1:]:
        series_episodes = child.find('series_episodes')
        series_title = child.find('series_title')
        
        if  int(series_episodes.text) > max:#this code iterates over your list and finds the max value of show length
            max = int(series_episodes.text)
            showName = series_title.text
    print(f"The longest show you've watched has {max} episodes and is called {showName}")
            
def showstatus(root):
    print("your choices are watching,completed,onhold,dropped, and plantowatch")#prompts the user for the showstatus
    findstat = input("what status of show would you like to look for")
    
    for child in root[1:]:
        status = child.find('my_status')
        show = child.find('series_title')
        if(status.text.lower() == findstat.lower()):
            print(show.text)#if the status is found it prints out the show name, so you can see what you have completed

def showrating(root):
    findrate = input("What rating would you like to find")#prompts the user to find shows based on what rating they've given
    for child in root[1:]:
        rate = child.find('my_score')
        show = child.find('series_title')
        if(findrate == rate.text):
            print(show.text)

def visualizeStatus(root):
    statusdict = {"total": int(root[0][3].text),#this way of making the dict by parsing the data is o(1) vs the o(n) verison because it's already accounted for
                  "watching": int(root[0][4].text),
                  "completed": int(root[0][5].text),
                  "onhold": int(root[0][6].text),
                  "dropped":  int(root[0][7].text),
                  "plantowatch": int(root[0][8].text)
            }
    statuses = list(statusdict.keys())
    counts = list(statusdict.values())
    #using matplotlib to make a bargraph
    plt.figure(figsize=(10,6))
    plt.bar(statuses,counts,color='skyblue')
    plt.xlabel("Status")
    plt.ylabel("amount of shows")
    plt.title("Comparison of amount of shows to given status")
    plt.show()

def scorepie(root):
    scoredict = {}#making a dictonary of scores, by how many shows you gave said score
    for child in root[1:]:
        score = child.find('my_score')
        if score.text in scoredict:
            scoredict[score.text] += 1
        else:
            scoredict[score.text] = 1
    #matplotlib code to make it into a nice bargraph
    plt.figure(figsize=(10,6))
    scores = list(scoredict.values())
    scoresgiv = list(scoredict.keys())
    colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251', '#B565A7', '#009B77', '#DD4124', '#D65076'] 
    plt.pie(scores,colors=colors,labels=scoresgiv,autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()



        
        
#The data has series id, series title, series type, series episodes, watched episodes, started and finish dates, what you score it, your status on it
if __name__ == '__main__':

    scorepie(root)


