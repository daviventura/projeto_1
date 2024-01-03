# Dados e Gráficos ===================================================================

# O que deve conter no Dashboard:
# gráfico em barras de gross income por cidade;
# gráfico em barras de rationg por cidade;
# gráfico em barra horizontal de gross income por tipo de pagamento
# gráfico em barra horizontal de rating por tipo de pagamento
# gráfico em barra horizontal de gross income por product line e
#       cidade;
# gráfico em barra horizontal de rating por product line e
#       cidade;
# filtro: gross income / rating
# filtro: por cidade


import dash
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from PIL import Image


# Dados

df=pd.read_csv(R'C:\Users\user\OneDrive\Área de Trabalho\Dash -Projeto 1\supermarket_sales.csv')
df.info()
df.head(3)
df['Date']=pd.to_datetime(df['Date'])
cidades=df['City'].unique()
pagamento=df['Payment'].unique()
pl=df['Product line'].unique()
income_rating=['gross income','Rating']

df_gender=df.groupby(['Gender','City']).sum('gross income').reset_index()
dff_g=df_gender[df_gender['City'].isin(['Mandalay','Naypyitaw'])]
fig=px.bar(dff_g, y='gross income',x='Gender',barmode='group',color='City')


imagem_card=Image.open('imagens/imagemrr.jpg')
load_figure_template('flatly')

# App

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
server=app.server

# Layout

app.layout=html.Div([

    dbc.Row([
        dbc.Col(md=2,xs=5,
            children=[
                dbc.Card(className='card',
                    children=[
                        dbc.CardImg(src=imagem_card,top=True,className='img_card'),

                        html.Hr(),

                        html.H4('Cidade',className='titulo1'),

                        dcc.Checklist(
                            id='cidades',
                            options=cidades,
                            value=list(cidades),
                            inputStyle={'margin-bottom':'10px'}
                        ),

                        html.H4('Variável',style={'margin-top':'20px'}),

                        dcc.RadioItems(
                            id='variavel',
                            options=income_rating,
                            value=income_rating[0]
                        )
                    ]),
            ]
        ),

        dbc.Col(md=10,xs=7,
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(md=4,className='graph1',
                            children=[
                                dcc.Graph(id='graph_bar1'),

                            ]
                        ),

                        dbc.Col(md=4,className='graph1',
                            children=[
                                dcc.Graph(id='graph_bar2'),
                            ]
                        ),

                        dbc.Col(md=4,className='graph1',
                            children=[
                                dcc.Graph(id='graph_bar_gender'),
                            ]
                        ),

                    ]
                ),

                dbc.Row(className='graph3',
                    children=[
                        dcc.Graph(id='graph_bar3')
                    ]
                ),
            ]
        )
    ]),

])


# Callbacks



@app.callback(
    [Output('graph_bar1','figure'),
     Output('graph_bar2','figure'),
     Output('graph_bar_gender','figure'),
     Output('graph_bar3','figure')
    ],
    
    [Input('cidades','value'),
    Input('variavel','value')]
)
def grafico_1(cidade,variavel):

    operation=np.sum if variavel=='gross income' else np.mean

    df_city=df.groupby('City')[variavel].apply(operation).to_frame().reset_index()
    dff_city=df_city[df_city['City'].isin(cidade)]
    fig_city=px.bar(dff_city,x='City',y=variavel)

    df_pay=df.groupby('Payment')[variavel].apply(operation).to_frame().reset_index()
    dff_pay=df_pay[df_pay['Payment'].isin(pagamento[range(0,3)])]
    fig_payment=px.bar(dff_pay,y='Payment',x=variavel,orientation='h')

    df_pl=df.groupby(['Product line','City'])[variavel].apply(operation).to_frame().reset_index()
    dff_pl=df_pl[df_pl['City'].isin(cidade)]
    fig_pl=px.bar(dff_pl,y='Product line',x=variavel,color='City',barmode='group')

    df_gender=df.groupby(['Gender','City'])[variavel].apply(operation).to_frame().reset_index()
    dff_g=df_gender[df_gender['City'].isin(cidade)]
    fig_gender=px.bar(dff_g, y=variavel,x='Gender',barmode='group',color='City')

    for fig in [fig_city,fig_payment,fig_gender]:
        fig.update_layout(height=250,template='flatly')

    fig_pl.update_layout(height=350,template='flatly')

    return fig_city, fig_payment, fig_gender, fig_pl

# Run Server

if __name__=='__main__':
    app.run_server(debug=False,port=8051)