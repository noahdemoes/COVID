import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

import dash
import dash_bootstrap_components as dbc

import plotly.express as px
import random
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import pandas as pd
import plotly
from urllib.request import urlopen
import random

directory="./data/pact_strategy_results"

def combinejson(directory):
    totaloutput=pd.DataFrame(columns=['intervention','no_intervention','time','strategy'])
    i=0
    for filename in os.listdir(directory):
        i+=1
        filepath=directory+"/"+filename
        strategy=filename[19:-5]
        jsonfile=pd.read_json(filepath)
        jsonfile['time']=list(jsonfile.index)
        jsonfile['strategy']=[strategy]*jsonfile.shape[0]
        jsonfile=jsonfile.reset_index()
        jsonfile=jsonfile.drop('index',axis=1)
        totaloutput=pd.concat([totaloutput,jsonfile],axis=0)
    totaloutput=totaloutput.reset_index()
    totaloutput=totaloutput.drop('index',axis=1)
    return (totaloutput)



def combineJson(directory):
    totaloutput=pd.DataFrame(columns=['S','E','I','R','Intervention','Strategy','time'])
    S=[]
    E=[]
    I=[]
    R=[]
    time=[]
    strategies=[]
    intervention=[]
    for filename in os.listdir(directory):
        strategy=filename[19:-5]
        filepath=directory+"/"+filename
        with open(filepath) as d:

            data=json.load(d)
            for i in data:
                for j in data[i]:
                    S.append(int(data[i][j]["S"]))
                    E.append(int(data[i][j]["E"]))
                    I.append(int(data[i][j]["I"]))
                    R.append(int(data[i][j]["R"]))
                    intervention.append(i)
                    time.append(int(j))
                    strategies.append(strategy)
    data=pd.DataFrame([S,E,I,R,intervention,strategies,time])
    data=data.T
    data.columns=["S","E","I","R","intervention","strategy","time_stamp"]
    return(data)
def graphCreation(directory,strategy):
    data=combineJson(directory)
    data=data[data["intervention"]=="intervention"]
    data=data[data["strategy"]==str(strategy)]
    data=data.sort_values("time_stamp")
    time=list(data.time_stamp)

    S=list(data.S)
    E=list(data.E)
    I=list(data.I)
    R=list(data.R)
    maxY=max([max(S),max(E),max(I),max(R)])
    minY=min([min(S),min(E),min(I),min(R)])

    trace1=go.Scatter(x=time, y=S,mode="lines",name="Susceptible")
    trace2=go.Scatter(x=time, y=E,mode="lines",name="Exposed")
    trace3=go.Scatter(x=time, y=I,mode="lines",name="Infected")
    trace4=go.Scatter(x=time, y=R,mode="lines",name="Recovered")
    i_fig_SEIR_LINE = go.Figure(data=[trace1,trace2,trace3,trace4])
    # Change the bar mode
    i_fig_SEIR_LINE.update_layout(barmode='group',title="COVID-19 TIME SERIES SEIR MODEL with Intervention")
    i_fig_SEIR_LINE.update_layout(xaxis=dict(range=[time[0],time[-1]]),yaxis=dict(range=[minY,maxY]))
    data=combineJson(directory)
    data2=data[data["intervention"]=="no_intervention"]
    data2=data2[data2["strategy"]==str(strategy)]
    data2=data2.sort_values("time_stamp")
    time=list(data2.time_stamp)

    S2=list(data2.S)
    E2=list(data2.E)
    I2=list(data2.I)
    R2=list(data2.R)

    maxY2=max([max(S2),max(E2),max(I2),max(R2)])
    minY2=min([min(S2),min(E2),min(I2),min(R2)])

    trace12=go.Scatter(x=time, y=S2,mode="lines",name="Susceptible")
    trace22=go.Scatter(x=time, y=E2,mode="lines",name="Exposed")
    trace32=go.Scatter(x=time, y=I2,mode="lines",name="Infected")
    trace42=go.Scatter(x=time, y=R2,mode="lines",name="Recovered")
    non_fig_SEIR_LINE = go.Figure(data=[trace12,trace22,trace32,trace42])
    non_fig_SEIR_LINE.update_layout(barmode='group',title="COVID-19 TIME SERIES SEIR MODEL with No Intervention",xaxis=dict(range=[time[0],time[-1]]),yaxis=dict(range=[minY2,maxY2]))
    i_fig_SEIR_LINE.update_layout(yaxis=dict(range=[minY2,maxY2]))

    S2=list(data2.S)
    E2=list(data2.E)
    I2=list(data2.I)
    R2=list(data2.R)
    time=data.time_stamp
    dS=[]
    dE=[]
    dI=[]
    dR=[]
    differences={"intervention":str(strategy),"Susceptible_Difference":sum(S)-sum(S2),"Exposed_Difference":sum(E)-sum(E2),"Infected_Difference":sum(I)-sum(I2),"Recovered_Difference":sum(R)-sum(R2)}


    return(i_fig_SEIR_LINE,non_fig_SEIR_LINE,differences)
def graphCreationAnimations(directory,strategy):
    data=combineJson(directory)
    data=data[data["intervention"]=="intervention"]
    data=data[data["strategy"]==str(strategy)]
    data=data.sort_values("time_stamp")
    time=list(data.time_stamp)
    S=list(data.S)
    E=list(data.E)
    I=list(data.I)
    R=list(data.R)
    trace1=go.Scatter(
        x=time[0:1], y=S[0:1],
        mode='lines',
        line=dict(width=0.5, color='Green'),
        stackgroup='one',
        groupnorm='percent',
        name="Susceptible"# sets the normalization for the sum of the stackgroup
    )
    trace2=go.Scatter(
        x=time[0:1], y=E[0:1],
        mode='lines',
        line=dict(width=0.5, color='Yellow'),
        stackgroup='one',
        name="Exposed"
    )
    trace3=go.Scatter(
        x=time[0:1], y=I[0:1],
        mode='lines',
        line=dict(width=0.5, color='Red'),
        stackgroup='one',
        name="Infected"
    )
    trace4=go.Scatter(
        x=time[0:1], y=R[0:1],
        mode='lines',
        line=dict(width=0.5, color='Grey'),
        stackgroup='one',
        name="Recovered"
    )

    frames=[]
    for i in range(len(R)):
        trace1.x=time[0:i]
        trace1.y=S[0:i]
        trace2.x=time[0:i]
        trace2.y=E[0:i]
        trace3.x=time[0:i]
        trace3.y=I[0:i]
        trace4.x=time[0:i]
        trace4.y=R[0:i]

        frame=go.Frame(data=[trace1,trace2,trace3,trace4])
        frames.append(frame)
    trace1=go.Scatter(
        x=time, y=S,
        mode='lines',
        line=dict(width=0.5, color='Green'),
        stackgroup='one',
        groupnorm='percent',
        name="Susceptible"# sets the normalization for the sum of the stackgroup
    )
    trace2=go.Scatter(
        x=time, y=E,
        mode='lines',
        line=dict(width=0.5, color='Yellow'),
        stackgroup='one',
        name="Exposed"
    )
    trace3=go.Scatter(
        x=time, y=I,
        mode='lines',
        line=dict(width=0.5, color='Red'),
        stackgroup='one',
        name="Infected"
    )
    trace4=go.Scatter(
        x=time, y=R,
        mode='lines',
        line=dict(width=0.5, color='Grey'),
        stackgroup='one',
        name="Recovered"
    )
    frame=go.Frame(data=[trace1,trace2,trace3,trace4])
    frames.append(frame)

    figTimeSeries = go.Figure(
        data=[trace1, trace2,trace3,trace4],
        layout=go.Layout(
            xaxis=dict(range=[0, max(time)], autorange=False),
            yaxis=dict(range=[0,100],autorange=False),
            title="Start Title",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=frames
    )
    figTimeSeries.update_layout(
        showlegend=True,
        title="COANET Simulation Time Series with Intervention",
        xaxis_type='category',
        xaxis=dict(title="Time Step"),
        yaxis=dict(
            title="Percent of Population",
            type='linear',
            range=[1, 100],
            ticksuffix='%'))
    data=combineJson(directory)
    data=data[data["intervention"]=="no_intervention"]
    data=data[data["strategy"]==str(strategy)]
    data=data.sort_values("time_stamp")
    time=list(data.time_stamp)

    time=list(data.time_stamp)

    S=list(data.S)
    E=list(data.E)
    I=list(data.I)
    R=list(data.R)
    trace1=go.Scatter(
        x=time[0:1], y=S[0:1],
        mode='lines',
        line=dict(width=0.5, color='Green'),
        stackgroup='one',
        groupnorm='percent',
        name="Susceptible"# sets the normalization for the sum of the stackgroup
    )
    trace2=go.Scatter(
        x=time[0:1], y=E[0:1],
        mode='lines',
        line=dict(width=0.5, color='Yellow'),
        stackgroup='one',
        name="Exposed"
    )
    trace3=go.Scatter(
        x=time[0:1], y=I[0:1],
        mode='lines',
        line=dict(width=0.5, color='Red'),
        stackgroup='one',
        name="Infected"
    )
    trace4=go.Scatter(
        x=time[0:1], y=R[0:1],
        mode='lines',
        line=dict(width=0.5, color='Grey'),
        stackgroup='one',
        name="Recovered"
    )

    frames=[]
    for i in range(max(time)):
        trace1.x=time[0:i]
        trace1.y=S[0:i]
        trace2.x=time[0:i]
        trace2.y=E[0:i]
        trace3.x=time[0:i]
        trace3.y=I[0:i]
        trace4.x=time[0:i]
        trace4.y=R[0:i]

        frame=go.Frame(data=[trace1,trace2,trace3,trace4])
        frames.append(frame)
    trace1=go.Scatter(
        x=time, y=S,
        mode='lines',
        line=dict(width=0.5, color='Green'),
        stackgroup='one',
        groupnorm='percent',
        name="Susceptible"# sets the normalization for the sum of the stackgroup
    )
    trace2=go.Scatter(
        x=time, y=E,
        mode='lines',
        line=dict(width=0.5, color='Yellow'),
        stackgroup='one',
        name="Exposed"
    )
    trace3=go.Scatter(
        x=time, y=I,
        mode='lines',
        line=dict(width=0.5, color='Red'),
        stackgroup='one',
        name="Infected"
    )
    trace4=go.Scatter(
        x=time, y=R,
        mode='lines',
        line=dict(width=0.5, color='Grey'),
        stackgroup='one',
        name="Recovered"
    )

    frame=go.Frame(data=[trace1,trace2,trace3,trace4])
    frames.append(frame)
    noni_figTimeSeries = go.Figure(
        data=[trace1, trace2,trace3,trace4],
        layout=go.Layout(
            xaxis=dict(range=[0, max(time)], autorange=False),
            yaxis=dict(range=[0,100],autorange=False),
            title="Start Title",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=frames
    )
    noni_figTimeSeries.update_layout(
        showlegend=True,
        title="NO Intervention COANET Simulation Time Series",
        xaxis_type='category',
        xaxis=dict(title="Time Step"),
        yaxis=dict(
            title="Percent of Population",
            type='linear',
            range=[1, 100],
            ticksuffix='%'))

    return(figTimeSeries,noni_figTimeSeries)
data=combineJson(directory)
strategylist=list(set(list(data["strategy"])))

def createInterventionGraphs(directory,strategy_list):

    data=combineJson(directory)
    strategylist=list(set(list(data["strategy"])))
    InterventionOptions=[]
    for i in strategylist:
        intervention_timeseries,nonintervention_timeseries,differences=graphCreation(directory,i)
        print(differences)
        option={"label":i,"intervention":intervention_timeseries,"non_intervention":nonintervention_timeseries}
        option1={'label':i,"value":option}
        InterventionOptions.append(option1)

    return(InterventionOptions)
def createInterventionGraphsAnimations(directory,strategy_list):
    data=combineJson(directory)
    strategylist=list(set(list(data["strategy"])))
    results=[]
    InterventionOptions=[]
    for i in strategylist:
        intervention_timeseriesa,nonintervention_timeseriesa=graphCreationAnimations(directory,i)
        intervention_timeseries,nonintervention_timeseries,differences=graphCreation(directory,i)
        results.append(differences)
        option={"label":i,"intervention":intervention_timeseries,"non_intervention":nonintervention_timeseries,
               "interventiona":intervention_timeseriesa,"non_interventiona":nonintervention_timeseriesa}
        option1={'label':i,"value":option}
        InterventionOptions.append(option1)
    results_df=pd.DataFrame(results)
    trace12=go.Scatter(x=results_df.intervention, y=results_df.Susceptible_Difference,mode='markers',name="Susceptible")
    trace22=go.Scatter(x=results_df.intervention, y=results_df.Exposed_Difference,mode='markers',    marker=dict(size=[15]*len(list(results_df.intervention))),name="Exposed")
    trace32=go.Scatter(x=results_df.intervention, y=results_df.Infected_Difference,mode='markers',name="Infected")
    trace42=go.Scatter(x=results_df.intervention, y=results_df.Recovered_Difference,mode='markers',name="Recovered")
    non_fig_SEIR_LINE = go.Figure(data=[trace12,trace22,trace32,trace42])
    non_fig_SEIR_LINE.update_layout(title="Differences In Class Distribution for Intervention vs NonIntervention by Experiment")
    return(InterventionOptions)
options2=createInterventionGraphsAnimations(directory,strategylist)

app = dash.Dash(
__name__,
external_stylesheets = [
dbc.themes.SLATE,  # Bootswatch theme
"https://use.fontawesome.com/releases/v5.9.0/css/all.css",],
meta_tags = [{
"name": "description",
"content": "Live coronavirus news, statistics, and visualizations tracking the number of cases and death toll due to COVID-19, with up-to-date testing center information by US states and counties. Also provides current SARS-COV-2 vaccine progress and treatment research across different countries. Sign up for SMS updates."},
{"name": "viewport", "content": "width=device-width*9, initial-scale=1.0"},],)

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.H1('COVID Tracker', className="app-header--title"),
        ]
    ),
    html.Div([
    dcc.Dropdown(
        id='intervention-dropdown',
        options=options2,

    ),
    html.Div(id='intervention-output-container')
])
])



# Disable the autosize on double click because it adds unwanted margins around the image
# More detail: https://plotly.com/python/configuration-options/


server = app.server
@app.callback(
    dash.dependencies.Output('intervention-output-container', 'children'),
    [dash.dependencies.Input('intervention-dropdown', 'value')])
def update_output1(value):
    g=go.Figure(value['intervention'])
    h=go.Figure(value['non_intervention'])
    ga=go.Figure(value['interventiona'])
    ha=go.Figure(value['non_interventiona'])
    return     html.Div(
        children=html.Div([
                    dbc.Row([dbc.Col(html.Div(children=[html.H1("Intervention", className="app-header--title"),dcc.Graph(figure=g)],
            style = {'display': 'inline-block', 'width': '95%',"color":"primary"})),
                           dbc.Col(html.Div(children=[html.H1("No Intervention", className="app-header--title"),dcc.Graph(figure=h)],
            style = {'display': 'inline-block', 'width': '95%',"color":"primary"}))]),
                                dbc.Row([dbc.Col(html.Div(children=[html.H1("Intervention Animation", className="app-header--title"),dcc.Graph(figure=ga)],
            style = {'display': 'inline-block', 'width': '95%',"color":"primary"})),
                           dbc.Col(html.Div(children=[html.H1("No Intervention Animation", className="app-header--title"),dcc.Graph(figure=ha)],
            style = {'display': 'inline-block', 'width': '95%',"color":"primary"}))]),



        ]))



if __name__ == '__main__':
    app.run_server(debug=True)