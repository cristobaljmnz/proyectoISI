"""
Created on Thu May 16 12:13:20 2024

@author: cristobaljimenez_
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from claseVuelo import Vuelo

            

class Scraping:
    def __init__(self, aeropuerto_ida, aeropuerto_vuelta, fecha_ida, fecha_vuelta):
        self.aeropuerto_ida = aeropuerto_ida
        self.aeropuerto_vuelta = aeropuerto_vuelta
        self.fecha_ida = fecha_ida
        self.fecha_vuelta = fecha_vuelta
        self.listaVuelos = []

    def buscar(self):
        service = Service('skyscrapper/drivers/chromedriver')
        service.start()
        # Inicializa las opciones de Chrome
        options = Options()
        options.add_argument('--headless')  # Ejecuta Chrome en modo headless, si lo deseas
        
        # Pasa las opciones al constructor de Remote
        driver = webdriver.Remote(service.service_url, options=options)
        
        
        url = f"https://www.vuelosbaratos.es/Buscar/{self.aeropuerto_ida}-{self.aeropuerto_vuelta}/{self.fecha_ida}/{self.fecha_vuelta}/ES/"
        driver.get(url)
        
        # time.sleep(0.5)
        # Espera a que los filtros de escalas estén visibles y haz clic en ellos
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'stopsFilter')))
            # print("Filters loaded.")
            
            # Usar JavaScript para hacer clic en los elementos
            driver.execute_script("document.getElementById('chk1Stop').click();")
            # print("Checkbox 1 clicked.")
            time.sleep(1)
            driver.execute_script("document.getElementById('chk2Stop').click();")
            # print("Checkboxes clicked.")
            
        except TimeoutException:
            # print("Timeout while waiting for filters to load.")
            driver.quit()
            service.stop()
            return []
        # Espera a que se carguen los datos dinámicamente (puedes ajustar el tiempo según sea necesario)
        time.sleep(2)

        entradas = driver.find_elements(By.CLASS_NAME, 'boxBody')

        # print("\nCantidad de vuelos encontrados:", len(entradas))
        # Obtener el tiempo y el número de escalas para la ida
        
        
        contador = 0
        for elem in entradas:
            precio_texto = elem.find_element(By.CLASS_NAME, 'priceBig').text.strip()
            precio = int(precio_texto.replace('.', ''))

            url = elem.find_element(By.CLASS_NAME, 'ResultPrice').get_attribute('href')

            portal = elem.find_element(By.CLASS_NAME, 'operatorName').text.strip()
            
            detalles = elem.find_elements(By.CLASS_NAME, 'groupDetailsCell')
            aeropuerto_ida = detalles[0].find_element(By.CLASS_NAME, 'groupApt').text.strip()
            fecha_hora_ida = detalles[0].find_element(By.CLASS_NAME, 'groupDate').text.strip()
            fecha_ida, hora_ida = fecha_hora_ida.split(', ')
            
            aeropuerto_ida_llegada = detalles[1].find_element(By.CLASS_NAME, 'groupApt').text.strip()
            fecha_hora_ida_llegada = detalles[1].find_element(By.CLASS_NAME, 'groupDate').text.strip()
            fecha_ida_llegada, hora_ida_llegada = fecha_hora_ida_llegada.split(', ')
            
            
            aeropuerto_vuelta=detalles[2].find_element(By.CLASS_NAME, 'groupApt').text.strip()
            fecha_hora_vuelta=detalles[2].find_element(By.CLASS_NAME, 'groupDate').text.strip()
            fecha_vuelta, hora_vuelta = fecha_hora_vuelta.split(', ')

            aeropuerto_vuelta_llegada=detalles[3].find_element(By.CLASS_NAME, 'groupApt').text.strip()
            fecha_hora_vuelta_llegada=detalles[3].find_element(By.CLASS_NAME, 'groupDate').text.strip()
            fecha_vuelta_llegada, hora_vuelta_llegada = fecha_hora_vuelta_llegada.split(', ')

            
            # Obtener el tiempo y el número de escalas para la ida
            # tiempo = elem.find_elements(By.XPATH, '//td[@align="center" and @valign="middle" and @class="groupDivider"]')
            
            # # print(len(tiempo))
            # # Obtener el tiempo y el número de escalas para la ida
            # tiempos_ida = elem.find_elements(By.XPATH, '//td[@align="center" and @valign="middle" and @width="70"]')
            # # for tiempo in tiempos_ida:
            # #     print(tiempo.text.strip())
            # tiempo_ida = tiempos_ida.text.strip()        
            # # Obtener el tiempo y el número de escalas para la vuelta
            # tiempos_vuelta = elem.find_elements(By.XPATH, '//td[@align="center" and @valign="middle" and contains(text(), "escala")]')
            # # for tiempo in tiempos_vuelta:
            # #     print(tiempo.text.strip())
            # tiempo_vuelta = tiempos_vuelta.text.strip()
            
            # # Obtener el tiempo y el número de escalas para la vuelta
            # tiempo_vuelta = elem.find_element(By.XPATH, '//td[@valign="middle"]').text.strip()
            
            # tiempo_vuelta, escalas_vuelta = info_vuelta.split('<br>')
            
            # //*[@id="result1OUT_476b2432"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]
            # //*[@id="result1OUT_b9ee540d"]/div[1]/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[4]
            # //*[@id="result1OUT_601b0cc0"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]
            # //*[@id="result1OUT_bdc1e6"]/div[1]/div/div[2]/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[4]
            
            
            vuelo = Vuelo(precio, url, portal, aeropuerto_ida, fecha_ida, hora_ida, fecha_ida_llegada, hora_ida_llegada, aeropuerto_vuelta, fecha_vuelta, hora_vuelta, fecha_vuelta_llegada, hora_vuelta_llegada) #tiempo_ida, tiempo_vuelta
            contador = contador +1
            self.listaVuelos.append(vuelo)

        driver.quit()
        service.stop()

        return self.listaVuelos

# Lista de proxies
PROXIES = [
    "http://ip1:port1",
    "http://ip2:port2",
    # Agrega más proxies aquí
]