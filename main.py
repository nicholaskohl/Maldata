from tkinter  import *
from tkinter import ttk
import tkinter as tk
import pandas as pd
import xml.etree.ElementTree as ET 
import Maldata as md



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My anime list Data Analyzer")
        
        self.filename = tk.StringVar()

        self.start_page = StartPage(self, self.filename)
        self.page1 = Page1(self,self.filename)

        self.start_page.grid(row=0, column=0, sticky=("N W E S"))
        self.page1.grid(row=0,column=0, sticky=("N W E S"))
        
        self.show_frame(self.start_page)

    def show_frame(self,frame):
        frame.tkraise()

#This is the Setup for the start page, the user enters the file name of their animelist, which lets the program do it's work
class StartPage(ttk.Frame):
     def __init__(self,root, filename):
        super().__init__(root) 
        
        self.root = root
        self.filename = filename

        root.title("Enter in the file name")

        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0 , sticky=("N W E S"))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        

        filename_entry = ttk.Entry(mainframe, width=7, textvariable=self.filename)
        filename_entry.grid(column=2,row=1,sticky=("W E"))
        ttk.Label(mainframe,text="Enter your filename").grid(column=1, row=1)
        ttk.Button(mainframe,text="continue", command=self.load_data).grid(column=2,row=2)
         
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        filename_entry.focus()

     def load_data(self):
        try:
            filename = self.filename.get()
            #This is setting up the parser for my data specfically 
            #ToDo figure out how to make this dynamic to the user
    
            xmlp: ET.XMLParser = ET.XMLParser(encoding="UTF-8")
            tree: ET.ElementTree = ET.parse(source=filename, parser=xmlp)
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
            global dataf 
            dataf = pd.DataFrame(data)
            self.root.show_frame(self.root.page1)
        except Exception as e:
            print(f"Error loading file: {e}")


#This is the setup for Page 1
class Page1(ttk.Frame):
    def __init__(self,root, filename):
        super().__init__(root)
        self.root = root
        self.filename = filename
        root.title("Anime Data Analyzer")
        
        #This is setting up the frame for what we're adding to it
        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0 , sticky=("N W E S"))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.text_widget = Text(mainframe, height=10, width=50)
        self.text_widget.grid(column=1, row=7, columnspan=8)
        
        #These are all the commands I made in the Maldata file, running on a gui, they use Lambda so they only activate on click
        ttk.Button(mainframe,text="quit",command=root.destroy).grid(column=1, row=6)
        ttk.Button(mainframe,text="Scores by Episode Count (opens graph in new window",command=lambda: md.ScoreEpisode(dataf)).grid(column=1,row=5)
        ttk.Button(mainframe,text="Scores in a Pi chart (opens graph in new window",command=lambda: md.scorepie(dataf)).grid(column=1,row=4)
        ttk.Button(mainframe,text="Bar Graph by Status",command=lambda: md.barstat(dataf)).grid(column=1,row=3)
        ttk.Button(mainframe,text="10 Longest Episodes",command=self.update_text2).grid(column=1,row=2)
        ttk.Button(mainframe,text="top rated shows ",command=self.update_text1).grid(column=1,row=1)
        ttk.Button(mainframe,text="summary", command=self.update_text).grid(column=1, row=0)

         
        #ToDo find a fix for this by making it one function
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

#after the Dataframe is made using all the Data in the XML file we make the gui with these commands and previous classes
if __name__ == "__main__":
    root = App()
    root.mainloop()
