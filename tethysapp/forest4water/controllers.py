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
            name='Min Discharge',
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
            line=dict(color='#8c564b')
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

def get_monthly_mean_discharge_data(request):
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

        pairs = [list(a) for a in zip(dates, mean_discharge)]
        mean_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        mean_discharge_df.set_index('Datetime', inplace=True)

        mean_jan_df = mean_discharge_df[mean_discharge_df.index.month == 1]
        mean_feb_df = mean_discharge_df[mean_discharge_df.index.month == 2]
        mean_mar_df = mean_discharge_df[mean_discharge_df.index.month == 3]
        mean_apr_df = mean_discharge_df[mean_discharge_df.index.month == 4]
        mean_may_df = mean_discharge_df[mean_discharge_df.index.month == 5]
        mean_jun_df = mean_discharge_df[mean_discharge_df.index.month == 6]
        mean_jul_df = mean_discharge_df[mean_discharge_df.index.month == 7]
        mean_aug_df = mean_discharge_df[mean_discharge_df.index.month == 8]
        mean_sep_df = mean_discharge_df[mean_discharge_df.index.month == 9]
        mean_oct_df = mean_discharge_df[mean_discharge_df.index.month == 10]
        mean_nov_df = mean_discharge_df[mean_discharge_df.index.month == 11]
        mean_dec_df = mean_discharge_df[mean_discharge_df.index.month == 12]

        mean_jan_Q = go.Scatter(
            x=mean_jan_df.index.year.unique().tolist(),
            y=mean_jan_df.iloc[:,0].tolist(),
            name='mean January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        mean_feb_Q = go.Scatter(
            x=mean_feb_df.index.year.unique().tolist(),
            y=mean_feb_df.iloc[:, 0].tolist(),
            name='mean February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        mean_mar_Q = go.Scatter(
            x=mean_mar_df.index.year.unique().tolist(),
            y=mean_mar_df.iloc[:, 0].tolist(),
            name='mean March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        mean_apr_Q = go.Scatter(
            x=mean_apr_df.index.year.unique().tolist(),
            y=mean_apr_df.iloc[:, 0].tolist(),
            name='mean April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        mean_may_Q = go.Scatter(
            x=mean_may_df.index.year.unique().tolist(),
            y=mean_may_df.iloc[:, 0].tolist(),
            name='mean May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        mean_jun_Q = go.Scatter(
            x=mean_jun_df.index.year.unique().tolist(),
            y=mean_jun_df.iloc[:, 0].tolist(),
            name='mean June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        mean_jul_Q = go.Scatter(
            x=mean_jul_df.index.year.unique().tolist(),
            y=mean_jul_df.iloc[:, 0].tolist(),
            name='mean July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        mean_aug_Q = go.Scatter(
            x=mean_aug_df.index.year.unique().tolist(),
            y=mean_aug_df.iloc[:, 0].tolist(),
            name='mean August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        mean_sep_Q = go.Scatter(
            x=mean_sep_df.index.year.unique().tolist(),
            y=mean_sep_df.iloc[:, 0].tolist(),
            name='mean September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        mean_oct_Q = go.Scatter(
            x=mean_oct_df.index.year.unique().tolist(),
            y=mean_oct_df.iloc[:, 0].tolist(),
            name='mean October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        mean_nov_Q = go.Scatter(
            x=mean_nov_df.index.year.unique().tolist(),
            y=mean_nov_df.iloc[:, 0].tolist(),
            name='mean November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        mean_dec_Q = go.Scatter(
            x=mean_dec_df.index.year.unique().tolist(),
            y=mean_dec_df.iloc[:, 0].tolist(),
            name='mean December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Mean Discharge at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Mean Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[mean_jan_Q, mean_feb_Q, mean_mar_Q, mean_apr_Q, mean_may_Q, mean_jun_Q, mean_jul_Q, mean_aug_Q, mean_sep_Q,
                  mean_oct_Q, mean_nov_Q, mean_dec_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_monthly_std_discharge_data(request):
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
        std_discharge = df['Qs'].tolist()

        pairs = [list(a) for a in zip(dates, std_discharge)]
        std_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        std_discharge_df.set_index('Datetime', inplace=True)

        std_jan_df = std_discharge_df[std_discharge_df.index.month == 1]
        std_feb_df = std_discharge_df[std_discharge_df.index.month == 2]
        std_mar_df = std_discharge_df[std_discharge_df.index.month == 3]
        std_apr_df = std_discharge_df[std_discharge_df.index.month == 4]
        std_may_df = std_discharge_df[std_discharge_df.index.month == 5]
        std_jun_df = std_discharge_df[std_discharge_df.index.month == 6]
        std_jul_df = std_discharge_df[std_discharge_df.index.month == 7]
        std_aug_df = std_discharge_df[std_discharge_df.index.month == 8]
        std_sep_df = std_discharge_df[std_discharge_df.index.month == 9]
        std_oct_df = std_discharge_df[std_discharge_df.index.month == 10]
        std_nov_df = std_discharge_df[std_discharge_df.index.month == 11]
        std_dec_df = std_discharge_df[std_discharge_df.index.month == 12]

        std_jan_Q = go.Scatter(
            x=std_jan_df.index.year.unique().tolist(),
            y=std_jan_df.iloc[:,0].tolist(),
            name='std January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        std_feb_Q = go.Scatter(
            x=std_feb_df.index.year.unique().tolist(),
            y=std_feb_df.iloc[:, 0].tolist(),
            name='std February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        std_mar_Q = go.Scatter(
            x=std_mar_df.index.year.unique().tolist(),
            y=std_mar_df.iloc[:, 0].tolist(),
            name='std March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        std_apr_Q = go.Scatter(
            x=std_apr_df.index.year.unique().tolist(),
            y=std_apr_df.iloc[:, 0].tolist(),
            name='std April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        std_may_Q = go.Scatter(
            x=std_may_df.index.year.unique().tolist(),
            y=std_may_df.iloc[:, 0].tolist(),
            name='std May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        std_jun_Q = go.Scatter(
            x=std_jun_df.index.year.unique().tolist(),
            y=std_jun_df.iloc[:, 0].tolist(),
            name='std June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        std_jul_Q = go.Scatter(
            x=std_jul_df.index.year.unique().tolist(),
            y=std_jul_df.iloc[:, 0].tolist(),
            name='std July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        std_aug_Q = go.Scatter(
            x=std_aug_df.index.year.unique().tolist(),
            y=std_aug_df.iloc[:, 0].tolist(),
            name='std August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        std_sep_Q = go.Scatter(
            x=std_sep_df.index.year.unique().tolist(),
            y=std_sep_df.iloc[:, 0].tolist(),
            name='std September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        std_oct_Q = go.Scatter(
            x=std_oct_df.index.year.unique().tolist(),
            y=std_oct_df.iloc[:, 0].tolist(),
            name='std October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        std_nov_Q = go.Scatter(
            x=std_nov_df.index.year.unique().tolist(),
            y=std_nov_df.iloc[:, 0].tolist(),
            name='std November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        std_dec_Q = go.Scatter(
            x=std_dec_df.index.year.unique().tolist(),
            y=std_dec_df.iloc[:, 0].tolist(),
            name='std December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Std Discharge at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Std Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[std_jan_Q, std_feb_Q, std_mar_Q, std_apr_Q, std_may_Q, std_jun_Q, std_jul_Q, std_aug_Q, std_sep_Q,
                  std_oct_Q, std_nov_Q, std_dec_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_monthly_max_discharge_data(request):
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
        max_discharge = df['Qx'].tolist()

        pairs = [list(a) for a in zip(dates, max_discharge)]
        max_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        max_discharge_df.set_index('Datetime', inplace=True)

        max_jan_df = max_discharge_df[max_discharge_df.index.month == 1]
        max_feb_df = max_discharge_df[max_discharge_df.index.month == 2]
        max_mar_df = max_discharge_df[max_discharge_df.index.month == 3]
        max_apr_df = max_discharge_df[max_discharge_df.index.month == 4]
        max_may_df = max_discharge_df[max_discharge_df.index.month == 5]
        max_jun_df = max_discharge_df[max_discharge_df.index.month == 6]
        max_jul_df = max_discharge_df[max_discharge_df.index.month == 7]
        max_aug_df = max_discharge_df[max_discharge_df.index.month == 8]
        max_sep_df = max_discharge_df[max_discharge_df.index.month == 9]
        max_oct_df = max_discharge_df[max_discharge_df.index.month == 10]
        max_nov_df = max_discharge_df[max_discharge_df.index.month == 11]
        max_dec_df = max_discharge_df[max_discharge_df.index.month == 12]

        max_jan_Q = go.Scatter(
            x=max_jan_df.index.year.unique().tolist(),
            y=max_jan_df.iloc[:,0].tolist(),
            name='max January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        max_feb_Q = go.Scatter(
            x=max_feb_df.index.year.unique().tolist(),
            y=max_feb_df.iloc[:, 0].tolist(),
            name='max February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        max_mar_Q = go.Scatter(
            x=max_mar_df.index.year.unique().tolist(),
            y=max_mar_df.iloc[:, 0].tolist(),
            name='max March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        max_apr_Q = go.Scatter(
            x=max_apr_df.index.year.unique().tolist(),
            y=max_apr_df.iloc[:, 0].tolist(),
            name='max April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        max_may_Q = go.Scatter(
            x=max_may_df.index.year.unique().tolist(),
            y=max_may_df.iloc[:, 0].tolist(),
            name='max May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        max_jun_Q = go.Scatter(
            x=max_jun_df.index.year.unique().tolist(),
            y=max_jun_df.iloc[:, 0].tolist(),
            name='max June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        max_jul_Q = go.Scatter(
            x=max_jul_df.index.year.unique().tolist(),
            y=max_jul_df.iloc[:, 0].tolist(),
            name='max July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        max_aug_Q = go.Scatter(
            x=max_aug_df.index.year.unique().tolist(),
            y=max_aug_df.iloc[:, 0].tolist(),
            name='max August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        max_sep_Q = go.Scatter(
            x=max_sep_df.index.year.unique().tolist(),
            y=max_sep_df.iloc[:, 0].tolist(),
            name='max September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        max_oct_Q = go.Scatter(
            x=max_oct_df.index.year.unique().tolist(),
            y=max_oct_df.iloc[:, 0].tolist(),
            name='max October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        max_nov_Q = go.Scatter(
            x=max_nov_df.index.year.unique().tolist(),
            y=max_nov_df.iloc[:, 0].tolist(),
            name='max November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        max_dec_Q = go.Scatter(
            x=max_dec_df.index.year.unique().tolist(),
            y=max_dec_df.iloc[:, 0].tolist(),
            name='max December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Max Discharge at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Max Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[max_jan_Q, max_feb_Q, max_mar_Q, max_apr_Q, max_may_Q, max_jun_Q, max_jul_Q, max_aug_Q, max_sep_Q,
                  max_oct_Q, max_nov_Q, max_dec_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_monthly_min_discharge_data(request):
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
        min_discharge = df['Qn'].tolist()

        pairs = [list(a) for a in zip(dates, min_discharge)]
        min_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        min_discharge_df.set_index('Datetime', inplace=True)

        min_jan_df = min_discharge_df[min_discharge_df.index.month == 1]
        min_feb_df = min_discharge_df[min_discharge_df.index.month == 2]
        min_mar_df = min_discharge_df[min_discharge_df.index.month == 3]
        min_apr_df = min_discharge_df[min_discharge_df.index.month == 4]
        min_may_df = min_discharge_df[min_discharge_df.index.month == 5]
        min_jun_df = min_discharge_df[min_discharge_df.index.month == 6]
        min_jul_df = min_discharge_df[min_discharge_df.index.month == 7]
        min_aug_df = min_discharge_df[min_discharge_df.index.month == 8]
        min_sep_df = min_discharge_df[min_discharge_df.index.month == 9]
        min_oct_df = min_discharge_df[min_discharge_df.index.month == 10]
        min_nov_df = min_discharge_df[min_discharge_df.index.month == 11]
        min_dec_df = min_discharge_df[min_discharge_df.index.month == 12]

        min_jan_Q = go.Scatter(
            x=min_jan_df.index.year.unique().tolist(),
            y=min_jan_df.iloc[:,0].tolist(),
            name='min January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        min_feb_Q = go.Scatter(
            x=min_feb_df.index.year.unique().tolist(),
            y=min_feb_df.iloc[:, 0].tolist(),
            name='min February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        min_mar_Q = go.Scatter(
            x=min_mar_df.index.year.unique().tolist(),
            y=min_mar_df.iloc[:, 0].tolist(),
            name='min March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        min_apr_Q = go.Scatter(
            x=min_apr_df.index.year.unique().tolist(),
            y=min_apr_df.iloc[:, 0].tolist(),
            name='min April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        min_may_Q = go.Scatter(
            x=min_may_df.index.year.unique().tolist(),
            y=min_may_df.iloc[:, 0].tolist(),
            name='min May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        min_jun_Q = go.Scatter(
            x=min_jun_df.index.year.unique().tolist(),
            y=min_jun_df.iloc[:, 0].tolist(),
            name='min June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        min_jul_Q = go.Scatter(
            x=min_jul_df.index.year.unique().tolist(),
            y=min_jul_df.iloc[:, 0].tolist(),
            name='min July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        min_aug_Q = go.Scatter(
            x=min_aug_df.index.year.unique().tolist(),
            y=min_aug_df.iloc[:, 0].tolist(),
            name='min August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        min_sep_Q = go.Scatter(
            x=min_sep_df.index.year.unique().tolist(),
            y=min_sep_df.iloc[:, 0].tolist(),
            name='min September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        min_oct_Q = go.Scatter(
            x=min_oct_df.index.year.unique().tolist(),
            y=min_oct_df.iloc[:, 0].tolist(),
            name='min October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        min_nov_Q = go.Scatter(
            x=min_nov_df.index.year.unique().tolist(),
            y=min_nov_df.iloc[:, 0].tolist(),
            name='min November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        min_dec_Q = go.Scatter(
            x=min_dec_df.index.year.unique().tolist(),
            y=min_dec_df.iloc[:, 0].tolist(),
            name='min December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Min Discharge at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Min Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[min_jan_Q, min_feb_Q, min_mar_Q, min_apr_Q, min_may_Q, min_jun_Q, min_jul_Q, min_aug_Q, min_sep_Q,
                  min_oct_Q, min_nov_Q, min_dec_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_monthly_mean_sediments_data(request):
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

        pairs = [list(a) for a in zip(dates, mean_sediments)]
        mean_sediments_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        mean_sediments_df.set_index('Datetime', inplace=True)

        mean_jan_df = mean_sediments_df[mean_sediments_df.index.month == 1]
        mean_feb_df = mean_sediments_df[mean_sediments_df.index.month == 2]
        mean_mar_df = mean_sediments_df[mean_sediments_df.index.month == 3]
        mean_apr_df = mean_sediments_df[mean_sediments_df.index.month == 4]
        mean_may_df = mean_sediments_df[mean_sediments_df.index.month == 5]
        mean_jun_df = mean_sediments_df[mean_sediments_df.index.month == 6]
        mean_jul_df = mean_sediments_df[mean_sediments_df.index.month == 7]
        mean_aug_df = mean_sediments_df[mean_sediments_df.index.month == 8]
        mean_sep_df = mean_sediments_df[mean_sediments_df.index.month == 9]
        mean_oct_df = mean_sediments_df[mean_sediments_df.index.month == 10]
        mean_nov_df = mean_sediments_df[mean_sediments_df.index.month == 11]
        mean_dec_df = mean_sediments_df[mean_sediments_df.index.month == 12]

        mean_jan_S = go.Scatter(
            x=mean_jan_df.index.year.unique().tolist(),
            y=mean_jan_df.iloc[:,0].tolist(),
            name='mean January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        mean_feb_S = go.Scatter(
            x=mean_feb_df.index.year.unique().tolist(),
            y=mean_feb_df.iloc[:, 0].tolist(),
            name='mean February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        mean_mar_S = go.Scatter(
            x=mean_mar_df.index.year.unique().tolist(),
            y=mean_mar_df.iloc[:, 0].tolist(),
            name='mean March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        mean_apr_S = go.Scatter(
            x=mean_apr_df.index.year.unique().tolist(),
            y=mean_apr_df.iloc[:, 0].tolist(),
            name='mean April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        mean_may_S = go.Scatter(
            x=mean_may_df.index.year.unique().tolist(),
            y=mean_may_df.iloc[:, 0].tolist(),
            name='mean May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        mean_jun_S = go.Scatter(
            x=mean_jun_df.index.year.unique().tolist(),
            y=mean_jun_df.iloc[:, 0].tolist(),
            name='mean June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        mean_jul_S = go.Scatter(
            x=mean_jul_df.index.year.unique().tolist(),
            y=mean_jul_df.iloc[:, 0].tolist(),
            name='mean July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        mean_aug_S = go.Scatter(
            x=mean_aug_df.index.year.unique().tolist(),
            y=mean_aug_df.iloc[:, 0].tolist(),
            name='mean August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        mean_sep_S = go.Scatter(
            x=mean_sep_df.index.year.unique().tolist(),
            y=mean_sep_df.iloc[:, 0].tolist(),
            name='mean September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        mean_oct_S = go.Scatter(
            x=mean_oct_df.index.year.unique().tolist(),
            y=mean_oct_df.iloc[:, 0].tolist(),
            name='mean October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        mean_nov_S = go.Scatter(
            x=mean_nov_df.index.year.unique().tolist(),
            y=mean_nov_df.iloc[:, 0].tolist(),
            name='mean November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        mean_dec_S = go.Scatter(
            x=mean_dec_df.index.year.unique().tolist(),
            y=mean_dec_df.iloc[:, 0].tolist(),
            name='mean December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Mean Sediments Concentration at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Mean Sediments Concentration (kg/m<sup>3</sup>)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[mean_jan_S, mean_feb_S, mean_mar_S, mean_apr_S, mean_may_S, mean_jun_S, mean_jul_S, mean_aug_S, mean_sep_S,
                  mean_oct_S, mean_nov_S, mean_dec_S], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_monthly_std_sediments_data(request):
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
        std_sediments = df['Ss'].tolist()

        pairs = [list(a) for a in zip(dates, std_sediments)]
        std_sediments_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        std_sediments_df.set_index('Datetime', inplace=True)

        std_jan_df = std_sediments_df[std_sediments_df.index.month == 1]
        std_feb_df = std_sediments_df[std_sediments_df.index.month == 2]
        std_mar_df = std_sediments_df[std_sediments_df.index.month == 3]
        std_apr_df = std_sediments_df[std_sediments_df.index.month == 4]
        std_may_df = std_sediments_df[std_sediments_df.index.month == 5]
        std_jun_df = std_sediments_df[std_sediments_df.index.month == 6]
        std_jul_df = std_sediments_df[std_sediments_df.index.month == 7]
        std_aug_df = std_sediments_df[std_sediments_df.index.month == 8]
        std_sep_df = std_sediments_df[std_sediments_df.index.month == 9]
        std_oct_df = std_sediments_df[std_sediments_df.index.month == 10]
        std_nov_df = std_sediments_df[std_sediments_df.index.month == 11]
        std_dec_df = std_sediments_df[std_sediments_df.index.month == 12]

        std_jan_S = go.Scatter(
            x=std_jan_df.index.year.unique().tolist(),
            y=std_jan_df.iloc[:,0].tolist(),
            name='std January',
            mode='lines+markers',
            line=dict(color="rgb(141,211,199)")
        )

        std_feb_S = go.Scatter(
            x=std_feb_df.index.year.unique().tolist(),
            y=std_feb_df.iloc[:, 0].tolist(),
            name='std February',
            mode='lines+markers',
            line=dict(color="rgb(255,255,179)")
        )

        std_mar_S = go.Scatter(
            x=std_mar_df.index.year.unique().tolist(),
            y=std_mar_df.iloc[:, 0].tolist(),
            name='std March',
            mode='lines+markers',
            line=dict(color="rgb(190,186,218)")
        )

        std_apr_S = go.Scatter(
            x=std_apr_df.index.year.unique().tolist(),
            y=std_apr_df.iloc[:, 0].tolist(),
            name='std April',
            mode='lines+markers',
            line=dict(color="rgb(251,128,114)")
        )

        std_may_S = go.Scatter(
            x=std_may_df.index.year.unique().tolist(),
            y=std_may_df.iloc[:, 0].tolist(),
            name='std May',
            mode='lines+markers',
            line=dict(color="rgb(128,177,211)")
        )

        std_jun_S = go.Scatter(
            x=std_jun_df.index.year.unique().tolist(),
            y=std_jun_df.iloc[:, 0].tolist(),
            name='std June',
            mode='lines+markers',
            line=dict(color="rgb(253,180,98)")
        )

        std_jul_S = go.Scatter(
            x=std_jul_df.index.year.unique().tolist(),
            y=std_jul_df.iloc[:, 0].tolist(),
            name='std July',
            mode='lines+markers',
            line=dict(color="rgb(179,222,105)")
        )

        std_aug_S = go.Scatter(
            x=std_aug_df.index.year.unique().tolist(),
            y=std_aug_df.iloc[:, 0].tolist(),
            name='std August',
            mode='lines+markers',
            line=dict(color="rgb(252,205,229)")
        )

        std_sep_S = go.Scatter(
            x=std_sep_df.index.year.unique().tolist(),
            y=std_sep_df.iloc[:, 0].tolist(),
            name='std September',
            mode='lines+markers',
            line=dict(color="rgb(217,217,217)")
        )

        std_oct_S = go.Scatter(
            x=std_oct_df.index.year.unique().tolist(),
            y=std_oct_df.iloc[:, 0].tolist(),
            name='std October',
            mode='lines+markers',
            line=dict(color="rgb(188,128,189)")
        )

        std_nov_S = go.Scatter(
            x=std_nov_df.index.year.unique().tolist(),
            y=std_nov_df.iloc[:, 0].tolist(),
            name='std November',
            mode='lines+markers',
            line=dict(color="rgb(204,235,197)")
        )

        std_dec_S = go.Scatter(
            x=std_dec_df.index.year.unique().tolist(),
            y=std_dec_df.iloc[:, 0].tolist(),
            name='std December',
            mode='lines+markers',
            line=dict(color="rgb(255,237,111)")
        )

        layout = go.Layout(title='Std Sediments Concentration at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Dates', ), yaxis=dict(title='Std Sediments Concentration (kg/m<sup>3</sup>)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(
            data=[std_jan_S, std_feb_S, std_mar_S, std_apr_S, std_may_S, std_jun_S, std_jul_S, std_aug_S, std_sep_S,
                  std_oct_S, std_nov_S, std_dec_S], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_scatterPlot_Q_FC(request):
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
        forest_cover = df['Fm'].tolist()

        pairs = [list(a) for a in zip(dates, mean_discharge)]
        mean_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        mean_discharge_df.set_index('Datetime', inplace=True)

        pairs = [list(a) for a in zip(dates, max_discharge)]
        max_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        max_discharge_df.set_index('Datetime', inplace=True)

        pairs = [list(a) for a in zip(dates, min_discharge)]
        min_discharge_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        min_discharge_df.set_index('Datetime', inplace=True)

        pairs = [list(a) for a in zip(dates, forest_cover)]
        forest_cover_df = pd.DataFrame(pairs, columns=['Datetime', 'Forest Cover (%)'])
        forest_cover_df.set_index('Datetime', inplace=True)

        mean_annual_discharge_df = mean_discharge_df.groupby(mean_discharge_df.index.strftime("%Y")).mean()
        mean_annual_discharge_df.index = pd.to_datetime(mean_annual_discharge_df.index)

        max_annual_discharge_df = max_discharge_df.groupby(max_discharge_df.index.strftime("%Y")).max()
        max_annual_discharge_df.index = pd.to_datetime(max_annual_discharge_df.index)

        min_annual_discharge_df = min_discharge_df.groupby(min_discharge_df.index.strftime("%Y")).min()
        min_annual_discharge_df.index = pd.to_datetime(min_annual_discharge_df.index)

        annual_forest_cover_df = forest_cover_df.groupby(forest_cover_df.index.strftime("%Y")).mean()
        annual_forest_cover_df.index = pd.to_datetime(annual_forest_cover_df.index)

        df1 = pd.concat([mean_annual_discharge_df, annual_forest_cover_df], axis=1)

        mean_Q = go.Scatter(
            x=df1.iloc[:,1].tolist(),
            y=df1.iloc[:,0].tolist(),
            mode='lines+markers',
            name='Mean Discharge',
            line=dict(color='#00cc96')
        )

        df2 = pd.concat([max_annual_discharge_df, annual_forest_cover_df], axis=1)

        max_Q = go.Scatter(
            x=df2.iloc[:,1].tolist(),
            y=df2.iloc[:,0].tolist(),
            mode='lines+markers',
            name='Max Discharge',
            line=dict(color='#ef553b')
        )

        df3 = pd.concat([min_annual_discharge_df, annual_forest_cover_df], axis=1)

        min_Q = go.Scatter(
            x=df3.iloc[:,1].tolist(),
            y=df3.iloc[:,0].tolist(),
            mode='lines+markers',
            name='Min Discharge',
            line=dict(color='#636efa')
        )

        layout = go.Layout(title='Mean Streamflow at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Forecast Cover (%)', ), yaxis=dict(title='Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[mean_Q, max_Q, min_Q], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})

def get_scatterPlot_S_FC(request):
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
        forest_cover = df['Fm'].tolist()

        pairs = [list(a) for a in zip(dates, mean_sediments)]
        mean_sediments_df = pd.DataFrame(pairs, columns=['Datetime', 'Streamflow (m3/s)'])
        mean_sediments_df.set_index('Datetime', inplace=True)

        pairs = [list(a) for a in zip(dates, forest_cover)]
        forest_cover_df = pd.DataFrame(pairs, columns=['Datetime', 'Forest Cover (%)'])
        forest_cover_df.set_index('Datetime', inplace=True)

        mean_annual_sediments_df = mean_sediments_df.groupby(mean_sediments_df.index.strftime("%Y")).mean()
        mean_annual_sediments_df.index = pd.to_datetime(mean_annual_sediments_df.index)

        annual_forest_cover_df = forest_cover_df.groupby(forest_cover_df.index.strftime("%Y")).mean()
        annual_forest_cover_df.index = pd.to_datetime(annual_forest_cover_df.index)

        df1 = pd.concat([mean_annual_sediments_df, annual_forest_cover_df], axis=1)

        mean_S = go.Scatter(
            x=df1.iloc[:,1].tolist(),
            y=df1.iloc[:,0].tolist(),
            mode='lines+markers',
            name='Sediment Concentration',
            line=dict(color='#00cc96')
        )

        layout = go.Layout(title='Mean Streamflow at {0}-{1}'.format(nomEstacion, codEstacion),
                           xaxis=dict(title='Forecast Cover (%)', ), yaxis=dict(title='Discharge (m<sup>3</sup>/s)',
                                                                   autorange=True), showlegend=True)

        chart_obj = PlotlyView(go.Figure(data=[mean_S], layout=layout))

        context = {
            'gizmo_object': chart_obj,
        }

        return render(request, 'forest4water/gizmo_ajax.html', context)

    except Exception as e:
        print(str(e))
        return JsonResponse({'error': 'No observed data found for the selected station.'})