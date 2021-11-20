#==========================Front End GUI======================================
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import EpioneDatabasev10
import threading
import queue
import datetime
#============================= Main Window Setup=======================================
#==========================Front End GUI======================================
class EpioneGUI:
    def __init__(self,root):
        self.root = root
        self.root.title("Epione Solution Inventory Management System")
        self.root.geometry("900x400")
        
        #Setting up Tabs For Storage Location
        tab_control = ttk.Notebook(root)

        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Incubator')
        tab_control.pack(expand=1, fill='both')
        
        tab2 = ttk.Frame(tab_control)
        tab_control.add(tab2, text='Dry Storage')
        tab_control.pack(expand=1, fill='both')

        tab3 = ttk.Frame(tab_control)
        tab_control.add(tab3, text='+4 Refrigerator')
        tab_control.pack(expand=1, fill='both')
        
        tab4 = ttk.Frame(tab_control)
        tab_control.add(tab4, text='-20C Freezer')
        tab_control.pack(expand=1, fill='both')

        tab5 = ttk.Frame(tab_control)
        tab_control.add(tab5, text='-80C Freezer')
        tab_control.pack(expand=1, fill='both')

        #===============================Defining Each Tab of MainFrame==================

        #=============INCUBATOR TAB===========================
        #adding drop down menus to incubator tab
        inc_cat = Combobox(tab1)
        inc_cat['values'] = EpioneDatabasev10.IncCategories()
        inc_cat.set('Categories')
        inc_cat.grid(column=0, row=1)
        #adding drop down menus for time remaining in incubator
        inc_time = Combobox(tab1)
        inc_time['values']= ('Time Remaining','Over 24 Hours Remaining','12-24 hours remaining',
                          '3-12 Hours Remaining','Under 3 Hours Remaining')
        inc_time.current(0)
        inc_time.grid(column=1, row=1)
        #add button for filter
        inc_filter = Button(tab1, text = "Filter", command= lambda: \
                                    EpioneDatabasev10.IncFilter(inc_list, inc_cat.get()))
        inc_filter.grid(row = 1, column = 2)
        #add text entry for search 
        inc_search = Entry(tab1,width=10)
        inc_search.insert(0,"Search Here")
        inc_search.grid(column=3, row=1)
        inc_searchbtn = Button(tab1, text="Search", command = lambda : \
                               EpioneDatabasev10.IncSearch(inc_list, inc_search.get()))\
                               .grid(column=4, row=1)
        #treeview frame for data display
        inc_frame = Frame(tab1, relief = RAISED)
        inc_frame.grid(row = 3, column = 0, columnspan = 8)
        inc_list = Treeview(inc_frame)
        inc_list.bind("<<TreeviewSelect>>")
        inc_list.pack(side = 'left')
        inc_list["columns"] = ("one", "two", "three", "four")
        inc_list['show'] = 'headings'
        inc_list.column("one", width = 200)
        inc_list.heading("one", text = "Name")
        inc_list.column("two",width = 200)
        inc_list.heading("two", text = "Category")
        inc_list.column("three", width = 200)
        inc_list.heading("three", text = "Time To Be Taken Out")
        inc_list.column("four",width = 200)
        inc_list.heading("four", text = "Last Scan")
        vsb = ttk.Scrollbar(inc_frame, orient="vertical", command= inc_list.yview)
        vsb.pack(side='right', fill='y')
        inc_list.configure(yscrollcommand=vsb.set)
        
        inc_rows = EpioneDatabasev10.IncData()
        for inc_row in inc_rows:
            inc_list.insert('', 'end', values = inc_row)
        
        #buton to create new item
        inc_createbtn = Button(tab1, text="Create New", command = NewItem.NewItemWin)\
                        .grid(column=0, row=4)    
        #button to edit selected item on table
        inc_edit = Button(tab1, text = "Edit Selected Item", command = lambda: \
                                          EditItem.EditItemWin('inc_list',inc_list))\
                                          .grid(row = 4, column = 1)

        #button to delete item from table
        inc_delete = Button(tab1, text = "Delete Selected Item", command = lambda: \
                            EpioneDatabasev10.IncDelete(inc_list)).grid(row = 4, column = 2)
        
        #button to refresh data table
        inc_refresh = Button(tab1, text = "Refresh Data Table", command = lambda: \
                             EpioneDatabasev10.IncRefresh(inc_list)).grid(row = 4, column = 4)
        
        #=======DRY STORAGE TAB===========
        #adding drop down menus for dry storage tab
        dry_cat = Combobox(tab2)
        dry_cat['values']= EpioneDatabasev10.DryCategories()
        dry_cat.set('Categories')
        dry_cat.grid(column=0, row=1)
        dry_inv = Combobox(tab2)
        dry_inv['values']= ('Inventory Level','Low Inventory', 'Out of Stock')
        dry_inv.current(0)
        dry_inv.grid(column=1, row=1)
        #add button for filter
        dry_filter = Button(tab2, text = "Filter", command = lambda: \
                            EpioneDatabasev10.DryFilter(dry_list, dry_cat.get()))
        dry_filter.grid(row = 1, column = 2)
        #add dry storage search entry 
        dry_search = Entry(tab2,width=10)
        dry_search.insert(0,"Search Here")
        dry_search.grid(column=3, row=1)
        dry_searchbtn = Button(tab2, text="Search", command= lambda: \
                               EpioneDatabasev10.DrySearch(dry_list, dry_search.get()))
        dry_searchbtn.grid(column=4, row=1)
        #add treeview frame to display data
        dry_frame = Frame(tab2)
        dry_frame.grid(row = 3, columnspan = 6)
        dry_list = Treeview(dry_frame)
        dry_list.pack(side = 'left')
        dry_list["columns"] = ("one", "two", "three", "four", "five")
        dry_list['show'] = 'headings'
        dry_list.column("one", width = 200)
        dry_list.heading("one", text = "Name")
        dry_list.column("two",width = 150)
        dry_list.heading("two", text = "Category")
        dry_list.column("three", width = 125)
        dry_list.heading("three", text = "Quantity Remaining")
        dry_list.column("four",width = 100)
        dry_list.heading("four", text = "Expiration Date")
        dry_list.column("five",width = 200)
        dry_list.heading("five", text = "Last Scan")
        
        dry_scroll = ttk.Scrollbar(dry_frame, orient="vertical", command=dry_list.yview)
        dry_scroll.pack(side='right', fill='y')
        dry_list.configure(yscrollcommand=dry_scroll.set)
        
        dry_rows = EpioneDatabasev10.DryData()
        for dry_row in dry_rows:
            dry_list.insert('', 'end', values = dry_row)
            
        #add buton to create new item
        dry_createbtn = Button(tab2, text="Create New", command= NewItem.NewItemWin)\
                        .grid(row = 4, column = 0)
        #button to edit selected item on table
        dry_edit = Button(tab2, text = "Edit Selected Item", command = lambda: \
                                          EditItem.EditItemWin('dry_list',dry_list))\
                                          .grid(row = 4, column = 1)
        #button to delete item from table
        dry_delete = Button(tab2, text = "Delete Selected Item", command = lambda: \
                            EpioneDatabasev10.DryDelete(dry_list)).grid(row = 4, column = 2)
        #button to refresh data table
        dry_refresh = Button(tab2, text = "Refresh Data Table", command = lambda: \
                             EpioneDatabasev10.DryRefresh(dry_list)).grid(row = 4, column = 4)  
        
        #============+4C Refrigerator TAB==================
        #adding drop down menus for dry storage tab
        f4_cat = Combobox(tab3)
        f4_cat['values']= EpioneDatabasev10.F4Categories()
        f4_cat.set('Categories')
        f4_cat.grid(column=0, row=1)
        f4_inv = Combobox(tab3)
        f4_inv['values']= ('Inventory Level','Low Inventory', 'Out of Stock')
        f4_inv.current(0)
        f4_inv.grid(column=1, row=1)
        #add button for filter
        f4_filter = Button(tab3, text = "Filter", command = lambda: \
                           EpioneDatabasev10.F4Filter(f4_list,f4_cat.get()))
        f4_filter.grid(row = 1, column = 2)
        #add -20c freezer search entry 
        f4_search = Entry(tab3,width=10)
        f4_search.insert(0,"Search Here")
        f4_search.grid(column=3, row=1)
        f4_searchbtn = Button(tab3, text="Search", command = lambda: \
                               EpioneDatabasev10.F4Search(f4_list, f4_search.get()))\
                               .grid(column=4, row=1)
        #adding treeview frame to display data
        f4_frame = Frame(tab3)
        f4_frame.grid(row = 3, columnspan = 6)
        f4_list = Treeview(f4_frame)
        f4_list.pack(side = 'left')
        f4_list["columns"] = ("one", "two", "three", "four")
        f4_list['show'] = 'headings'
        f4_list.column("one", width = 200)
        f4_list.heading("one", text = "Name")
        f4_list.column("two",width = 200)
        f4_list.heading("two", text = "Category")
        f4_list.column("three", width = 200)
        f4_list.heading("three", text = "Quantity Remaining")
        f4_list.column("four",width = 200)
        f4_list.heading("four", text = "Last Scan")
        f4_scroll = ttk.Scrollbar(f4_frame, orient="vertical", command=f4_list.yview)
        f4_scroll.pack(side='right', fill='y')
        f4_list.configure(yscrollcommand=f4_scroll.set)
        
        f4_rows = EpioneDatabasev10.F4Data()
        for f4_row in f4_rows:
            f4_list.insert('', 'end', values = f4_row)
            
        #add buton to create new item
        f4_createbtn = Button(tab3, text="Create New", command= NewItem.NewItemWin)
        f4_createbtn.grid(row=4, column=0)
        #button to edit selected item on table
        f4_edit = Button(tab3, text = "Edit Selected Item", command = lambda: \
                                          EditItem.EditItemWin('f4_list',f4_list))\
                                          .grid(row = 4, column = 1)
        #button to delete item from table
        f4_delete = Button(tab3, text = "Delete Selected Item", command = lambda: \
                            EpioneDatabasev10.F4Delete(f4_list)).grid(row = 4, column = 2)
        #button to refresh data table
        f4_refresh = Button(tab3, text = "Refresh Data Table", command = lambda: \
                             EpioneDatabasev10.F4Refresh(f4_list)).grid(row = 4, column = 4) 
           
        #============-20C FREEZER TAB==================
        #adding drop down menus for dry storage tab
        f20_cat = Combobox(tab4)
        f20_cat['values']= EpioneDatabasev10.F20Categories()
        f20_cat.set('Categories')
        f20_cat.grid(column=0, row=1)
        f20_inv = Combobox(tab4)
        f20_inv['values']= ('Inventory Level','Low Inventory', 'Out of Stock')
        f20_inv.current(0)
        f20_inv.grid(column=1, row=1)
        #add button for filter
        f20_filter = Button(tab4, text = "Filter", command = lambda: \
                           EpioneDatabasev10.F20Filter(f20_list,f20_cat.get()))
        f20_filter.grid(row = 1, column = 2)
        #add -20c freezer search entry 
        f20_search = Entry(tab4,width=10)
        f20_search.insert(0,"Search Here")
        f20_search.grid(column=3, row=1)
        f20_searchbtn = Button(tab4, text="Search", command = lambda: \
                               EpioneDatabasev10.F20Search(f20_list, f20_search.get()))\
                               .grid(column=4, row=1)
        #adding treeview frame to display data
        f20_frame = Frame(tab4)
        f20_frame.grid(row = 3, columnspan = 6)
        f20_list = Treeview(f20_frame)
        f20_list.pack(side = 'left')
        f20_list["columns"] = ("one", "two", "three", "four")
        f20_list['show'] = 'headings'
        f20_list.column("one", width = 200)
        f20_list.heading("one", text = "Name")
        f20_list.column("two",width = 200)
        f20_list.heading("two", text = "Category")
        f20_list.column("three", width = 200)
        f20_list.heading("three", text = "Quantity Remaining")
        f20_list.column("four",width = 200)
        f20_list.heading("four", text = "Last Scan")
        f20_scroll = ttk.Scrollbar(f20_frame, orient="vertical", command=f20_list.yview)
        f20_scroll.pack(side='right', fill='y')
        f20_list.configure(yscrollcommand=f20_scroll.set)
        
        f20_rows = EpioneDatabasev10.F20Data()
        for f20_row in f20_rows:
            f20_list.insert('', 'end', values = f20_row)
            
        #add buton to create new item
        f20_createbtn = Button(tab4, text="Create New", command= NewItem.NewItemWin)
        f20_createbtn.grid(row=4, column=0)
        #button to edit selected item on table
        f20_edit = Button(tab4, text = "Edit Selected Item", command = lambda: \
                                          EditItem.EditItemWin('f20_list',f20_list))\
                                          .grid(row = 4, column = 1)
        #button to delete item from table
        f20_delete = Button(tab4, text = "Delete Selected Item", command = lambda: \
                            EpioneDatabasev10.F20Delete(f20_list)).grid(row = 4, column = 2)
        #button to refresh data table
        f20_refresh = Button(tab4, text = "Refresh Data Table", command = lambda: \
                             EpioneDatabasev10.F20Refresh(f20_list)).grid(row = 4, column = 4) 

        #=================-80C FREEZER TAB===========
        #adding drop down menus for dry storage tab
        f80_cat = Combobox(tab5)
        f80_cat['values']= EpioneDatabasev10.F80Categories()
        f80_cat.set('Categories')
        f80_cat.grid(column=0, row=1)
        f80_inv = Combobox(tab5)
        f80_inv['values']= ('Inventory Level','Low Inventory', 'Out of Stock')
        f80_inv.current(0)
        f80_inv.grid(column=1, row=1)
        #add button for filter
        f80_filter = Button(tab5, text = "Filter", command = lambda: \
                           EpioneDatabasev10.F80Filter(f80_list,f80_cat.get()))
        f80_filter.grid(row = 1, column = 2)
        #add -80C freezer storage search entry 
        f80_search = Entry(tab5,width=10)
        f80_search.insert(0,"Search Here")
        f80_search.grid(column=3, row=1)
        f80_searchbtn = Button(tab5, text="Search", command= lambda: \
                               EpioneDatabasev10.F80Search(f80_list, f80_search.get()))\
                               .grid(column=4, row=1)
        #adding treeview frame to display data
        f80_frame = Frame(tab5)
        f80_frame.grid(row = 3, columnspan = 6)
        f80_list = Treeview(f80_frame)
        f80_list.pack(side = 'left')
        f80_list["columns"] = ("one", "two", "three", "four")
        f80_list['show'] = 'headings'
        f80_list.column("one", width = 200)
        f80_list.heading("one", text = "Name")
        f80_list.column("two",width = 200)
        f80_list.heading("two", text = "Category")
        f80_list.column("three", width = 200)
        f80_list.heading("three", text = "Quantity Remaining")
        f80_list.column("four",width = 200)
        f80_list.heading("four", text = "Last Scan")
        f80_scroll = ttk.Scrollbar(f80_frame, orient="vertical", command = f80_list.yview)
        f80_scroll.pack(side='right', fill='y')
        f80_list.configure(yscrollcommand=f80_scroll.set)
        
        f80_rows = EpioneDatabasev10.F80Data()
        for f80_row in f80_rows:
            f80_list.insert('', 'end', values = f80_row)
            
        #add buton to create new item
        f80_createbtn = Button(tab5, text="Create New", command = NewItem.NewItemWin)
        f80_createbtn.grid(row=4, column=0)
        #button to edit selected item on table
        f80_edit = Button(tab5, text = "Edit Selected Item", command = lambda: \
                                          EditItem.EditItemWin('f80_list',f80_list))\
                                          .grid(row = 4, column = 1)
        #button to delete item from table
        f80_delete = Button(tab5, text = "Delete Selected Item", command = lambda: \
                            EpioneDatabasev10.F80Delete(f80_list)).grid(row = 4, column = 2)
        #button to refresh data table
        f80_refresh = Button(tab5, text = "Refresh Data Table", command = lambda: \
                             EpioneDatabasev10.F80Refresh(f80_list)).grid(row = 4, column = 4) 

#================================== New Item Functions ============================================
class NewItem():
    def __init__(self, root):
        self.root = root
        self.root.title("Add a New Item to the Inventory")
        self.root.geometry("400x200")
        self.loc_req_txt = Label(root, text = "Where would you like to add your new item?: ")
        self.loc_req_txt.grid(row = 0, column = 0 )
        self.loc_req_combo = Combobox(root)
        self.loc_req_combo['values'] = ('Incubator', 'Dry Storage','+4C Refrigerator',\
                                        '-20C Freezer', '-80C Freezer')
        self.loc_req_combo.grid(row = 1, column = 0)

        self.loc_okbtn = Button(root, text = "Confirm Location", command = lambda: \
                                        self.NewItemTree(self.loc_req_combo.get()))
        self.loc_okbtn.grid(row = 2, column = 0)

    def NewItemWin():
        newitem = NewItem(Toplevel())
        if q.empty() == False:
            q.task_done()
            q.queue.clear()
        
    def NewItemTree(self,loc):
        if loc == 'Incubator':
            inc_item_win = Toplevel()
            inc_item_win.title("Incubator Storage New Item")
            inc_label = Label(inc_item_win, text = ("Enter Item Information: "))\
                            .grid(row = 0, column = 1)            
            name_entry = Entry(inc_item_win)
            name_entry.grid(column = 1, row = 1)
            name_lbl = Label(inc_item_win, text = "Enter Name: ")
            name_lbl.grid(column = 0, row = 1)

            cat_entry = Combobox(inc_item_win,)
            cat_entry['values'] = ('Cell Cultures', 'Reagents')
            cat_entry.grid(column = 1, row = 2)
            cat_lbl = Label(inc_item_win, text = "Enter Category: ")
            cat_lbl.grid(column = 0, row = 2)
            
            time_entry = Entry(inc_item_win)
            time_entry.grid(column = 1, row = 3)
            name_lbl = Label(inc_item_win, text = "Enter Time Remaining in Incubator (Hrs): ")
            name_lbl.grid(column = 0, row = 3)
            
            scantxt = Label(inc_item_win, text = "Press 'Check for Tag ID' to Initialize new item")
            scantxt.grid(row = 4, column = 1)
            self.scanbtn = Button(inc_item_win, text = "Check for Tag ID", command = lambda: \
                                  EpioneDatabasev10.CheckQ(q,scantxt))
            self.scanbtn.grid(row = 4, column = 0)
                
            conf_btn = Button(inc_item_win, text = "Confirm",command = lambda: \
                              EpioneDatabasev10.addIncItem(inc_item_win, q.get(), \
                                                        name_entry.get(),cat_entry.get(), \
                                                        time_entry.get(), datetime.datetime.now(),))                   
            conf_btn.grid(row = 4, column = 2)

        if loc == 'Dry Storage':
            dry_item_win = Toplevel()
            dry_item_win.title("Dry Storage")
            dry_label = Label(dry_item_win, text = ("Enter Item Information: "))\
                        .grid(row = 0, column = 0)
            
            name_entry = Entry(dry_item_win)
            name_entry.grid(column = 1, row = 1)
            name_lbl = Label(dry_item_win, text = "Enter Name: ")
            name_lbl.grid(column = 0, row = 1)

            cat_entry = Combobox(dry_item_win)
            cat_entry['values'] = ('Cell Cultures', 'Reagents')
            cat_entry.grid(column = 1, row = 2)
            cat_lbl = Label(dry_item_win, text = "Enter Category: ")
            cat_lbl.grid(column = 0, row = 2)
            
            quant_entry = Entry(dry_item_win)
            quant_entry.grid(column = 1, row = 3)
            name_lbl = Label(dry_item_win, text = "Enter Quantity: ")
            name_lbl.grid(column = 0, row = 3)

            expdatelbl = Label(dry_item_win, text = "Enter Exp Date")
            expdatelbl.grid(row = 4,column = 0)

            year = datetime.datetime.today().year
            years = [year + i for i in range (25)]
            years.insert(0,"Year")
            months = [1 + i for i in range (12)]
            months.insert(0,"Month")
            months = [str(item).zfill(2) for item in months]
            days = [1 + i for i in range (31)]
            days.insert(0, "Day")
            days = [str(item).zfill(2) for item in days]
            
            monthcombo = Combobox(dry_item_win, state = "readonly")
            monthcombo['values'] = (months)
            monthcombo.current(0)
            monthcombo.grid(row=4, column = 1)
            
            daycombo = Combobox(dry_item_win, state = "readonly")
            daycombo['values'] = (days)
            daycombo.current(0)
            daycombo.grid(row=5, column = 1)
            
            yearcombo = Combobox(dry_item_win, state = "readonly")
            yearcombo['values'] = (years)
            yearcombo.current(0)
            yearcombo.grid(row=6, column = 1)

            scantxt = Label(dry_item_win, text = "Press 'Check for Tag ID' to Initialize new item")
            scantxt.grid(row = 7, column = 0)
            scanbtn = Button(dry_item_win, text = "Check for Tag ID", command = lambda: \
                                  EpioneDatabasev10.CheckQ(q,scantxt))
            scanbtn.grid(row = 7, column = 1)

            conf_btn = Button(dry_item_win, text = "Confirm",command = lambda: \
                              EpioneDatabasev10.addDryItem(dry_item_win, q.get(), \
                                                        name_entry.get(), cat_entry.get(), \
                                                        quant_entry.get(),monthcombo.get(),\
                                                          daycombo.get(),yearcombo.get(),\
                                                          datetime.datetime.now(),))                              
            conf_btn.grid(row = 7, column = 2)

        if loc == '+4C Refrigerator':
            f4_item_win = Toplevel()
            f4_item_win.title("+4C Refrigerator")
            f4_label = Label(f4_item_win, text = ("Enter Item Information: "))\
                        .grid(row = 0, column = 0)
            
            name_entry = Entry(f4_item_win)
            name_entry.grid(column = 1, row = 1)
            name_lbl = Label(f4_item_win, text = "Enter Name: ")
            name_lbl.grid(column = 0, row = 1)

            cat_entry = Combobox(f4_item_win)
            cat_entry['values'] = ('Cell Cultures', 'Reagents')
            cat_entry.grid(column = 1, row = 2)
            cat_lbl = Label(f4_item_win, text = "Enter Category: ")
            cat_lbl.grid(column = 0, row = 2)
            
            quant_entry = Entry(f4_item_win)
            quant_entry.grid(column = 1, row = 3)
            name_lbl = Label(f4_item_win, text = "Enter Quantity: ")
            name_lbl.grid(column = 0, row = 3)

            scantxt = Label(f4_item_win, text = "Press 'Check for Tag ID' to Initialize new item")
            scantxt.grid(row = 4, column = 0)
            scanbtn = Button(f4_item_win, text = "Check for Tag ID", command = lambda: \
                                  EpioneDatabasev10.CheckQ(q,scantxt))
            scanbtn.grid(row = 4, column = 1)

            conf_btn = Button(f4_item_win, text = "Confirm", command = lambda: \
                              EpioneDatabasev10.addF4Item(f4_item_win, q.get(), \
                                                        name_entry.get(), cat_entry.get(), \
                                                        quant_entry.get(), datetime.datetime.now(),))
            conf_btn.grid(row = 4, column = 2)
        
        if loc == '-20C Freezer':
            f20_item_win = Toplevel()
            f20_item_win.title("-20C Freezer")
            f20_label = Label(f20_item_win, text = ("Enter Item Information: "))\
                        .grid(row = 0, column = 0)
            
            name_entry = Entry(f20_item_win)
            name_entry.grid(column = 1, row = 1)
            name_lbl = Label(f20_item_win, text = "Enter Name: ")
            name_lbl.grid(column = 0, row = 1)

            cat_entry = Combobox(f20_item_win)
            cat_entry['values'] = ('Cell Cultures', 'Reagents')
            cat_entry.grid(column = 1, row = 2)
            cat_lbl = Label(f20_item_win, text = "Enter Category: ")
            cat_lbl.grid(column = 0, row = 2)
            
            quant_entry = Entry(f20_item_win)
            quant_entry.grid(column = 1, row = 3)
            name_lbl = Label(f20_item_win, text = "Enter Quantity: ")
            name_lbl.grid(column = 0, row = 3)

            scantxt = Label(f20_item_win, text = "Press 'Check for Tag ID' to Initialize new item")
            scantxt.grid(row = 4, column = 0)
            scanbtn = Button(f20_item_win, text = "Check for Tag ID", command = lambda: \
                                  EpioneDatabasev10.CheckQ(q,scantxt))
            scanbtn.grid(row = 4, column = 1)

            conf_btn = Button(f20_item_win, text = "Confirm", command = lambda: \
                              EpioneDatabasev10.addF20Item(f20_item_win, q.get(), \
                                                        name_entry.get(), cat_entry.get(), \
                                                        quant_entry.get(), datetime.datetime.now(),))
            conf_btn.grid(row = 4, column = 2)

        if loc == '-80C Freezer':
            f80_item_win = Toplevel()
            f80_item_win.title("-80C Freezer")
            f80_label = Label(f80_item_win, text = ("Enter Item Information: "))\
                        .grid(row = 0, column = 0)
            
            name_entry = Entry(f80_item_win)
            name_entry.grid(column = 1, row = 1)
            name_lbl = Label(f80_item_win, text = "Enter Name: ")
            name_lbl.grid(column = 0, row = 1)

            cat_entry = Combobox(f80_item_win)
            cat_entry['values'] = ('Cell Cultures', 'Reagents')
            cat_entry.grid(column = 1, row = 2)
            cat_lbl = Label(f80_item_win, text = "Enter Category: ")
            cat_lbl.grid(column = 0, row = 2)
            
            quant_entry = Entry(f80_item_win)
            quant_entry.grid(column = 1, row = 3)
            name_lbl = Label(f80_item_win, text = "Enter Quantity: ")
            name_lbl.grid(column = 0, row = 3)
            
            scantxt = Label(f80_item_win, text = "Press 'Check for Tag ID' to Initialize new item")
            scantxt.grid(row = 4, column = 0)
            scanbtn = Button(f80_item_win, text = "Check for Tag ID", command = lambda: \
                                  EpioneDatabasev10.CheckQ(q,scantxt))
            scanbtn.grid(row = 4, column = 1)
            
            conf_btn = Button(f80_item_win, text = "Confirm", command = lambda: \
                              EpioneDatabasev10.addF80Item(f80_item_win, q.get(), \
                                                        name_entry.get(), cat_entry.get(), \
                                                        quant_entry.get(), datetime.datetime.now(),))
            conf_btn.grid(row = 4, column = 2)
            
#========================Creating class to edit items=======================================

class EditItem():
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x200")
        self.root.title('title')

    def EditItemWin(treename, tree):
        if treename == 'inc_list':
            item = EpioneDatabasev10.IncEditData(tree)
            inc_edit_win = Toplevel()
            inc_edit_win.title("Incubator Storage Edit Item")
            inc_label = Label(inc_edit_win, text = ("Change Item Information: "))\
                            .grid(row = 0, column = 1)

            TagID_entry = Label(inc_edit_win, text = item[0])
            TagID_entry.grid(column = 1, row = 1)
            TagID_lbl = Label(inc_edit_win, text = "TagID: ")
            TagID_lbl.grid(column = 0, row = 1)
            
            name_entry = Entry(inc_edit_win)
            name_entry.insert(0,item[1])
            name_entry.grid(column = 1, row = 2)
            name_lbl = Label(inc_edit_win, text = "Name: ")
            name_lbl.grid(column = 0, row = 2)

            cat_entry = Entry(inc_edit_win)
            cat_entry.insert(0,item[2])
            cat_entry.grid(column = 1, row = 3)
            cat_lbl = Label(inc_edit_win, text = "Category: ")
            cat_lbl.grid(column = 0, row = 3)
            
            time_entry = Entry(inc_edit_win)
            time_entry.insert(0, item[3])
            time_entry.grid(column = 1, row = 4)
            time_lbl = Label(inc_edit_win, text = "Time Remaining in Incubator (Hrs): ")
            time_lbl.grid(column = 0, row = 4)
            
            conf_btn = Button(inc_edit_win, text = "Confirm Item Properties",command = lambda: \
                              EpioneDatabasev10.IncEditUpdate(inc_edit_win, item[0], \
                                                        name_entry.get(),cat_entry.get(), \
                                                        time_entry.get(),))                       
            conf_btn.grid(row = 5, column = 1)

        if treename == 'dry_list':
            item = EpioneDatabasev10.DryEditData(tree)
            dry_edit_win = Toplevel()
            dry_edit_win.title("Dry Storage Edit Item")
            dry_label = Label(dry_edit_win, text = ("Change Item Information: "))\
                            .grid(row = 0, column = 1)

            TagID_entry = Label(dry_edit_win, text = item[0])
            TagID_entry.grid(column = 1, row = 1)
            TagID_lbl = Label(dry_edit_win, text = "TagID: ")
            TagID_lbl.grid(column = 0, row = 1)
            
            name_entry = Entry(dry_edit_win)
            name_entry.insert(0,item[1])
            name_entry.grid(column = 1, row = 2)
            name_lbl = Label(dry_edit_win, text = "Name: ")
            name_lbl.grid(column = 0, row = 2)

            cat_entry = Entry(dry_edit_win)
            cat_entry.insert(0,item[2])
            cat_entry.grid(column = 1, row = 3)
            cat_lbl = Label(dry_edit_win, text = "Category: ")
            cat_lbl.grid(column = 0, row = 3)

            quant_entry = Entry(dry_edit_win)
            quant_entry.insert(0, item[3])
            quant_entry.grid(column = 1, row = 4)
            quant_lbl = Label(dry_edit_win, text = "Quantity: ")
            quant_lbl.grid(column = 0, row = 4)

            date_entry = Entry(dry_edit_win)
            date_entry.insert(0,item[4])
            date_entry.grid(column = 1, row = 5)
            date_lbl = Label(dry_edit_win, text = "Exp Date: ")
            date_lbl.grid(column = 0, row = 5)
            
            conf_btn = Button(dry_edit_win, text = "Confirm Item Properties",command = lambda: \
                              EpioneDatabasev10.DryEditUpdate(dry_edit_win, item[0], \
                                                        name_entry.get(),cat_entry.get(), \
                                                        quant_entry.get(),date_entry.get(),))                       
            conf_btn.grid(row = 6, column = 1)

        if treename == 'f4_list':
            item = EpioneDatabasev10.F4EditData(tree)
            f4_edit_win = Toplevel()
            f4_edit_win.title("+4C Refrigerator Edit Item")
            f4_lbl = Label(f4_edit_win, text = ("Change Item Information: "))\
                            .grid(row = 0, column = 1)
            
            TagID_entry = Label(f4_edit_win, text = item[0])
            TagID_entry.grid(column = 1, row = 1)
            TagID_lbl = Label(f4_edit_win, text = "TagID: ")
            TagID_lbl.grid(column = 0, row = 1)
            
            name_entry = Entry(f4_edit_win)
            name_entry.insert(0,item[1])
            name_entry.grid(column = 1, row = 2)
            name_lbl = Label(f4_edit_win, text = "Name: ")
            name_lbl.grid(column = 0, row = 2)

            cat_entry = Entry(f4_edit_win)
            cat_entry.insert(0,item[2])
            cat_entry.grid(column = 1, row = 3)
            cat_lbl = Label(f4_edit_win, text = "Category: ")
            cat_lbl.grid(column = 0, row = 3)
            
            quant_entry = Entry(f4_edit_win)
            quant_entry.insert(0, item[3])
            quant_entry.grid(column = 1, row = 4)
            quant_lbl = Label(f4_edit_win, text = "Quantity: ")
            quant_lbl.grid(column = 0, row = 4)
            
            conf_btn = Button(f4_edit_win, text = "Confirm Item Properties",command = lambda: \
                              EpioneDatabasev10.F4EditUpdate(f4_edit_win, item[0], \
                                                        name_entry.get(),cat_entry.get(), \
                                                        quant_entry.get(),))                       
            conf_btn.grid(row = 5, column = 1)
        
        if treename == 'f20_list':
            item = EpioneDatabasev10.F20EditData(tree)
            f20_edit_win = Toplevel()
            f20_edit_win.title("-20C Freezer Edit Item")
            f20_lbl = Label(f20_edit_win, text = ("Change Item Information: "))\
                            .grid(row = 0, column = 1)
            
            TagID_entry = Label(f20_edit_win, text = item[0])
            TagID_entry.grid(column = 1, row = 1)
            TagID_lbl = Label(f20_edit_win, text = "TagID: ")
            TagID_lbl.grid(column = 0, row = 1)
            
            name_entry = Entry(f20_edit_win)
            name_entry.insert(0,item[1])
            name_entry.grid(column = 1, row = 2)
            name_lbl = Label(f20_edit_win, text = "Name: ")
            name_lbl.grid(column = 0, row = 2)

            cat_entry = Entry(f20_edit_win)
            cat_entry.insert(0,item[2])
            cat_entry.grid(column = 1, row = 3)
            cat_lbl = Label(f20_edit_win, text = "Category: ")
            cat_lbl.grid(column = 0, row = 3)
            
            quant_entry = Entry(f20_edit_win)
            quant_entry.insert(0, item[3])
            quant_entry.grid(column = 1, row = 4)
            quant_lbl = Label(f20_edit_win, text = "Quantity: ")
            quant_lbl.grid(column = 0, row = 4)
            
            conf_btn = Button(f20_edit_win, text = "Confirm Item Properties",command = lambda: \
                              EpioneDatabasev10.F20EditUpdate(f20_edit_win, item[0], \
                                                        name_entry.get(),cat_entry.get(), \
                                                        quant_entry.get(),))                       
            conf_btn.grid(row = 5, column = 1)
            
        if treename == 'f80_list':
            item = EpioneDatabasev10.F80EditData(tree)
            f80_edit_win = Toplevel()
            f80_edit_win.title("-80C Freezer Edit Item")
            f80_lbl = Label(f80_edit_win, text = ("Change Item Information: "))\
                            .grid(row = 0, column = 1)
            
            TagID_entry = Label(f80_edit_win, text = item[0])
            TagID_entry.grid(column = 1, row = 1)
            TagID_lbl = Label(f80_edit_win, text = "TagID: ")
            TagID_lbl.grid(column = 0, row = 1)
            
            name_entry = Entry(f80_edit_win)
            name_entry.insert(0,item[1])
            name_entry.grid(column = 1, row = 2)
            name_lbl = Label(f80_edit_win, text = "Name: ")
            name_lbl.grid(column = 0, row = 2)

            cat_entry = Entry(f80_edit_win)
            cat_entry.insert(0,item[2])
            cat_entry.grid(column = 1, row = 3)
            cat_lbl = Label(f80_edit_win, text = "Category: ")
            cat_lbl.grid(column = 0, row = 3)
            
            quant_entry = Entry(f80_edit_win)
            quant_entry.insert(0, item[3])
            quant_entry.grid(column = 1, row = 4)
            quant_lbl = Label(f80_edit_win, text = "Quantity: ")
            quant_lbl.grid(column = 0, row = 4)
            
            conf_btn = Button(f80_edit_win, text = "Confirm Item Properties",command = lambda: \
                              EpioneDatabasev10.F80EditUpdate(f80_edit_win, item[0], \
                                                        name_entry.get(),cat_entry.get(), \
                                                        quant_entry.get(),))                    
            conf_btn.grid(row = 5, column = 1)
            
#=========================Main loop to run applciation======================================
if __name__ == '__main__':
    root = Tk()
    application = EpioneGUI(root)
    
    global q
    q = queue.LifoQueue(maxsize = 5)
    constant_read = threading.Thread(target = EpioneDatabasev10.SerialQueue, args = (q,))
    constant_read.start()
    
    root.mainloop()




#/dev/ttyACM0
    
