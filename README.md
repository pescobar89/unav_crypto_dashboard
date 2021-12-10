# Universidad de Navarra - Master en Big Data Science - Asignatura Python 
# Proyecto Final: Crypto Dashboard

Autor: **Pablo Ernesto Escobar Vera**

Link de la app online: [**Crypto Dashboard en share.streamlit**](https://share.streamlit.io/pescobar89/unav_crypto_dashboard/main/unav_crypto_dashboard/app.py)

Repositorio (memoria incluida en el README.md): [**GitHub**](https://github.com/pescobar89/unav_crypto_dashboard)


## Objetivo general

El objetivo principal del proyecto es construir una visualización de la cotización de uno o más pares de criptomonedas. Para desarrollar el trabajo se utilizaran las diferentes herramientas vistas en clase.

## Desarrollo

Inicialmente se generó una estructura de carpetas y ficheros utilizando la plantilla proporcionada por **poetry**. Además se utilizó esta librería para desarrollar sobre un **entorno virtual** que facilitara la reproducción de la aplicación en otros sistemas.

Se comenzó el desarrollo trabajando en notebook.

Se investigó la extracción de los datos a través de la **API** de **Kraken**, con las librerías **krakenex** y **pykrakenapi** .

Una vez adquirido este conocimiento se desarrolló un **prototipo** en notebook con las partes de la obtención y tratamiento de los datos (se puede encontrar el notebook en la ruta unav_crypto_dashboard/notebooks/prototype.ipynb del repositorio). Para el desarrollo del prototipo ya se implementó una modularización utilizando **funciones** y **clases**.

En la parte del tratamiento de los datos en la clase Calculator de fichero transformer.py se desarrolló el método **compute_price** que calcula el precio medio ponderado por volumen. Este método no resulta útil con datos extraídos de un exchange centralizado en el que solo se cierra una operación en un mismo momento pero si es de utilidad en el caso de tener operaciones cerradas en el mismo momento como si ocurre en la verdadera blockchain descentralizada. 

En esta misma clase se puede encontrar el método **compute_vwap** que calcula el precio medio ponderado por volumen dado un intervalo de tiempo fijado como input de la método.

Como herramienta de visualización se eligió **Streamlit** por ser la que mayor crecimiento en uso ha estado experimentando y con la intención de conocer su potencial y futuras oportunidades de utilización.


<a href="" rel="some text">![Foo](https://global-uploads.webflow.com/5d3ec351b1eba4332d213004/5f99e10dafbd69a99c875340_C8_qX8dvzv60T4LVZ9GftX-ZH-VJzq3sjUroWWH5XSWw8RFHnCCPPrC6jB3EFVuQdwiqhoEMQKFV-dFz7t6fqaRpSZGvBKI0i1Utj38_j9a54GXMuzi1BiepdIMjOK4ATVdF2131.png)</a>

El diseño del dashboard fue variando según se fue aprendiendo sobre el funcionamiento de Streamlit. En el diseño final se integró un panel lateral para controlar los parámetros de descarga de los datos, la selección del par y del intervalo de tiempo. En el panel principal se integró un selector de intervalo de tiempo para el cálculo del **VWAP**  y para las visualizaciones. Para estas últimas se utilizó la librería **plotly**. Con esta librería se dibujaron dos gráficos:

 1. Un **grafico de serie de tiempo** representando las series **precio** y **VWAP** según el intervalo de tiempo definido en el selector.
 2. Un **grafico de barras** con la representación del **volumen** según el intervalo de tiempo definido en el selector.

Una vez acabado el desarrollo se subió el proyecto a [**GitHub**](https://github.com/pescobar89/unav_crypto_dashboard) y se disponibilizó la aplicación online a través del [**Cloud de Streamlit**](https://share.streamlit.io/pescobar89/unav_crypto_dashboard/main/unav_crypto_dashboard/app.py).

## Ejecución de la app

1. **Acceder** a la aplicación online: [**Crypto dashboard**](https://share.streamlit.io/pescobar89/unav_crypto_dashboard/main/unav_crypto_dashboard/app.py).
2. En el menú lateral izquierdo **seleccionar el par y el intervalo de tiempo**  de interés y **pulsar el botón Download data** para descargar los datos.
3. Tras esto, aparecerá un selector en el panel principal para **definir el intervalo de tiempo** para calcular el VWAP. Realizar la selección y **automáticamente se mostraran los gráficos**.


## Checklist de los objetivos especificos

Lectura y representación del movimiento del par de monedas - Máximo (4 puntos). :heavy_check_mark:
- Descargar datos. Máximo (2 puntos). :heavy_check_mark:
	* Utilizando la librería Kraken (2 puntos). https://github.com/veox/python3-krakenex :heavy_check_mark:
	* Utilizando descarga directa a través de Pandas (1 punto). https://drive.google.com/uc?id=1eQsiD8Z8wEt1mx9VICzCmIEQufWjaUD-
	* Descargar directamente y utilizar el csv en local (0 puntos).
- Graficar cotizaciones. Máximo (2 puntos). :heavy_check_mark:
	* Graficar el par BTC/USDT (1 punto). 
	* Input de usuario que permita graficar cualquier cotización o una a elegir en el menú (2 puntos). :heavy_check_mark:

VWAP. Máximo (3 puntos). :heavy_check_mark:
- Calcular el VWAP y graficarlo (2 puntos). :heavy_check_mark:
- Graficar el VWAP junto con la cotización del par calculado (1 punto). :heavy_check_mark:
- Calcular el VWAP utilizando intervalos temporales (1 punto). :heavy_check_mark:

Estructuración. Máximo (1 punto). :heavy_check_mark:
- Funciones (0,5 puntos). :heavy_check_mark:
- Utilización de clases (0,5 puntos). :heavy_check_mark:
- Manejo de errores y excepciones (0,5 puntos).

Memoria obligatoria. Máximo (2 puntos). :heavy_check_mark:
Este documento deberá ser subido a ADI y deberá tener todo lo necesario para comprender el alcance del proyecto y su modo de ejecución. 

Puntación Extra. Máximo (1 punto). :heavy_check_mark:
- Testeo y cobertura (unit-testing, integration-testing) (0,25 puntos)
- Facilitar los mecanismos para la reproducción del entorno virtual (ya sea con Poetry, Pipenv o pip) (0,25 puntos). :heavy_check_mark:
- Linting y Formatting (adhesión al estandar PEP-8) (0,25 puntos). :heavy_check_mark:
- Distribución del proyecto a través de PyPi o una plataforma PaaS (AWS, Heroku, etc) (0,25 puntos). :heavy_check_mark: