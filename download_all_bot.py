from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

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