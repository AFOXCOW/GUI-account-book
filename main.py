import numpy as np 
import sqlite3
import os
import datetime
import pandas as pd
import sys
import tkinter as tk
import tkinter.ttk as ttk
import Database
import GUI

def vp_start_gui(db):
    root = tk.Tk()
    top = GUI.Toplevel1 (db,root)
    root.mainloop()

if __name__ == '__main__':
    db = Database.DataBase("Lab407.db")
    tablename = "account_book"
    if db.tablename==None:
    	db.create_table(tablename)
    	db.set_default_table(tablename)
    else:
    	db.set_default_table(tablename)
    
    vp_start_gui(db)
    del(db)