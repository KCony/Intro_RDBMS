from tkinter import *
from tkinter.simpledialog import askstring
import psycopg
import sqlite3
from sqlite3 import Error

class Table:
    def __init__(self, root, data):
        self.data = data
        self.total_rows = len(data)
        self.total_columns = len(data[0])
        for i in range(self.total_rows):
            for j in range(self.total_columns):
                self.e = Entry(root, width=20, fg=config['font_color'], font=('Arial', 16, 'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(END, self.data[i][j])

    def destroy(self, root):
        for widget in root.winfo_children():
            widget.destroy()

t = None
username = ''
config = {'width': 1800, 'height': 900, 'font_color': 'blue', 'min_lat': 27, 'max_lat': 60, 'min_lon': -170, 'max_lon': -120}


def clicked1():
    cursor = cnx.cursor()

    query = ("SELECT m.market_name, c.city, s.state_full, m.lat, m.lon FROM markets m "
             "JOIN cities c ON c.city_id = m.city JOIN states s ON s.state_id = m.state "
             "WHERE lat BETWEEN %s AND %s AND lon BETWEEN %s AND %s;")

    cursor.execute(query, (float(min_lat.get()), float(max_lat.get()), float(min_lon.get()), float(max_lon.get())))
    lst = []
    for (market_name, city, state, lat, lon) in cursor:
        lst.append((market_name, city, state, lat, lon))
    cursor.close()
    global t
    if t is not None:
        t.destroy(bottom_frame)
    t = Table(bottom_frame, lst)


def login_command():
    global username
    global config
    username = askstring('Username', 'Please enter your username')
    cursorObj.execute('SELECT * FROM settings WHERE username = ?', (username,))
    row = cursorObj.fetchone()
    config = {'width': row[1], 'height': row[2], 'font_color': row[3], 'min_lat': row[4], 'max_lat': row[5],
              'min_lon': row[6], 'max_lon': row[7]}
    window.geometry(f'{config['width']}x{config['height']}')


def on_window_resize(event):
    global config
    config['width'] = event.width
    config['height'] = event.height


window = Tk()
window.title("Farmers Market Finder")
window.geometry(f'{config['width']}x{config['height']}')
window.bind("<Configure>", on_window_resize)

main_frame = Frame(window)
main_frame.pack()

top_frame = Frame(main_frame)
top_frame.pack(side=TOP)

bottom_frame = Frame(main_frame)
bottom_frame.pack(side=BOTTOM)

btn = Button(top_frame, text="Apply filter", bg="black", fg="red", font=("Arial Bold", 10), command=clicked1)
btn.grid(column=0, row=4, columnspan=2)

btn = Button(top_frame, text="Login", bg="yellow", fg=config['font_color'], font=("Arial Bold", 10), command=login_command)
btn.grid(column=7, row=4)

Label(top_frame, text="Min latitude:").grid(row=0, column=0, sticky=W, pady=10, padx=10)
min_lat = Entry(top_frame, width=30)
min_lat.grid(column=0, row=1)
min_lat.delete(0, END)
min_lat.insert(0, config['min_lat'])

Label(top_frame, text="Max latitude:").grid(row=0, column=1, sticky=W, pady=10, padx=10)
max_lat = Entry(top_frame, width=30)
max_lat.grid(column=1, row=1)
max_lat.delete(0, END)
max_lat.insert(0, config['max_lat'])

Label(top_frame, text="Min longitude:").grid(row=2, column=0, sticky=W, pady=10, padx=10)
min_lon = Entry(top_frame, width=30)
min_lon.grid(column=0, row=3)
min_lon.delete(0, END)
min_lon.insert(0, config['min_lon'])

Label(top_frame, text="Max longitude:").grid(row=2, column=1, sticky=W, pady=10, padx=10)
max_lon = Entry(top_frame, width=30)
max_lon.grid(column=1, row=3)
max_lon.delete(0, END)
max_lon.insert(0, config['max_lon'])

cursorObj = None
try:
    con = sqlite3.connect('settings.db')
    cursorObj = con.cursor()
    cursorObj.execute("""CREATE TABLE if not exists settings( 
        username text PRIMARY KEY,
        width int,
        height int,
        font_color text,
        min_lat real,
        max_lat real,
        min_lon real,
        max_lon real
        )
        """)
    con.commit()
except Error:
    print(Error)

cnx = psycopg.connect(dbname="farmers_markets",
                        host="localhost",
                        user="marketsuser",
                        password="Pa$$W0rd",
                        port="5432")
clicked1()
window.mainloop()

if username != '':
    params = [username]
    params.extend(list(config.values()))
    params = tuple(params)
    print(params)
    cursorObj.execute('SELECT * FROM settings WHERE username = ?', (username,))
    row = cursorObj.fetchone()
    if row is None:
        cursorObj.execute('INSERT INTO settings VALUES (?, ?, ?, ?, ?, ?, ?, ?)', params)
    else:
        params = list(config.values())
        params.append(username)
        params = tuple(params)
        print(params)
        cursorObj.execute('UPDATE settings SET width = ?, height = ?, font_color = ?, min_lat = ?, max_lat = ?,'
                               'min_lon = ?, max_lon = ? WHERE username = ?', params)
    con.commit()
cnx.close()
con.close()
