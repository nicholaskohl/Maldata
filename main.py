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
        mainframe.grid(column=0, row=0 , sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.filename = StringVar()
        filename_entry = ttk.Entry(mainframe, width=7, textvariable=self.filename)
        filename_entry.grid(column=2,row=1,sticky=(W, E))
        self.test = StringVar()
        ttk.Label(mainframe,text="Enter your filename").grid(column=1, row=1)
        ttk.Button(mainframe,text="continue").grid(column=2,row=2)
        
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        filename_entry.focus()
class Page1(ttk.Frame):
    def __init__(self,root , dataf):
        root.title("Anime Data Analyzer")
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0 , sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.text_widget = Text(mainframe, height=10, width=40)
        self.text_widget.grid(column=0, row=2, columnspan=3)

        ttk.Button(mainframe,text="summary", command=self.update_text).grid(column=1, row=1)
        ttk.Button(mainframe,text="quit",command=root.destroy).grid(column=1, row=0)
    def update_text(self):
        string_value=md.summary(dataf) 
        self.text_widget.delete(1.0,END)
        self.text_widget.insert(END, string_value)

xmlp = ET.XMLParser(encoding="UTF-8")
tree = ET.parse(source='animelist_nicholas.xml', parser=xmlp)
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



root = Tk()
Page1(root, dataf)
root.mainloop()

