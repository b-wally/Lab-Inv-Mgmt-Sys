#============================Back End Database Storage=======================================
import sqlite3
import datetime
from time import strptime
import serial
import threading

#=============================Defining Tables for Data ====================================
def EpioneData():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    #create table for incubator
    datbase.execute("""CREATE TABLE IF NOT EXISTS incubator (
            TagID text,
            Name text NOT NULL,
            Category text NOT NULL,
            Time_Remaining real,
            LastScan text
            )""")

    #Create table for Dry Storage
    datbase.execute("""CREATE TABLE IF NOT EXISTS drystorage (
            TagID text,
            Name text NOT NULL,
            Category text NOT NULL,
            Quantity real,
            ExpDate text,
            LastScan text
            )""")
    
    #Create table for refrigerator +4C
    datbase.execute("""CREATE TABLE IF NOT EXISTS fridge4 (    
            TagID text,
            Name text NOT NULL,
            Category text NOT NULL,
            Quantity real,
            LastScan text
            )""")
    
    #Create table for freezer of -20
    datbase.execute("""CREATE TABLE IF NOT EXISTS freeze20 (    
            TagID text,
            Name text NOT NULL,
            Category text NOT NULL,
            Quantity real,
            LastScan text
            )""")

    #Create table for freezer of -80
    datbase.execute("""CREATE TABLE IF NOT EXISTS freeze80 (
            TagID text,
            Name text NOT NULL,
            Category text NOT NULL,
            Quantity real ,
            LastScan text
            )""")
    conn.commit()
    conn.close()
    
EpioneData()
#==============================Incubator Table===================================
def IncData():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Time_Remaining, LastScan FROM incubator")
    rows = datbase.fetchall()
    return rows
    conn.commit()
    conn.close()

def IncCategories():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT Category FROM incubator")
    rows = datbase.fetchall()
    conn.close()
    rows = list(set(rows))
    return rows

def IncFilter(tree,category):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Time_Remaining, LastScan FROM incubator WHERE \
                                        Category = ?", (category,))
    rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values = row)
    conn.close()

def IncRefresh(table):
    table.delete(*table.get_children())
    inc_rows = IncData()
    for inc_row in inc_rows:
        table.insert('', 'end', values = inc_row)
    
def addIncItem(window, TagID, Name, Category, Time_Remaining, LastScan):
    if Time_Remaining != "NA":
        Time_Remaining = int(Time_Remaining)
        time = datetime.datetime.now() + datetime.timedelta(hours = Time_Remaining)
    else:
        time = "NA"
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("INSERT INTO incubator VALUES(?,?,?,?,?)",(TagID, Name, Category, \
                                                             time, LastScan,))
    try:
        datbase.execute("SELECT * FROM incubator WHERE TagID = ?",(TagID,))
        s = datbase.fetchall()
        if len(s) == 1:
            print("New Item Succesfully Added to Incubator!")
            window.destroy()
    except:
        print("Error Finding TagID in database")
    conn.commit()
    conn.close()

def IncSearch(tree, search):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM incubator WHERE Name LIKE (?) OR \
                                Category LIKE (?)",('%'+search+'%','%'+search+'%',))
    inc_rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for inc_row in inc_rows:
        tree.insert('', 'end', values = inc_row[1:5])
    conn.close

def IncDelete(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    try:
        datbase.execute("DELETE FROM incubator WHERE Name = ? AND Category = ? AND \
                        Time_Remaining = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    except:
        print("Item unable to be deleted")
    datbase.execute("SELECT * FROM incubator WHERE Name = ? AND Category = ? AND \
                        Time_Remaining = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchall()
    if len(s) == 0:
        print("Item Removed from Database!")
        tree.delete(item)
    else:
        print("Item still found in database :(")
    conn.commit()
    conn.close()

def IncEditData(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM incubator WHERE Name = ? AND Category = ? AND \
                        Time_Remaining = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchone()
    return s
    conn.commit()
    conn.close()

def IncEditUpdate(window, TagID, Name, Category, Time_Remaining):
    if Time_Remaining != "NA":
        Time_Remaining = int(Time_Remaining)
        time = datetime.datetime.now() + datetime.timedelta(hours = Time_Remaining)
    else:
        time = "NA"
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("UPDATE incubator SET Name = ?, Category = ?, Time_Remaining = ? \
                                    WHERE TagID = ?",(Name, Category, \
                                                        time, TagID,))
    conn.commit()
    conn.close()
    window.destroy()
    print("Incubator Item Updated!")
    
#==============================Dry Storage Table===================================
def DryData():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, ExpDate, LastScan FROM drystorage")
    rows = datbase.fetchall()
    return rows
    conn.close()

def DryCategories():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT Category FROM drystorage")
    rows = datbase.fetchall()
    conn.close()
    rows = list(set(rows))
    return rows

def DryFilter(tree,category):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, ExpDate, LastScan FROM drystorage WHERE \
                                        Category = ?", (category,))
    rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values = row)
    conn.close()

def DryRefresh(tree):
    tree.delete(*tree.get_children())
    dry_rows = DryData()
    for dry_row in dry_rows:
        tree.insert('', 'end', values = dry_row)

def addDryItem(window, TagID, Name, Category, Quantity, Month, Day, Year, LastScan):
    expdate = (Month + "/" + Day + "/" + Year)
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("INSERT INTO drystorage VALUES(?,?,?,?,?,?)",(TagID, Name, Category, \
                                                                 Quantity, expdate, LastScan,))
    try:
        datbase.execute("SELECT * FROM drystorage WHERE TagID = ?",(TagID,))
        s = datbase.fetchall()
        if len(s) == 1:
            print("New Item Succesfully Added to Dry Storage!")
            window.destroy()
    except:
        print("Error Finding Item")
    conn.commit()
    conn.close()

def DrySearch(tree, search):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM drystorage WHERE Name LIKE (?) OR \
                                Category LIKE (?)",('%'+search+'%','%'+search+'%',))
    dry_rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for dry_row in dry_rows:
        tree.insert('', 'end', values = dry_row[1:5])
    conn.close()

def DryDelete(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    try:
        datbase.execute("DELETE FROM drystorage WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND ExpDate = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],item2[4],))
    except:
        print("Item unable to be deleted")
    datbase.execute("SELECT * FROM drystorage WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND ExpDate = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],item2[4],))
    s = datbase.fetchall()
    if len(s) == 0:
        print("Item Removed from Database!")
        tree.delete(item)
    else:
        print("Item still found in database :(")
    conn.commit()
    conn.close()

def DryEditData(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM drystorage WHERE Name = ? AND Category = ? AND \
                        Quantity = ? AND ExpDate = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],item2[4],))
    s = datbase.fetchone()
    return s
    conn.commit()
    conn.close()

def DryEditUpdate(window, TagID, Name, Category, Quantity, ExpDate):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("UPDATE drystorage SET Name = ?, Category = ?, Quantity = ?, ExpDate = ? \
                                    WHERE TagID = ?",(Name, Category, \
                                                        Quantity, ExpDate, TagID,))
    conn.commit()
    conn.close()
    window.destroy()
    print("Dry Storage Item Updated!")

def DryExpDate():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT ExpDate FROM drystorage")
    expdates = datbase.fetchall()
    for i in range (len(expdates)):
        expdate = datetime.datetime.strptime(str(expdates[i]), "('%m/%d/%Y',)")
        compare = expdate - datetime.datetime.today()
        if compare.days <= 0:
            datbase.execute("SELECT TagID FROM drystorage WHERE ExpDate = ?", (str(expdates[i]),))
            tagids = datbase.fetchall()
            for tagid in tagids:
                print(tagid)
                datbase.execute("UPDATE drystorage SET ExpDate = ? WHERE TagID = ?", \
                                                    ("Expired!",tagid,))
    conn.close()
    
#==============================+4C Fridge Table===================================
def F4Data():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM fridge4")
    rows = datbase.fetchall()
    return rows
    conn.close()

def F4Categories():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT Category FROM fridge4")
    rows = datbase.fetchall()
    conn.close()
    rows = list(set(rows))
    return rows

def F4Filter(tree,category):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM fridge4 WHERE \
                                        Category = ?", (category,))
    rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values = row)
    conn.close()
    
def F4Refresh(table):
    table.delete(*table.get_children())
    f4_rows = F4Data()
    for f4_row in f4_rows:
        table.insert('', 'end', values = f4_row)
        
def addF4Item(window, TagID, Name, Category, Quantity, LastScan):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("INSERT INTO fridge4 VALUES(?,?,?,?,?)",(TagID, Name, Category, \
                                                                 Quantity, LastScan,))
    try:
        datbase.execute("SELECT * FROM fridge4 WHERE TagID = ?",(TagID,))
        s = datbase.fetchall()
        if len(s) >= 1:
            print("New Item Succesfully Added to -20C Freezer!")
            window.destroy()
    except:
        print("Error Finding Item")
    conn.commit()
    conn.close()
    
def F4Search(tree, search):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM fridge4 WHERE Name LIKE (?) OR \
                                Category LIKE (?)",('%'+search+'%','%'+search+'%',))
    f4_rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for f4_row in f4_rows:
        tree.insert('', 'end', values = f4_row[1:5])
    conn.close()

def F4Delete(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    try:
        datbase.execute("DELETE FROM fridge4 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
        print("item removed from database")
    except:
        print("Item unable to be deleted")
    datbase.execute("SELECT * FROM fridge4 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchall()
    if len(s) == 0:
        print("Item Removed from GUI!")
        tree.delete(item)
    else:
        print("Item still found in database :(")
    conn.commit()
    conn.close()

def F4EditData(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM fridge4 WHERE Name = ? AND Category = ? AND \
                        Quantity = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchone()
    return s
    conn.commit()
    conn.close()

def F4EditUpdate(window, TagID, Name, Category, Quantity):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("UPDATE fridge4 SET Name = ?, Category = ?, Quantity = ? \
                                    WHERE TagID = ?",(Name, Category, \
                                                        Quantity, TagID,))
    conn.commit()
    conn.close()
    window.destroy()
    print("Dry Storage Item Updated!")

#==============================-20C Freezer Table===================================
def F20Data():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM freeze20")
    rows = datbase.fetchall()
    return rows
    conn.close()

def F20Categories():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT Category FROM freeze20")
    rows = datbase.fetchall()
    conn.close()
    rows = list(set(rows))
    return rows

def F20Filter(tree,category):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM freeze20 WHERE \
                                        Category = ?", (category,))
    rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values = row)
    conn.close()

def F20Refresh(table):
    table.delete(*table.get_children())
    f20_rows = F20Data()
    for f20_row in f20_rows:
        table.insert('', 'end', values = f20_row)
    
def addF20Item(window, TagID, Name, Category, Quantity, LastScan):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("INSERT INTO freeze20 VALUES(?,?,?,?,?)",(TagID, Name, Category, \
                                                                 Quantity, LastScan,))
    try:
        datbase.execute("SELECT * FROM freeze20 WHERE TagID = ?",(TagID,))
        s = datbase.fetchall()
        if len(s) == 1:
            print("New Item Succesfully Added to -20C Freezer!")
            window.destroy()
    except:
        print("Error Finding Item")
    conn.commit()
    conn.close()
    
def F20Search(tree, search):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM freeze20 WHERE Name LIKE (?) OR \
                                Category LIKE (?)",('%'+search+'%','%'+search+'%',))
    f20_rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for f20_row in f20_rows:
        tree.insert('', 'end', values = f20_row[1:5])
    conn.close()

def F20Delete(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    print(item2)
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    try:
        datbase.execute("DELETE FROM freeze20 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
        print("item removed from database")
    except:
        print("Item unable to be deleted")
    datbase.execute("SELECT * FROM freeze20 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchall()
    if len(s) == 0:
        print("Item Removed from GUI!")
        tree.delete(item)
    else:
        print("Item still found in database :(")
    conn.commit()
    conn.close()

def F20EditData(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM freeze20 WHERE Name = ? AND Category = ? AND \
                        Quantity = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchone()
    return s
    conn.commit()
    conn.close()

def F20EditUpdate(window, TagID, Name, Category, Quantity):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("UPDATE freeze20 SET Name = ?, Category = ?, Quantity = ? \
                                    WHERE TagID = ?",(Name, Category, \
                                                        Quantity, TagID,))
    conn.commit()
    conn.close()
    window.destroy()
    print("Dry Storage Item Updated!")

#==============================-80C Freezer Table/functions===================================
def F80Data():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM freeze80")
    rows = datbase.fetchall()
    return rows
    conn.close()

def F80Categories():
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT Category FROM freeze80")
    rows = datbase.fetchall()
    conn.close()
    rows = list(set(rows))
    return rows

def F80Filter(tree,category):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    data = datbase.execute("SELECT Name, Category, Quantity, LastScan FROM freeze80 WHERE \
                                        Category = ?", (category,))
    rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values = row)
    conn.close()

def F80Refresh(table):
    table.delete(*table.get_children())
    f80_rows = F80Data()
    for f80_row in f80_rows:
        table.insert('', 'end', values = f80_row)
    
def addF80Item(window, TagID, Name, Category, Quantity, LastScan):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("INSERT INTO freeze80 VALUES(?,?,?,?,?)",(TagID, Name, Category,
                                                                 Quantity, LastScan,))
    try:
        datbase.execute("SELECT * FROM freeze80 WHERE TagID = ?",(TagID,))
        s = datbase.fetchall()
        if len(s) >= 1:
            print("New Item Succesfully Added to -80C Freezer!")
            window.destroy()
    except:
        print("Error Finding Item")
    conn.commit()
    conn.close()

def F80Search(tree, search):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM freeze80 WHERE Name LIKE (?) OR \
                                Category LIKE (?)",('%'+search+'%','%'+search+'%',))
    f80_rows = datbase.fetchall()
    tree.delete(*tree.get_children())
    for f80_row in f80_rows:
        tree.insert('', 'end', values = f80_row[1:5])
    conn.close()

def F80Delete(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    try:
        datbase.execute("DELETE FROM freeze80 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    except:
        print("Item unable to be deleted")
    datbase.execute("SELECT * FROM freeze80 WHERE Name = ? AND Category = ? AND Quantity = ? \
                        AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchall()
    if len(s) == 0:
        print("Item Removed from Database!")
        tree.delete(item)
    else:
        print("Item still found in database :(")
    conn.commit()
    conn.close()

def F80EditData(tree):
    item = tree.selection()
    item2 = tree.item(item, 'values')
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("SELECT * FROM freeze80 WHERE Name = ? AND Category = ? AND \
                        Quantity = ? AND LastScan = ?",(item2[0],item2[1],item2[2],item2[3],))
    s = datbase.fetchone()
    return s
    conn.commit()
    conn.close()

def F80EditUpdate(window, TagID, Name, Category, Quantity):
    conn = sqlite3.connect('EpioneDatabase.db')
    datbase = conn.cursor()
    datbase.execute("UPDATE freeze80 SET Name = ?, Category = ?, Quantity = ? \
                                    WHERE TagID = ?",(Name, Category, \
                                                        Quantity, TagID,))
    conn.commit()
    conn.close()
    window.destroy()
    print("Dry Storage Item Updated!")

#====================Tag Read Functions====================================
def SerialQueue(q):
    try: 
        ser = serial.Serial('/dev/ttyACM0', 115200)
        print("Connection to RFID Reader Succesful")
    except:
        print("Error Connecting to Serial Port")
    while ser:
        ard = ser.readline().decode('ASCII')
        ard_out = ard[:-2]
        if len(ard_out) == 30:
            print("Tag ID Recieved")
            TagID = list("nullnullnullnullnullnull")
            for i in range(5,29):
                TagID[i-5] = ard_out[i]
                i += 1
            TagID = "".join(TagID)
            tagtime = datetime.datetime.now()
            
            conn = sqlite3.connect('EpioneDatabase.db')
            datbase = conn.cursor()
            tables = datbase.execute("SELECT name FROM sqlite_master \
                                        WHERE type='table';").fetchall()
            result = []
            for table in tables:
                row = datbase.execute("SELECT LastScan FROM %s WHERE \
                                        TagID = ?"%table, (TagID,)).fetchall()
                if row == []:
                    lastscan = []
                if row != []:
                    lastscan = row[0]
                    table = table
                    break
            if lastscan != []:
                lastscan = str(lastscan[0])
                lastscan = datetime.datetime.strptime(lastscan, '%Y-%m-%d %H:%M:%S.%f')
                compare = tagtime - lastscan
                if compare.total_seconds() > 5:
                    datbase.execute("UPDATE %s SET LastScan = ? WHERE TagID = ?" \
                                    %table,(tagtime, TagID,))
                    conn.commit()
                    conn.close()
                    print("Scan Time Updated Succesfully")
                    del tagtime
                    del TagID
                else:
                    del TagID
                    del tagtime
            if lastscan == []:
                print("Tag not recognized in system... adding to queue")
                q.put(TagID)
                if q.full() == True:
                    q.task_done()
                    q.queue.clear()
                continue

def CheckQ(q, label):
    if q.empty() == True:
        label['text'] = "No Tag Found! Scan Item and Press Check for Tag Again" 
    if q.empty() == False:
        label['text'] = "New Tag ID Found! Press Confirm When Ready"
    





    
