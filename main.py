import tkinter.ttk
from tkinter import *
from functools import partial
import psycopg2 as pg2
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
conn = pg2.connect(database="tkinter_login_db", user="postgres", password="")
cur = conn.cursor()

class App():
    def __init__(self):
        self.entries = []
        self.root = Tk()
        self.root.title("Register")
        self.root.geometry("1700x480")
        self.root.resizable(False, False)
        self.mainFrame = self.createMainFrame()
        self.c = self.createCanvas()
        self.draw()
        self.updateView()

    def draw(self):
        self.c.create_rectangle(20, 15, 380, 45, fill="#ffffff")
        self.c.create_text(200, 30, text="REGISTER PANEL", anchor="center", font=("Helvetica", "10", "bold"))
        self.c.create_text(200, 70, text="Name", anchor="center")
        self.name_entry = Entry(self.root, width=20, bd=2, justify=CENTER)
        self.name_entry.place(x=137, y=80)
        self.entries.append(self.name_entry)
        self.c.create_text(200, 120, text="Surname", anchor="center")
        self.sname_entry = Entry(self.root, width=20, bd=2, justify=CENTER)
        self.sname_entry.place(x=137, y=130)
        self.entries.append(self.sname_entry)
        self.c.create_text(200, 170, text="Email Address", anchor="center")
        self.mail_entry = Entry(self.root, width=33, bd=2, justify=CENTER)
        self.mail_entry.place(x=97, y=180)
        self.entries.append(self.mail_entry)
        self.c.create_text(200, 220, text="Username", anchor="center")
        self.user_entry = Entry(self.root, width=20, bd=2, justify=CENTER)
        self.user_entry.place(x=137, y=230)
        self.entries.append(self.user_entry)
        self.c.create_text(200, 270, text="Password", anchor="center")
        self.pass_entry = Entry(self.root, width=20, bd=2, show="*", justify=CENTER)
        self.pass_entry.place(x=137, y=280)
        self.entries.append(self.pass_entry)
        self.c.create_text(200, 320, text="Confirm password", anchor="center")
        self.ccpass_entry = Entry(self.root, width=20, bd=2, show="*", justify=CENTER)
        self.ccpass_entry.place(x=137, y=330)
        self.entries.append(self.ccpass_entry)

        append = Button(self.mainFrame, width=10, command=partial(self.register), text="Register", font=("Helvetica", "9", "bold"),
                        borderwidth=4)
        append.place(x=159, y=380)
        self.error = self.c.create_text(200, 450, text="", fill="#ff0000")
        self.c.create_line(400, 0, 400, 480)
        self.c.create_line(1300, 0, 1300, 480)

        self.view = tkinter.ttk.Treeview(self.root, columns=("2", "3", "4", "5", "6", "7"), height=21, selectmode="browse")
        self.view.place(x=420, y=15)
        self.view.heading("#0", text="user_id"); self.view.column("#0", width=50, anchor=CENTER)
        self.view.heading("2", text="user_name"); self.view.column("2", width=120, anchor=CENTER)
        self.view.heading("3", text="user_surname"); self.view.column("3", width=120, anchor=CENTER)
        self.view.heading("4", text="user_email"); self.view.column("4", width=200, anchor=CENTER)
        self.view.heading("5", text="user_username"); self.view.column("5", width=110, anchor=CENTER)
        self.view.heading("6", text="user_password"); self.view.column("6", width=110, anchor=CENTER)
        self.view.heading("7", text="user_created_on"); self.view.column("7", width=150, anchor=CENTER)

        self.c.create_rectangle(1320, 15, 1680, 45, fill="#ffffff")
        self.c.create_text(1500, 30, text="ACCOUNT MANAGEMENT", anchor="center", font=("Helvetica", "10", "bold"))
        self.c.create_text(1500, 80, text="Update", anchor="center")
        self.modify_selector = tkinter.ttk.Combobox(self.root, state="readonly")
        self.modify_selector["values"] = ("user_name", "user_surname", "user_email", "user_username", "user_password")
        self.modify_selector.place(x=1430, y=90)
        self.c.create_text(1390, 140, text="To:", anchor="center")
        self.modify_entry = Entry(self.root, width=30, bd=2, justify=CENTER)
        self.modify_entry.place(x=1407, y=130)
        self.modifybutton = Button(self.mainFrame, width=15, command=partial(self.modify), text="Accept", font=("Helvetica", "9", "bold"),
                        borderwidth=4)
        self.modifybutton.place(x=1442, y=170)

        self.c.create_line(1300, 240, 1700, 240)

    def modify(self):
        pass

    def updateView(self):
        self.view.delete(*self.view.get_children())
        data = []
        cur.execute("SELECT * FROM account")
        for i in cur.fetchall():
            data.append(i)

        for i in data:
            self.view.insert("", END, text=str(i[0]),
                             values=(str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6])))

    def register(self):
        for i in self.entries:
            if i.get() == "":
                self.c.itemconfig(self.error, fill="#ff0000", text="Fill all the required fields")
                return

        if not re.fullmatch(regex, self.mail_entry.get()):
            self.c.itemconfig(self.error, fill="#ff0000", text="Invalid email address")
            return

        if self.pass_entry.get() != self.ccpass_entry.get():
            self.c.itemconfig(self.error, fill="#ff0000", text="Make sure your passwords match")
            return

        name = self.entries[0].get(); surname = self.entries[1].get()
        mail = self.entries[2].get(); username = self.entries[3].get()
        password = self.entries[4].get()

        usernames = []
        mails = []
        cur.execute("SELECT user_username FROM account")
        for i in cur.fetchall():
            usernames.append(i)
        cur.execute("SELECT user_email FROM account")
        for i in cur.fetchall():
            mails.append(i)

        for i in mails:
            if i[0] == mail:
                self.c.itemconfig(self.error, fill="#ff0000", text="Email address already in use")
                return
        for i in usernames:
            if i[0] == username:
                self.c.itemconfig(self.error, fill="#ff0000", text="Username already in use")
                return

        cur.execute("INSERT INTO account(user_name, user_surname, user_email, user_username, user_password, user_created_on) "
                    f"VALUES('{name}', '{surname}', '{mail}', '{username}', '{password}', CURRENT_TIMESTAMP)")
        conn.commit()
        self.c.itemconfig(self.error, fill="#00b800", text="Your account has been successfully created")
        self.updateView()

    def createMainFrame(self):
        frame = Frame(self.root, bg="#ffffff")
        frame.pack(fill="both", expand="True")
        return frame

    def createCanvas(self):
        self.c = Canvas()
        c = Canvas(self.mainFrame, width=1300, height=480, bg="#e4deff")
        c.pack(fill="both", expand="True")
        return c

    def loop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.loop()

conn.close()
