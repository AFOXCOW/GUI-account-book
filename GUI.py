import tkinter as tk
import tkinter.ttk as ttk
import sys
import pandas as pd
import numpy as np 
import os 

class Toplevel1:
    def __init__(self, db, top):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        def button_search_by_time():
            Time = self.TEntry4.get()
            results,error = self.db.search_by_time(Time)
            msg = "Time".ljust(15,' ')+"Comment".center(45,' ')+"Money".rjust(10,' ')+"\n" #15 char 25 char 10 char
            if not error:
                if results!=[]:
                    for res in results:
                        str_res = res[0].ljust(15,' ')+res[1].center(45,' ')+str(res[2]).rjust(10,' ')
                        msg = msg+str_res+'\n'
                    self.notify.set(msg)
                else:
                    self.notify.set("No Search Result")
            else:
                self.notify.set(self.db.msg)
        def button_insert():
            Time = self.TEntry1.get()
            cmt = self.TEntry3.get()
            cmt = cmt.replace(' ','_')
            Money_float = self.TEntry2.get()
            string = Time+' '+cmt+' '+Money_float
            self.db.insert(string)
            self.notify.set(self.db.msg)

        def button_delete():
            Time = self.TEntry4.get()
            self.db.delete_by_time(Time)
            self.notify.set(self.db.msg)

        def button_import():
            filename = "account.xlsx"
            if not os.path.exists(filename):
                self.notify.set("No excel file named account.xlsx")
            else:
                self.db.import_from_excel(filename)
                self.notify.set("Import from excel Accomplished")
        def button_calculate_balance():
            sql = "select * from %s" % self.db.tablename
            self.db_df = pd.read_sql_query(sql,self.db.conn)
            nparr = self.db_df.values
            money = nparr[:,2]
            Balance = np.sum(money)
            self.notify.set("The Balance is: "+str(Balance))

        def export_excel():
            self.db.export_table_to_excel(self.db.tablename)
            self.notify.set("Export Accomplished")

        self.notify = tk.StringVar()
        self.db = db
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+600+240")
        top.minsize(120, 1)
        top.maxsize(1900, 1080)
        top.resizable(1, 1)
        top.title("Account Book GUI")
        top.configure(background="#d9d9d9")

        self.TEntry1 = ttk.Entry(top)
        self.TEntry1.place(relx=0.050, rely=0.090, relheight=0.050, relwidth=0.200)
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="ibeam")

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.050, rely=0.020, relheight=0.050, relwidth=0.200)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(anchor='w')
        self.TLabel1.configure(justify='left')
        self.TLabel1.configure(text='''日期(2020-02-02)''')

        self.TEntry2 = ttk.Entry(top)
        self.TEntry2.place(relx=0.250, rely=0.090, relheight=0.050, relwidth=0.200)
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="fleur")

        self.TEntry3 = ttk.Entry(top)
        self.TEntry3.place(relx=0.450, rely=0.090, relheight=0.050, relwidth=0.45)
        self.TEntry3.configure(takefocus="")
        self.TEntry3.configure(cursor="ibeam")

        self.TLabel2 = ttk.Label(top)
        self.TLabel2.place(relx=0.250, rely=0.020, relheight=0.050, relwidth=0.200)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font="TkDefaultFont")
        self.TLabel2.configure(relief="flat")
        self.TLabel2.configure(anchor='w')
        self.TLabel2.configure(justify='left')
        self.TLabel2.configure(text='''金额(-100)''')

        self.TLabel3 = ttk.Label(top)
        self.TLabel3.place(relx=0.450, rely=0.020, relheight=0.050, relwidth=0.200)
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief="flat")
        self.TLabel3.configure(anchor='w')
        self.TLabel3.configure(justify='left')
        self.TLabel3.configure(text='''注释说明''')

        self.TButton1 = ttk.Button(top,command=button_insert)
        self.TButton1.place(relx=0.400, rely=0.150, relheight=0.070, relwidth=0.150)
        self.TButton1.configure(takefocus="")
        self.TButton1.configure(text='''插入''')

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.0, rely=0.250, relwidth=1.0)



        self.TLabel4 = ttk.Label(top)
        self.TLabel4.place(relx=0.050, rely=0.260, relheight=0.050, relwidth=0.200)
        self.TLabel4.configure(background="#d9d9d9")
        self.TLabel4.configure(foreground="#000000")
        self.TLabel4.configure(font="TkDefaultFont")
        self.TLabel4.configure(relief="flat")
        self.TLabel4.configure(anchor='w')
        self.TLabel4.configure(justify='left')
        self.TLabel4.configure(text='''日期(2020-02-02)''')
        self.TLabel4.configure(cursor="fleur")


        self.TEntry4 = ttk.Entry(top)
        self.TEntry4.place(relx=0.050, rely=0.310,  relheight=0.050, relwidth=0.200)
        self.TEntry4.configure(takefocus="")
        self.TEntry4.configure(cursor="ibeam")



        self.TButton2 = ttk.Button(top,command=button_search_by_time)
        self.TButton2.place(relx=0.300, rely=0.300, relheight=0.070, relwidth=0.150)
        self.TButton2.configure(takefocus="")
        self.TButton2.configure(text='''Search''')

        self.TButton3 = ttk.Button(top,command=button_delete)
        self.TButton3.place(relx=0.450, rely=0.300, relheight=0.070, relwidth=0.150)
        self.TButton3.configure(takefocus="")
        self.TButton3.configure(text='''Delete''')

        self.TButton4 = ttk.Button(top,command=export_excel)
        self.TButton4.place(relx=0.600, rely=0.300, relheight=0.070, relwidth=0.150)
        self.TButton4.configure(takefocus="")
        self.TButton4.configure(text='''Export''')

        self.TButton5 = ttk.Button(top,command=button_import)
        self.TButton5.place(relx=0.750, rely=0.300, relheight=0.070, relwidth=0.150)
        self.TButton5.configure(takefocus="")
        self.TButton5.configure(text='''Import''')

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.0, rely=0.400, relwidth=1.0)

        self.TButton6 = ttk.Button(top,command=button_calculate_balance)
        self.TButton6.place(relx=0.400, rely=0.450, relheight=0.070, relwidth=0.150)
        self.TButton6.configure(takefocus="")
        self.TButton6.configure(text='''Balance''')

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=0.0, rely=0.550, relwidth=1.0)

        self.TLabel5 = ttk.Label(top,textvariable=self.notify)
        self.TLabel5.place(relx=0.050, rely=0.600, relheight=0.350, relwidth=0.850)
        self.TLabel5.configure(background="#f9f9f9")
        self.TLabel5.configure(foreground="#000000")
        self.TLabel5.configure(font="TkDefaultFont")
        self.TLabel5.configure(relief="flat")
        self.TLabel5.configure(anchor='w')
        self.TLabel5.configure(justify='left')
        self.TLabel5.configure(text='''notify''')