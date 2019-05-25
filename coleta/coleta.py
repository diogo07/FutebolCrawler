from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Coleta:
    def __init__(self, driver, navegador):
        if(navegador == "chrome"):
            self.wd = webdriver.Chrome(driver)
        if (navegador == "firefox"):
            self.wd = webdriver.Firefox(driver)
        if (navegador == "safari"):
            self.wd = webdriver.Safari(driver)
        if (navegador == "edge"):
            self.wd = webdriver.Edge(driver)

    def buscar_html_dinamico(self, url, tempo_espera, filtro_busca):
        self.wd.get(url)
        try:
            WebDriverWait(self.wd, tempo_espera).until(
                EC.element_to_be_clickable((By.XPATH, filtro_busca)))
        except TimeoutError:
            self.wd.quit()
            print("Erro: tempo esgotado")
            return 0

        html = self.wd.page_source

        divs = self.wd.find_elements_by_class_name('expand')


        for div in divs:
            div.click()

        html = self.wd.page_source
        self.wd.quit()
        return html


    def buscar_html_dinamico_por_data(self, url, tempo_espera, filtro_busca, dias):
        self.wd.get(url)

        import time
        time.sleep(5)

        if dias > 7:
            for i in range(7):
                bt_proximo_dia = self.wd.find_element_by_xpath('//*[@id="live-table"]/div[2]/div/div[3]/div')
                bt_proximo_dia.click()
                time.sleep(5)
        else:
            for i in range(dias):
                bt_proximo_dia = self.wd.find_element_by_xpath('//*[@id="live-table"]/div[2]/div/div[3]/div')
                bt_proximo_dia.click()
                time.sleep(5)
        try:
            WebDriverWait(self.wd, tempo_espera).until(
                EC.element_to_be_clickable((By.XPATH, filtro_busca)))
        except TimeoutError:
            self.wd.quit()
            print("Erro: tempo esgotado")
            return 0

        divs = self.wd.find_elements_by_class_name('event__header--no-my-games')

        for div in divs:
            bt = div.find_elements_by_class_name('expand')
            bt[0].click()

        html = self.wd.page_source
        self.wd.quit()
        return html

