# import modules 
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import datetime as dt
from mydb import Database  # Import the Database class from mydb
from tkinter import messagebox
import matplotlib.pyplot as plt

# object for database
data = Database(db='test.db')  # Initialize the Database object with the database file 'test.db'

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get(), item_group=item_group.get())
    refreshData()

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')
    item_group.delete(0, 'end')

def fetch_records():
    global count
    f = data.fetchRecord('SELECT rowid, * FROM expense_record')
    for rec in f:
        tv.insert(parent='', index='end', iid=count, values=(rec[1], rec[2], rec[3], rec[4], rec[5]))  # Corrected indices
        count += 1
    calculate_stats()

def calculate_stats():
    expenses = data.fetchRecord('SELECT item_group, SUM(item_price) FROM expense_record GROUP BY item_group')
    plot_graph(expenses)

def plot_graph(expenses):
    groups = [expense[0] for expense in expenses]
    prices = [expense[1] for expense in expenses]

    plt.figure(figsize=(10, 6))

    plt.bar(groups, prices, color='skyblue')
    plt.title('Expense Distribution by Item Group')
    plt.xlabel('Item Group')
    plt.ylabel('Total Expense')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]  # Adjusted index to skip serial number
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
        item_group.set(val[4])
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()
    # Update record
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), item_group.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get(), item_group.get()))  # Removed selected_rowid
    except Exception as ep:
        messagebox.showerror('Error',  ep)

    # Clear entry boxes
    clearEntries()
    refreshData()

def totalBalance():
    f = data.fetchRecord(query="SELECT SUM(item_price) FROM expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()
    
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

# create tkinter object
ws = Tk()
ws.title('Expense Tracking System')

# variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()
item_group = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)
Label(f1, text='ITEM GROUP', font=f).grid(row=3, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)
item_group_entry = Entry(f1, font=f, textvariable=item_group)
# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))
item_group_entry.grid(row=3, column=1, sticky=EW, padx=(10, 0))

# Function to show calendar
def show_calendar():
    top = Toplevel(ws)
    cal = Calendar(top, selectmode='day', year=dt.datetime.now().year, month=dt.datetime.now().month, day=dt.datetime.now().day)
    cal.pack(fill="both", expand=True)
    def set_date():
        dopvar.set(cal.get_date())
        top.destroy()
    Button(top, text="OK", command=set_date).pack()
    

# Action buttons
cur_date = Button(
    f1, 
    text='Current Date', 
    font=f, 
    bg='#04C4D9', 
    command=setDate,
    width=15
    )

popup_cal = Button(
    f1,
    text='Select Date',
    font=f,
    bg='#04C4D9',
    command=show_calendar
)

submit_btn = Button(
    f1, 
    text='Save Record', 
    font=f, 
    command=saveRecord, 
    bg='#42602D', 
    fg='white'
    )

clr_btn = Button(
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries, 
    bg='#D9B036', 
    fg='white'
    )

quit_btn = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#D33532', 
    fg='white'
    )

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#486966',
    command=totalBalance
)

update_btn = Button(
    f1, 
    text='Update',
    bg='#C2BB00',
    command=update_record,
    font=f
)

del_btn = Button(
    f1, 
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
)

# grid placement
cur_date.grid(row=4, column=0, sticky=EW, padx=(10, 0))
popup_cal.grid(row=4, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5), show='headings', height=8)  # Adjusted number of columns
tv.pack(side="left")

# add heading to treeview
tv.column(1, anchor=CENTER)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.column(5, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")  # Adjusted heading
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")
tv.heading(5, text="Item Group")

# binding treeview
tv.bind("<Double-Button-1>", select_record)


# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# calling function 
fetch_records()

# infinite loop
ws.mainloop()