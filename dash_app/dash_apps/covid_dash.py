from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime

app = DjangoDash('covid_dash')
app.css.append_css({'external_url': '/_static/css/dash.css'})
dateparser = lambda x: datetime.strptime(x, '%Y-%m-%d')
data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', parse_dates=['date'], date_parser=dateparser)
countries = data['location'].unique()
iso_codes = data['iso_code'].unique()
values = data.drop(['iso_code', 'continent', 'location', 'date'], axis=1).columns.to_list()
labels = [x.replace('_', ' ').capitalize() for x in values]
app = DjangoDash('covid_dash')
app.css.append_css({'external_url': '/_static/css/dash.css'})
app.layout = html.Div([
    # first row
    html.Div([
        html.Div([dcc.Dropdown(id='country-dropdown', multi=True, options=[{'label': country, 'value': iso_code} for country, iso_code in zip(countries, iso_codes)])], className='three columns'),
        html.Div([dcc.Dropdown(id='variable-dropdown', options=[{'label': label, 'value': value} for label, value in zip(labels, values)])], className='three columns'),
        html.Div([dcc.DatePickerRange(id='date-picker', clearable=True, max_date_allowed=datetime.today().strftime('%Y-%m-%d'), display_format='DD.MM.YYYY',)], className='three columns'),
    ], className='row'),
    #second row
    html.Div([
        html.Div([dcc.Graph(id='covid-graph')])
    ], className='row')
])

@app.callback(
    Output('covid-graph', 'figure'),
    [Input('country-dropdown', 'value'), Input('variable-dropdown', 'value'), Input('date-picker', 'start_date'), Input('date-picker', 'end_date')]
)
def update_div(country, variable, start, end):
    if country is None or variable is None:
        raise PreventUpdate
    else:
        df_wide = data.pivot(index='date', columns='iso_code', values=variable).sort_index()[country]
        country_map = pd.Series(data.location.values, index=data.iso_code).to_dict()
        if start is None:
            start = df_wide.dropna().index[0].strftime('%Y-%m-%d')
        else:
            start = start
        if end is None:
            end = df_wide.dropna().index[-1].strftime('%Y-%m-%d')
        else:
            end = end
        df_select = df_wide.loc[start:end]
        traces = []
        for ticker in df_select.columns:
            trace = go.Bar(
                dict(
                    x=df_select.index,
                    y=df_select[ticker],
                    name=country_map[ticker]
                )
            )
            traces.append(trace)
        layout = go.Layout(
            dict(
                template='plotly_white'
            )
        )
        figure = go.Figure(data=traces, layout=layout)
        return figure