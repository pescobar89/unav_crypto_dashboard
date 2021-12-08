import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt


class Wrangler:
    
    def __init__(self):
        pass
    
    @st.cache
    def get_clean_data(self, raw_data):
        clean_data = {}
        # Iteramos sobre los pares en raw_data y consolidamos un dataframe
        for k, v in raw_data.items():
            pair_data = pd.concat([x['trades'] for x in v])
            pair_data = pair_data.drop_duplicates()
            pair_data = pair_data[['dtime', 'time', 'price', 'volume']]
            pair_data = pair_data.sort_values('time', ascending=False)
            clean_data[k] = pair_data
        return(clean_data)


class Calculator:
    
    def __init__(self, data):
        self.data = {}
        self.data['original'] = data

    def compute_price(self, price='price', volume='volume', time=['dtime', 'time']):
        price_data = self.data['original'].copy()
        # Calculamos precio por volumen
        price_data[price+'_x_'+volume] = price_data[price]*price_data[volume]
        # Agregamos
        pxv = price+'_x_'+volume
        d = {volume: np.sum, pxv: np.sum}
        price_data = price_data.groupby(time).agg(d)
        # Recalculamos el precio
        price_data[price] = price_data[pxv]/price_data[volume]
        # Seleccionamos las variables
        price_data = price_data[[price, volume]].reset_index()
        # Guardamos
        self.data['price'] = price_data       
  
    def compute_vwap(self, price='price', volume='volume', time=['dtime', 'time'], minutes_interval=15):
        vwap_data = self.data['original'].copy()
        # Generamos los bins
        seconds = minutes_interval*60
        min_period = int(np.floor(min(vwap_data['time']/seconds))*seconds-seconds)
        max_period = int(np.ceil(max(vwap_data['time']/seconds))*seconds+seconds)
        bins = list(range(min_period, max_period, seconds))
        vwap_data['new_time'] = pd.cut(vwap_data[time[1]], bins=bins)
        # Calculamos precio por volumen
        vwap_data[price+'_x_'+volume] = vwap_data[price]*vwap_data[volume]
        # Agregamos
        pxv = price+'_x_'+volume
        d = {volume: np.sum, pxv: np.sum}
        vwap_data = vwap_data.groupby('new_time').agg(d)
        # Recalculamos el precio
        vwap_data[price] = vwap_data[pxv]/vwap_data[volume]
        # Reteamos indice y eliminamos nas
        vwap_data = vwap_data[[price, volume]].reset_index()
        # Formateamos la fecha
        vwap_data['time'] = [int(x[-11:-1]) for x in vwap_data['new_time'].astype(str)]
        vwap_data['dtime'] = [dt.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') for x in vwap_data['time']]
        # Aseguramos el orden por fecha 
        vwap_data = vwap_data.sort_values('time', ascending=True)
        # Rellenamos los precios vacios
        vwap_data['price'] = vwap_data['price'].fillna(method='ffill')
        vwap_data['price'] = vwap_data['price'].fillna(method='bfill')
        # Ordenamos variables
        vwap_data = vwap_data[time+[price, volume]]
        # Guardamos
        self.data['vwap'] = vwap_data
