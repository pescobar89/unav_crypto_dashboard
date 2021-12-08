import krakenex
from pykrakenapi import KrakenAPI
import numpy as np
import time
import streamlit as st


class Downloader:
    
    def __init__(self, API=KrakenAPI(krakenex.API())):
        self.API = API
        self.data = {}
    
    @st.cache
    def download_list_of_pairs(self):
        self.pairs = self.API.get_tradable_asset_pairs()[['altname', 'wsname', 'base', 'quote']]
    
    @st.cache
    def download_split_historic(self, pair, dt_from):
        # Obtenemos los 1000 registro desde la fecha indicada
        trades, last = self.API.get_recent_trades(pair, dt_from)
        # Ordenamos por fecha
        trades = trades.sort_values('time', ascending=False)
        trades = trades.reset_index()
        # Obtenemos primero y ultimo
        first = trades['time'].iloc[-1]
        last = trades['time'].iloc[0]
        return({'first': first, 'last': last, 'trades': trades})
    
    @st.cache
    def download_fromto_historic(self, pair, dt_from, dt_to):
        data_pair = []
        # Inicializamos while para descargar fromto historico
        from_dynamic = dt_from
        while from_dynamic<=dt_to:
            split = self.download_split_historic(pair, from_dynamic)
            data_pair.append(split)
            from_dynamic = split['last']
            print('Descargado de '+str(split['trades']['dtime'].iloc[-1])+' a '+str(split['trades']['dtime'].iloc[0]))
            # Dormimos la descarga
            time.sleep(np.random.uniform(1,2))
        # Guardamos el acumulado en el atributo de clase data
        self.data[pair] = data_pair