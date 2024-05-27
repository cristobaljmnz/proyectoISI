"""
Created on Sat May 18 21:26:45 2024

@author: cristobaljimenez_
"""

from flask import Flask, render_template, request
from claseVuelo import Vuelo
from APIkiwi import FlightSearchKiwi
from APISS import FlightSearchSS
from webscraping import Scraping
from datetime import datetime

app = Flask(__name__)

def convertir_formato_fecha(fecha):
    if fecha != "":
        # Convertir el string de fecha al formato datetime
        fecha_datetime = datetime.strptime(fecha, '%d/%m/%Y')
        # Formatear la fecha en el nuevo formato "YYYY-mm-dd"
        fecha_nueva_formato = fecha_datetime.strftime('%Y-%m-%d')
        return fecha_nueva_formato

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/buscar', methods=['POST'])
def buscar_vuelos():
    todos_vuelos = []
    
    
    aeropuerto_ida = request.form.get('aeropuerto_ida')
    aeropuerto_vuelta = request.form.get('aeropuerto_vuelta')
    fecha_ida = request.form.get('fecha_ida')
    fecha_vuelta =  request.form.get('fecha_vuelta')
    
    # aeropuerto_ida = "AGP"  
    # aeropuerto_vuelta = "PMI"  
    # fecha_ida = "26/05/2024"  
    # fecha_vuelta = "31/05/2024"  

    fecha_ida_nueva_formato = convertir_formato_fecha(fecha_ida)
    fecha_vuelta_nueva_formato = convertir_formato_fecha(fecha_vuelta)
    
    # API KIWI
    flight_search_kiwi = FlightSearchKiwi()
    vuelos = flight_search_kiwi.check_flights(aeropuerto_ida,aeropuerto_vuelta,fecha_ida,fecha_ida,fecha_vuelta,fecha_vuelta)
     # todos_vuelos.agregar_vuelos(vuelos)
    for vuelo in vuelos:
        todos_vuelos.append(vuelo)
    
   
    #scraping de vuelosbaratos.es
    
    scraping = Scraping(aeropuerto_ida,aeropuerto_vuelta,fecha_ida_nueva_formato,fecha_vuelta_nueva_formato)
    vuelos = scraping.buscar()
    for vuelo in vuelos:
        todos_vuelos.append(vuelo)
    
    
    
    #API rapid (SkyScanner)
    flight_search_SS = FlightSearchSS()
    vuelos_SS = flight_search_SS.check_flights(aeropuerto_ida,aeropuerto_vuelta,fecha_ida_nueva_formato,fecha_vuelta_nueva_formato)
    
    for vuelo in vuelos_SS:
        todos_vuelos.append(vuelo)


    for vuelo in todos_vuelos:
        try:
            print(vuelo)
            vuelo.precio = float(vuelo.precio)
        except ValueError:
            vuelo.precio = float('inf')  
    
    print(len(todos_vuelos))
    
    # Ordenar vuelos por precio descendiente
    todos_vuelos.sort(key=lambda vuelo: vuelo.precio)
    
    
    #Seleparar el vuelo más barato del resto
    top_vuelos = todos_vuelos[:1]
    demas_vuelos = todos_vuelos[1:]

    return render_template('index.html', top_vuelos=top_vuelos, demas_vuelos=demas_vuelos)

    

if __name__ == '__main__':
    app.run(debug=True, port=8888)
    # buscar_vuelos()