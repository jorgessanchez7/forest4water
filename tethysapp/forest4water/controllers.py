from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button

import io
import requests
import pandas as pd
import plotly.graph_objs as go
from tethys_sdk.gizmos import PlotlyView
from django.http import HttpResponse, JsonResponse

def home(request):
    """
    Controller for the app home page.
    """

    context = {
    }

    return render(request, 'forest4water/home.html', context)

def get_discharge_data(request):
    """
    Get observed data from csv files in Hydroshare
    """

    get_data = request.GET

    try:

        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        '''Get Observed Data'''

        url = 'https://www.hydroshare.org/resource/6278b7dfa9494764b6208c4a47845b4c/data/contents/{0}.csv'.format(codEstacion)

        s = requests.get(url, verify=False).content

        df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=0)
        df.index = pd.to_datetime(df.index)

        dates = df.index.tolist()
        mean_discharge = df['Qm'].tolist()
        max_discharge = df['Qx'].tolist()
        min_discharge = df['Qn'].tolist()

        mean_Q = go.Scatter(
            x=dates,
            y=mean_discharge,
            name='Mean Discharge',
            line=dict(color='#00cc96')
        )

        max_Q = go.Scatter(
            x=dates,
            y=max_discharge,
            name='Max Discharge',
            line=dict(color='#ef553b')
        )

        min_Q = go.Scatter(
            x=dates,
            y=min_discharge,
            name='Max Discharge',
            line=dict(color='#636efa')
        )

        layout = go.Layout(title='Mean Streamflow at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[mean_Q, max_Q, min_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_sediments_data(request):
    """
    Get observed data from csv files in Hydroshare
    """

    get_data = request.GET

    try:

        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        '''Get Observed Data'''

        url = 'https://www.hydroshare.org/resource/6278b7dfa9494764b6208c4a47845b4c/data/contents/{0}.csv'.format(codEstacion)

        s = requests.get(url, verify=False).content

        df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=0)
        df.index = pd.to_datetime(df.index)

        dates = df.index.tolist()
        mean_sediments = df['Sm'].tolist()

        mean_S = go.Scatter(
            x=dates,
            y=mean_sediments,
            name='Sediment Concentration',
            line=dict(color='#00cc96')
        )

        layout = go.Layout(title='Mean Sediment Concentration at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Sediment Concentration (kg/m<sup>3</sup>)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[mean_S], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_temperature_data(request):
    """
    Get observed data from csv files in Hydroshare
    """

    get_data = request.GET

    try:

        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        '''Get Observed Data'''

        url = 'https://www.hydroshare.org/resource/6278b7dfa9494764b6208c4a47845b4c/data/contents/{0}.csv'.format(codEstacion)

        s = requests.get(url, verify=False).content

        df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=0)
        df.index = pd.to_datetime(df.index)

        dates = df.index.tolist()
        mean_temperature = df['Tm'].tolist()

        mean_T = go.Scatter(
            x=dates,
            y=mean_temperature,
            name='Mean Temperature',
            line=dict(color='#ffa15a')
        )

        layout = go.Layout(title='Mean Temperature at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Temperature (<sup>o</sup>C)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[mean_T], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_precipitation_data(request):
    """
    Get observed data from csv files in Hydroshare
    """

    get_data = request.GET

    try:

        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        '''Get Observed Data'''

        url = 'https://www.hydroshare.org/resource/6278b7dfa9494764b6208c4a47845b4c/data/contents/{0}.csv'.format(codEstacion)

        s = requests.get(url, verify=False).content

        df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=0)
        df.index = pd.to_datetime(df.index)

        dates = df.index.tolist()
        total_precipitation = df['Pm'].tolist()

        total_P = go.Scatter(
            x=dates,
            y=total_precipitation,
            name='Total Precipitation',
            line=dict(color='#ab63fa')
        )

        layout = go.Layout(title='Total Precipitation at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Precipitation (mm)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[total_P], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_forest_cover_data(request):
    """
    Get observed data from csv files in Hydroshare
    """

    get_data = request.GET

    try:

        codEstacion = get_data['stationcode']
        nomEstacion = get_data['stationname']

        '''Get Observed Data'''

        url = 'https://www.hydroshare.org/resource/6278b7dfa9494764b6208c4a47845b4c/data/contents/{0}.csv'.format(codEstacion)

        s = requests.get(url, verify=False).content

        df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col=0)
        df.index = pd.to_datetime(df.index)

        dates = df.index.tolist()
        forest_cover = df['Fm'].tolist()

        total_P = go.Scatter(
            x=dates,
            y=forest_cover,
            name='Forest Cover',
            line=dict(color='#2ca02c')
        )

        layout = go.Layout(title='Forest Cover at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Forest Cover (%)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[total_P], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})