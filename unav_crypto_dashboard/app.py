import streamlit as st
import datetime as dt
from download.downloader import Downloader
from transform.transformer import Wrangler, Calculator
from utils.dates import DateFormatter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():

    if 'data' not in st.session_state:
        st.session_state.data = 0

    st.title('Price, VWAP and Volume plots')
    st.write('1. Select pair on the left menu and date interval to get data \n2. Select time interval to compute VWAP')

    # 1. Data downloader en la barra lateral
    ###############################################################################################

    st.sidebar.title("Data Download")

    # Llamamos al Downloader
    d = Downloader()
    # Descargamos la lista de pares
    d.download_list_of_pairs()
    pairs = d.pairs['wsname'].tolist()

    # Seleccionamos par
    st.sidebar.subheader("Select pair")
    pair = st.sidebar.selectbox(
        "Click below to select a new pair",
        ['']+pairs,
        format_func=lambda x: 'Select an option' if x == '' else x
    )
    if pair:
        st.sidebar.success('Succesful selection')
        ticker = d.pairs[d.pairs['wsname'] == pair]['altname'].tolist()[0]

    else:
        st.sidebar.warning('No option is selected')

    # Seleccionamos fecha
    st.sidebar.subheader("Select dates interval")
    today = dt.date.today()
    yesterday = today + dt.timedelta(days=-1)
    start_date = st.sidebar.date_input('Click below to select a new approx. start date', yesterday)
    end_date = st.sidebar.date_input('Click below to select a new approx. start date', today)
    if start_date < end_date:
        st.sidebar.success('Approximate start date: `%s`\n\nApproximate end date: `%s`' % (start_date, end_date))
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    # Boton de descarga
    button_download = st.sidebar.button('Download data')

    if button_download:
        dt_from = DateFormatter.date_formats(str(start_date)+' 00:00:00')
        dt_to = DateFormatter.date_formats(str(end_date)+' 00:00:00')
        with st.spinner('Downloading 🕒🕒🕒'):
            d.download_fromto_historic(ticker, dt_from['unix'], dt_to['unix'])
        st.sidebar.success('Finished!')

        # Comprobamos datos descargados
        st.sidebar.write('\n')
        st.sidebar.write('Information of downloaded data: ')

        for key, value in d.data.items():
            from_ = value[0]['first']
            from_ = str(dt.datetime.utcfromtimestamp(from_).strftime('%Y-%m-%d %H:%M:%S'))
            to_ = value[-1]['last']
            to_ = str(dt.datetime.utcfromtimestamp(to_).strftime('%Y-%m-%d %H:%M:%S'))
            st.sidebar.info('**'+key+'** from **' + from_ + '** to **'+to_+'**')

        st.session_state.data = d.data

    # 2. Graficos
    ###############################################################################################

    # VWAP interval
    interval_options = {
        5: '5 minutes',
        10: '10 minutes',
        15: '15 minutes',
        30: '30 minutes',
        60: '1 hour',
        4*60: '4 hours',
        12*60: '12 hours',
        24*60: '1 day',
        7*24*60: '1 week',
        14*24*60: '2 weeks',
        28*24*60: '1 month'
    }
    interval = st.selectbox(
        "Click below to select an interval to compute VWAP",
        ['']+list(interval_options.keys()),
        format_func=lambda x: 'Select an option' if x == '' else interval_options[x]
    )
    if interval:

        w = Wrangler()
        trades = w.get_clean_data(st.session_state.data)[ticker]

        # Calculamos los indicadores
        c = Calculator(trades)
        c.compute_price()
        c.compute_vwap(minutes_interval=interval)

        # Graficamos precio y vwap
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        fig.add_trace(
            go.Scatter(
                x=c.data['price']['dtime'],
                y=c.data['price']['price'],
                mode='lines', name='Price', line_color='#fc4f30'
            ),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(
                x=c.data['vwap']['dtime'],
                y=c.data['vwap']['price'],
                mode='lines', name='VWAP', line_color='#30a2da'
            ),
            row=1, col=1)
        # Graficamos volumen
        fig.add_trace(
            go.Bar(
                x=c.data['vwap']['dtime'],
                y=c.data['vwap']['volume'],
                name='Volume', marker={'color': '#30a2da'}
            ),
            row=2, col=1)
        fig['layout'].update(height=600, title=pair)
        fig['layout']['yaxis1'].update(domain=[0.30, 1])
        fig['layout']['yaxis2'].update(domain=[0, 0.25])
        fig['layout']['xaxis2']['title']='Time'
        fig['layout']['yaxis']['title']='Price'
        fig['layout']['yaxis2']['title']='Volume'
        fig.update_xaxes(rangeslider_thickness = 0.01)
        fig.update_layout(xaxis_rangeslider_visible=False, xaxis2_rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)

main()
