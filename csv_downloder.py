from tkinter import *
from tkinter import ttk, filedialog
import configparser
from functools import partial
from tkcalendar import DateEntry
import pandas as pd
import os, fnmatch
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

initfile = os.path.join(base_path,"config.txt")

print(initfile)

def trsformDate(date):
    ptr = [" ", "ene", "feb", "mar","abr", "may","jun","jul","ago","sep","oct","nov","dic"]
    aux = date.split('/',2)
    aux[1] = ptr[int(aux[1])]
    aux1 = " ".join(aux)
    return aux1


def download_csv(*login):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.set_window_position(-100000,-1000000)
    browser.get('https://clinical-connect.lumiradx.com/')
    browser.find_element_by_class_name(
        'input__TextInput--25xpW').send_keys(login[0][0])
    browser.find_element_by_class_name('AccessCode__Validate--3ohJw').click()

    browser.implicitly_wait(3)
    browser.find_element_by_id('username').send_keys(login[0][1])
    browser.find_element_by_id('password').send_keys(login[0][2])
    browser.find_element_by_id('login-button').click()
    browser.implicitly_wait(3)
    browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div/div/section[2]/a[2]').click()

    resultSet = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div/div[2]/ul')
    options = resultSet.find_elements_by_tag_name("li")

    for option in options:
        i = 0
        option.click()
        date = browser.find_element_by_xpath('//*[@id="overlays"]/div/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/input')
        while(i < 12):
            date.send_keys(Keys.BACK_SPACE)
            i+=1
        date.send_keys(trsformDate(login[0][3]))
        browser.find_element_by_xpath('/html/body').click()
        browser.find_element_by_xpath('//*[@id="overlays"]/div/div/div/div/div/div/div/div[1]/div[2]/div[2]/button').click()
        browser.implicitly_wait(7)
        browser.find_element_by_xpath('//*[@id="overlays"]/div[2]/div/div/div[3]/button[2]').click()
        browser.find_element_by_xpath('//*[@id="overlays"]/div/div/div/header/button').click()
    browser.close()

def find(pattern, path):
    result = []
    if(os.path.exists("combined_csv.csv")):
        result.append("combined_csv.csv")
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def joincsv(downloads_path,output_path):
    output_path = output_path + "/combined_csv.csv"
    paths = find('results*.csv', downloads_path)
    out = 0
    if(paths):
        #combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in paths]).drop_duplicates(keep='first')
        #export to csv
        combined_csv.to_csv( output_path, index=False, encoding='utf-8-sig')
        for f in paths:
            if(f != output_path):
                os.remove(f)
            else:
                out = 1
    if(out == 1):  
        print("Nothing to import")



def search_path(label1str):
    path = filedialog.askdirectory()
    config = configparser.ConfigParser()
    config.read((initfile))
    config.set('SECTION_PATHS', 'download_path', str(path))
    label1str.set(path)
    with open(initfile, "w+") as configfile:
        config.write(configfile)


def output_path(label2str):
    path = filedialog.askdirectory()
    config = configparser.ConfigParser()
    config.read((initfile))
    config.set('SECTION_PATHS', 'output_path', str(path))
    label2str.set(path)
    with open(initfile, "w+") as configfile:
        config.write(configfile)


def submit(cond, *login):
    config = configparser.ConfigParser()
    config.read((initfile))
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
    config.read((initfile))
    code = config.get('login', 'code')
    user = config.get('login', 'user')
    password = config.get('login', 'password')
    date = config.get('login', 'date')
    return [code, user, password, date]


def set_login_config(*login):
    config = configparser.ConfigParser()
    config.read((initfile))
    config.set('login', 'code', login[0][0][0])
    config.set('login', 'user', login[0][0][1])
    config.set('login', 'password', login[0][0][2])
    config.set('login', 'date', login[0][0][3])
    with open(initfile, "w+") as configfile:
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
        config.read((initfile))
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
