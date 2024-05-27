import requests
import os
from claseVuelo import Vuelo
from datetime import datetime


TEQUILA_API_KEY = "WeTXeXOzGhS7ewmf83hb0Rbb5C-DRHYz"  # Your TEQUILA_API_KEY
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"  # Your TEQUILA_ENDPOINT

def transformar_fecha(fecha_str):
    # Diccionario de meses en espaÃ±ol
    meses_espanol = {
        1: 'ene', 2: 'feb', 3: 'mar', 4: 'abr', 5: 'may', 6: 'jun',
        7: 'jul', 8: 'ago', 9: 'sep', 10: 'oct', 11: 'nov', 12: 'dic'
    }
    
    # Convertir el string de fecha a un objeto datetime
    fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
    
    # Formatear la fecha en el nuevo formato
    dia = fecha.day
    mes = meses_espanol[fecha.month]
    anio = fecha.year
    
    # Devolver la fecha formateada
    return f"{dia} {mes}. {anio}"


class FlightSearchKiwi:
    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, ret_from_time, ret_to_time):
        """ This function checks for the available flights through a get() request """
        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "return_from": ret_from_time,
            "return_to":  ret_to_time,
            "max_stopovers": 0,
            "curr": "EUR"
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}",  # search es el endpoint de SEARCH API
            headers=headers,
            params=query,
        )

        vuelos = []
        try:
            data = response.json()["data"]
            for flight_data in data:
                precio = flight_data["price"]
                url = flight_data["deep_link"]
                portal = "Kiwi"
                aeropuerto_ida = flight_data["route"][0]["flyFrom"]
                
                # fecha_ida = flight_data["route"][0]["local_departure"].split("T")[0]
                # fecha_ida_llegada = flight_data["route"][0]["local_arrival"].split("T")[0]
                # fecha_ida = flight_data["route"][0]["local_departure"]
                # fecha_ida_llegada = flight_data["route"][0]["local_arrival"]
                
                # aeropuerto_vuelta = flight_data["route"][1]["flyFrom"]
                
                # fecha_vuelta = flight_data["route"][1]["local_departure"].split("T")[0]
                # fecha_vuelta_llegada = flight_data["route"][1]["local_arrival"].split("T")[0]
                # fecha_vuelta = flight_data["route"][1]["local_departure"]
                # fecha_vuelta_llegada = flight_data["route"][1]["local_arrival"]
                
                fecha_ida = transformar_fecha(flight_data["route"][0]["local_departure"].split("T")[0])
                hora_ida_aux = flight_data["route"][0]["local_departure"].split("T")[1]
                hora_ida_aux2 = hora_ida_aux.split(":")[:2]
                hora_ida = ":".join(hora_ida_aux2)
                
                fecha_ida_llegada = transformar_fecha(flight_data["route"][0]["local_arrival"].split("T")[0])
                hora_ida_llegada_aux = flight_data["route"][0]["local_arrival"].split("T")[1]
                hora_ida_llegada_aux2 = hora_ida_llegada_aux.split(":")[:2]
                hora_ida_llegada = ":".join(hora_ida_llegada_aux2)
                
                aeropuerto_vuelta = flight_data["route"][1]["flyFrom"]
                
                fecha_vuelta = transformar_fecha(flight_data["route"][1]["local_departure"].split("T")[0])
                hora_vuelta_aux = flight_data["route"][1]["local_departure"].split("T")[1]
                hora_vuelta_aux2 = hora_vuelta_aux.split(":")[:2]
                hora_vuelta = ":".join(hora_vuelta_aux2)
                
                fecha_vuelta_llegada = transformar_fecha(flight_data["route"][1]["local_arrival"].split("T")[0])
                hora_vuelta_llegada_aux = flight_data["route"][1]["local_arrival"].split("T")[1]
                hora_vuelta_llegada_aux2 = hora_vuelta_llegada_aux.split(":")[:2]
                hora_vuelta_llegada = ":".join(hora_vuelta_llegada_aux2)
                
                
                vuelo = Vuelo(precio, url, portal, aeropuerto_ida, fecha_ida, hora_ida, fecha_ida_llegada, hora_ida_llegada, aeropuerto_vuelta, fecha_vuelta, hora_vuelta, fecha_vuelta_llegada, hora_vuelta_llegada) #tiempo_ida, tiempo_vuelta
                vuelos.append(vuelo)
                
                
                # fecha_ida = itineraries["legs"][0]["departure"].split("T")[0]
                # hora_ida_aux = itineraries["legs"][0]["departure"].split("T")[1]
                # hora_ida_aux2 = hora_ida_aux.split(":")[:2]
                # hora_ida = ":".join(hora_ida_aux2)
                # fecha_ida_llegada = itineraries["legs"][0]["arrival"].split("T")[0]
                # hora_ida_llegada_aux = itineraries["legs"][0]["arrival"].split("T")[1]
                # hora_ida_llegada_aux2 = hora_ida_llegada_aux.split(":")[:2]
                # hora_ida_llegada = ":".join(hora_ida_llegada_aux2)
                # aeropuerto_vuelta = itineraries["legs"][1]["origin"]["id"]
                # fecha_vuelta = itineraries["legs"][1]["departure"].split("T")[0]
                # hora_vuelta_aux = itineraries["legs"][1]["departure"].split("T")[1]
                # hora_vuelta_aux2 = hora_vuelta_aux.split(":")[:2]
                # hora_vuelta = ":".join(hora_vuelta_aux2)
                # fecha_vuelta_llegada = itineraries["legs"][1]["arrival"].split("T")[0]
                # hora_vuelta_llegada_aux = itineraries["legs"][1]["arrival"].split("T")[1]
                # hora_vuelta_llegada_aux2 = hora_vuelta_llegada_aux.split(":")[:2]
                # hora_vuelta_llegada = ":".join(hora_vuelta_llegada_aux2)


                
        except IndexError:
            pass

        return vuelos

# Ejemplo de uso
if __name__ == "__main__":
    flight_search = FlightSearchKiwi()
    origin_city_code = "AGP"
    destination_city_code = "PMI"
    from_time = "26/05/2024"
    to_time = "26/05/2024"
    ret_from_time = "31/05/2024"
    ret_to_time = "31/05/2024"

    vuelos = flight_search.check_flights(origin_city_code, destination_city_code, from_time, to_time, ret_from_time, ret_to_time)
    if vuelos:
        for vuelo in vuelos:
            print(vuelo)
    else:
        print("No se encontraron vuelos.")
        
        
        
# import requests
# import os
# from claseVuelo import Vuelo,imprimirResultados

# TEQUILA_API_KEY = "WeTXeXOzGhS7ewmf83hb0Rbb5C-DRHYz" #Your TEQUILA_API_KEY
# TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com" #Your TEQUILA_ENDPOINT

# class FlightData:
#     def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, stop_overs=0, via_city=""):
#         self.price = price
#         self.origin_city = origin_city
#         self.origin_airport = origin_airport
#         self.destination_city = destination_city
#         self.destination_airport = destination_airport
#         self.out_date = out_date
#         self.return_date = return_date
#         self.stop_overs = stop_overs
#         self.via_city = via_city
        
# class FlightSearch:
#     # def get_destination_code(self, city_name):
#     #     """ This function get the city IATA code of a flight """
#     #     location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
#     #     headers = {"apikey": TEQUILA_API_KEY}
#     #     query = {"term": city_name, "location_types": "city"}
#     #     response = requests.get(url=location_endpoint, headers=headers, params=query)
#     #     results = response.json()["locations"]
#     #     code = results[0]["code"]
#     #     return code

#     def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, ret_from_time, ret_to_time):
#         """ This function checks for the available flights throught a get() request """
#         headers = {"apikey": TEQUILA_API_KEY}
#         query = {
#             "fly_from": origin_city_code,
#             "fly_to": destination_city_code,
#             "date_from": from_time,
#             "date_to": to_time,
#             "return_from": ret_from_time,
#             "return_to":  ret_to_time,
#             "curr": "EUR"
#         }

#         response = requests.get(
#             url=f"{TEQUILA_ENDPOINT}/v2/search", #search es el endpoint de SEARCH API
#             headers=headers,
#             params=query,
#         )
        
#         # Imprimir el JSON de la respuesta
#         # print(response.json())

#         try:
#             data = response.json()["data"][0]
#         # except IndexError:
#             # # Makes the call again adding a stop over to the query
#             # query["max_stopovers"] = 0
#             # response = requests.get(
#             #     url=f"{TEQUILA_ENDPOINT}/v2/search",
#             #     headers=headers,
#             #     params=query,
#             # )
#             # try:
#             #     data = response.json()["data"][0]
#             # except IndexError:
#             #     return None
#             # else:
#             #     # FlightData instance with stop_overs and via_city
#             #     flight_data = FlightData(
#             #         price=data["price"],
#             #         origin_airport=data["route"][0]["flyFrom"],
#             #         destination_airport=data["route"][1]["flyTo"],
                    
#             #         out_date=data["route"][0]["local_departure"].split("T")[0],
#             #         return_date=data["route"][1]["local_departure"].split("T")[0],
#             #         stop_overs=3,
#             #         via_city=data["route"][0]["cityTo"]
#             #         # deep_link
#             #         # local_arrival	string
#             #         # Time of arrival in ISO timestamp format.
                    
#             #         # local_departure	string
#             #         # Time of departure in ISO timestamp format.
                    
#             #         # flyTo	string
#             #         # IATA code identifier of the destination airport.
                    
#             #         # flyFrom	string
#             #         # IATA code identifier of the origin airport.

#             #     )
#             #     print(f"{flight_data.destination_city}: â‚¬{flight_data.price}")
#             #     return flight_data
#         # else:
#             # FlightData instance without stop_overs and via_city
#             precio=data["price"]
#             url = data["route"][0]["flyFrom"]
#             portal = "Kiwi"
#             aeropuerto_ida=data["deep_link"]
#             fecha_ida=data["route"][0]["local_departure"].split("T")[0]
#             fecha_ida_llegada=data["route"][0]["local_arrival"].split("T")[0]
#             aeropuerto_vuelta=data["route"][1]["flyFrom"]
#             fecha_vuelta=data["route"][1]["local_departure"].split("T")[0]
#             fecha_vuelta_llegada=data["route"][1]["local_arrival"].split("T")[0]
            
#             vuelo = Vuelo(precio, url, portal, aeropuerto_ida, fecha_ida, fecha_ida_llegada, aeropuerto_vuelta, fecha_vuelta, fecha_vuelta_llegada)
            
#             # flight_data = FlightData(
#             #     precio=data["price"],
                
#             #     aeropuerto_ida=data["route"][0]["flyFrom"],
#             #     aeropuerto_vuelta=data["route"][1]["flyFrom"],
#             #     fecha_ida=data["route"][0]["local_departure"].split("T")[0],
#             #     fecha_ida_llegada=data["route"][0]["local_arrival"].split("T")[0],
#             #     fecha_vuelta=data["route"][1]["local_departure"].split("T")[0],
#             #     fecha_vuelta_llegada=data["route"][1]["local_arrival"].split("T")[0],
                
#             #     # deep_link
#             #     #         # local_arrival	string
#             #     #         # Time of arrival in ISO timestamp format.
                        
#             #     #         # local_departure	string
#             #     #         # Time of departure in ISO timestamp format.
                        
#             #     #         # flyTo	string
#             #     #         # IATA code identifier of the destination airport.
                        
#             #     #         # flyFrom	string
#             #     #         # IATA code identifier of the origin airport.

#             # )
#             # print(f"{flight_data.destination_city}: â‚¬{flight_data.price}")
#             return flight_data


# # Ejemplo de uso
# if __name__ == "__main__":
#     flight_search = FlightSearch()
#     # from datetime import datetime

#     origin_city_code = "AGP"
#     destination_city_code = "PMI"
#     from_time = "26/05/2024"
#     to_time = "26/05/2024"
#     ret_from_time ="31/05/2024"
#     ret_to_time = "31/05/2024"

#     flight_search.check_flights(origin_city_code, destination_city_code, from_time, to_time, ret_from_time, ret_to_time)
    