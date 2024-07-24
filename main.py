from tkinter  import *
from tkinter import ttk
import pandas as pd
import xml.etree.ElementTree as ET 
import Maldata as md
#class MalParser:


class StartPage(ttk.Frame):
     def __init__(self,root):
        root.title("Enter in the file name")
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0 , sticky=("N W E S"))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.filename = StringVar()
        filename_entry = ttk.Entry(mainframe, width=7, textvariable=self.filename)
        filename_entry.grid(column=2,row=1,sticky=("W E"))
        self.test = StringVar()
        ttk.Label(mainframe,text="Enter your filename").grid(column=1, row=1)
        ttk.Button(mainframe,text="continue", command=lambda: root.destroy()).grid(column=2,row=2)
         
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        filename_entry.focus()
class Page1(ttk.Frame):
    def __init__(self,root):
        root.title("Anime Data Analyzer")
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0 , sticky=("N W E S"))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.geometry("1920x1080")
        self.text_widget = Text(mainframe, height=10, width=40)
        self.text_widget.grid(column=1, row=2, columnspan=3)

        #Need to add  Scores by ep graph, scorepie, barstatus, longest, toprated,
        ttk.Button(mainframe,text="Scores by Episode Count (opens graph in new window",command=lambda: md.ScoreEpisode(dataf)).grid(column=1,row=6)
        ttk.Button(mainframe,text="Scores in a Pi chart (opens graph in new window",command=lambda: md.scorepie(dataf)).grid(column=1,row=5)
        ttk.Button(mainframe,text="Bar Graph by Status",command=lambda: md.barstat(dataf)).grid(column=1,row=4)
        ttk.Button(mainframe,text="10 Longest Episodes",command=self.update_text2).grid(column=1,row=3)
        ttk.Button(mainframe,text="top rated shows ",command=self.update_text1).grid(column=1,row=2)
        ttk.Button(mainframe,text="summary", command=self.update_text).grid(column=1, row=1)
        ttk.Button(mainframe,text="quit",command=root.destroy).grid(column=1, row=0)
         
    def update_text(self):
        string_value=md.summary(dataf) 
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(END, string_value)
    def update_text2(self):
        string_value = md.longest(dataf)
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(END, string_value)
    def update_text1(self):
        string_value = md.toprated(dataf)
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(END, string_value)
xmlp: ET.XMLParser = ET.XMLParser(encoding="UTF-8")
tree: ET.ElementTree = ET.parse(source="animelist_nicholas.xml", parser=xmlp)
Aroot: ET.Element = tree.getroot()

data: list[dict[str, any]] = []

for anime in Aroot.findall('anime'):
    series_id: str = anime.find('series_animedb_id').text
    title: str = anime.find('series_title').text
    type_: str = anime.find('series_type').text
    episodes: int = int(anime.find('series_episodes').text)
    watched: int = int(anime.find('my_watched_episodes').text)
    score: int = int(anime.find('my_score').text)
    status: str = anime.find('my_status').text

    data.append({
        "series_id": series_id,
        "title": title,
        "type": type_,
        "episodes": episodes,
        "watched": watched,
        "score": score,
        "status": status,
        })

    dataf: pd.DataFrame = pd.DataFrame(data)

root = Tk()
StartPage(root)
root.mainloop()
Page1(root)
root.mainloop()

