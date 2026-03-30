import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

app = dash.Dash(__name__)

# Layout
app.layout = html.Div(style={'backgroundColor': '#0d1117', 'color': 'white', 'padding': '20px'}, children=[

    html.H1("Currency Exchange Rate Simulator", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Interest Rate (%)"),
        dcc.Slider(0, 10, step=0.5, value=2, id='interest'),

        html.Label("Inflation (%)"),
        dcc.Slider(0, 15, step=0.5, value=5, id='inflation'),

        html.Label("Trade Balance (%)"),
        dcc.Slider(-10, 10, step=1, value=0, id='trade'),

        html.Label("Economic Strength Index"),
        dcc.Slider(50, 150, step=5, value=100, id='strength'),

    ], style={'marginBottom': '40px'}),

    dcc.Graph(id='exchange-graph'),
    html.Div(id='output-text', style={'fontSize': 20, 'marginTop': '20px'})
])

# Model
def exchange_model(interest, inflation, trade, strength):
    exchange_rate = 1 + 0.02*interest - 0.03*inflation + 0.01*trade + 0.005*strength
    volatility = abs(inflation - interest) + abs(trade)
    return exchange_rate, volatility

# Callback
@app.callback(
    [Output('exchange-graph', 'figure'),
     Output('output-text', 'children')],
    [Input('interest', 'value'),
     Input('inflation', 'value'),
     Input('trade', 'value'),
     Input('strength', 'value')]
)
def update_graph(interest, inflation, trade, strength):
    rate, volatility = exchange_model(interest, inflation, trade, strength)

    x = np.linspace(0, 10, 50)
    y = rate + 0.1*np.sin(x)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Exchange Rate'))

    fig.update_layout(
        template='plotly_dark',
        title="Exchange Rate Dynamics",
        xaxis_title="Time",
        yaxis_title="Exchange Rate"
    )

    text = f"Exchange Rate: {rate:.2f} | Volatility: {volatility:.2f}"

    return fig, text

if __name__ == '__main__':
    app.run(debug=True)
