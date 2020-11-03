from tkinter import *
from tkinter import ttk, filedialog
from csv_to_xcel import joincsv
import configparser
from functools import partial
from download_all_bot import download_csv
from tkcalendar import DateEntry


def search_path(label1str):
    path = filedialog.askdirectory()
    config = configparser.ConfigParser()
    config.read(('config.txt'))
    config.set('SECTION_PATHS', 'download_path', str(path))
    label1str.set(path)
    with open("config.txt", "w+") as configfile:
        config.write(configfile)


def output_path(label2str):
    path = filedialog.askdirectory()
    config = configparser.ConfigParser()
    config.read(('config.txt'))
    config.set('SECTION_PATHS', 'output_path', str(path))
    label2str.set(path)
    with open("config.txt", "w+") as configfile:
        config.write(configfile)


def submit(cond, *login):
    config = configparser.ConfigParser()
    config.read(('config.txt'))
    set_login_config(login)
    if(cond == 1):
        download_csv(login[0])
    joincsv(config.get('SECTION_PATHS', 'download_path'),
            config.get('SECTION_PATHS', 'output_path'))


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def get_login_config():
    config = configparser.ConfigParser()
    config.read(('config.txt'))
    code = config.get('login', 'code')
    user = config.get('login', 'user')
    password = config.get('login', 'password')
    date = config.get('login', 'date')
    return [code, user, password, date]


def set_login_config(*login):
    config = configparser.ConfigParser()
    config.read(('config.txt'))
    config.set('login', 'code', login[0][0][0])
    config.set('login', 'user', login[0][0][1])
    config.set('login', 'password', login[0][0][2])
    config.set('login', 'date', login[0][0][3])
    with open("config.txt", "w+") as configfile:
        config.write(configfile)

checkVar = 1 

class Aplicacion():
    def __init__(self):

        def frame_state(frame):
            global checkVar
            if(checkVar == 1):
                for child in frame.winfo_children():
                    child.configure(state='disable')
                checkVar = 0
            else:
                for child in frame.winfo_children():
                    child.configure(state='normal')
                checkVar = 1
        raiz = Tk()
        raiz.geometry('780x300')
        raiz.configure(bg=_from_rgb((67, 151, 209)))
        raiz.title('CsvDownloader')
        config = configparser.ConfigParser()
        config.read(('config.txt'))
        frameBottom = Frame(raiz, width=100, height=130, bg='green')
        frameTopLeft = Frame(raiz, width=200, height=250, bg='white')
        frameTopRigth = Frame(raiz, width=400, height=350, bg='white')
        checkbutton = Checkbutton(raiz, text="Enable download", bg=_from_rgb(
            (67, 151, 209)),  command=partial(frame_state, frameTopLeft))
        checkbutton.select()
        checkbutton.grid(row=0, sticky=W, padx=20, pady=10)
        frameTopLeft.grid(row=1, sticky=W, padx=20,
                          pady=10, ipadx=10, ipady=10)
        frameTopRigth.grid(row=1, column=1, padx=30, pady=25, sticky=N)
        frameBottom.grid(row=2, column=1, padx=30, sticky=E)
        login = []
        label1str = StringVar()
        label2str = StringVar()
        login = get_login_config()
        Label(frameTopLeft, text="Code:").grid(
            row=0, column=0, sticky=W, pady=13)
        Label(frameTopLeft, text="User:").grid(
            row=1, column=0, sticky=W, pady=8)
        Label(frameTopLeft, text="Password:").grid(
            row=2, column=0, sticky=W, pady=13)
        Label(frameTopLeft, text="Date:").grid(
            row=3, column=0, sticky=W, pady=13)
        codeEntry = Entry(frameTopLeft)
        userEntry = Entry(frameTopLeft)
        passEntry = Entry(frameTopLeft)
        dateEntry = DateEntry(frameTopLeft)
        codeEntry.grid(row=0, column=1)
        userEntry.grid(row=1, column=1)
        passEntry.grid(row=2, column=1)
        dateEntry.grid(row=3, column=1)
        codeEntry.insert(0, login[0])
        userEntry.insert(0, login[1])
        passEntry.insert(0, login[2])
        dateEntry.set_date(login[3])

        def get_entry():
            global checkVar
            stra = [" ", " ", " ", " "]
            stra[0] = codeEntry.get()
            stra[1] = userEntry.get()
            stra[2] = passEntry.get()
            stra[3] = dateEntry.get()
            submit(checkVar, stra)
        label1 = Label(frameTopRigth, textvariable=label1str)
        label2 = Label(frameTopRigth, textvariable=label2str)
        label1str.set(config.get('SECTION_PATHS', 'download_path'))
        label2str.set(config.get('SECTION_PATHS', 'output_path'))
        label1.grid(row=0, sticky=W)
        label2.grid(row=1, sticky=W)
        ttk.Button(frameTopRigth, text='Seleccionar Carpeta Descargas',
                   command=partial(search_path, label1str)).grid(row=0, column=1)
        ttk.Button(frameTopRigth, text='Seleccionar Carpeta Destino',
                   command=partial(output_path, label2str)).grid(row=1, column=1)
        ttk.Button(frameBottom, text='Salir',
                   command=raiz.destroy).grid(row=0, column=0)
        ttk.Button(frameBottom, text='Descargar',
                   command=get_entry).grid(row=0, column=1)
        raiz.mainloop()


def main():
    mi_app = Aplicacion()
    return 0


if __name__ == '__main__':
    main()
