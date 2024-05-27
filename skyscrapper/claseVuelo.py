#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 20:34:48 2024

@author: cristobaljimenez_
"""

class Vuelo:
    # vuelos = []
    def __init__(self, precio, url, portal, aeropuerto_ida, fecha_ida, hora_ida, fecha_ida_llegada, hora_ida_llegada, aeropuerto_vuelta, fecha_vuelta, hora_vuelta, fecha_vuelta_llegada, hora_vuelta_llegada): #tiempo_ida, tiempo_vuelta
        self.precio = precio
        self.url = url
        self.portal = portal
        self.aeropuerto_ida = aeropuerto_ida
        self.fecha_ida = fecha_ida
        self.fecha_ida_llegada=fecha_ida_llegada
        self.aeropuerto_vuelta = aeropuerto_vuelta
        self.fecha_vuelta = fecha_vuelta
        self.fecha_vuelta_llegada=fecha_vuelta_llegada
        self.hora_ida = hora_ida
        self.hora_ida_llegada = hora_ida_llegada
        self.hora_vuelta = hora_vuelta
        self.hora_vuelta_llegada = hora_vuelta_llegada
        # self.tiempo_ida = tiempo_ida
        # self.tiempo_vuelta = tiempo_vuelta
        
        # Vuelo.vuelos.append(self)
    
    def __str__(self):
        return f"Nombre: {self.aeropuerto_ida} a {self.aeropuerto_vuelta}\n" \
               f"Precio: {self.precio}\n" \
               f"Portal: {self.portal}\n" \
               f"Fecha ida: {self.fecha_ida}\n" \
               f"Hora ida: {self.hora_ida}\n" \
               f"Fecha ida llegada: {self.fecha_ida_llegada}\n" \
               f"Hora ida llegada: {self.hora_ida_llegada}\n" \
               f"Fecha vuelta: {self.fecha_vuelta}\n" \
               f"Hora vuelta: {self.hora_vuelta}\n" \
               f"Fecha vuelta llegada: {self.fecha_vuelta_llegada}\n" \
               f"Hora vuelta llegada: {self.hora_vuelta_llegada}\n" \
               f"URL: {self.url}\n" \
               f"-------------------------------"
               
    # @staticmethod
    # def agregar_vuelos(array_vuelos):
    #     Vuelo.vuelos.extend(array_vuelos)
        
    # @staticmethod
    # def clear_vuelo():
    #     Vuelo.vuelos.clear()