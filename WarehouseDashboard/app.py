import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Данные для консалтинговых услуг
def create_consulting_data():
    np.random.seed(42)
    
    services = ['Стратегический консалтинг', 'IT-консалтинг', 'Финансовый консалтинг', 'HR-консалтинг']
    clients = ['Клиент A', 'Клиент B', 'Клиент C', 'Клиент D']
    consultants = ['Консультант 1', 'Консультант 2', 'Консультант 3']
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(100):
        service = np.random.choice(services)
        client = np.random.choice(clients)
        consultant = np.random.choice(consultants)
        
        record = {
            'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
            'service': service,
            'client': client,
            'consultant': consultant,
            'hours': np.random.randint(10, 100),
            'rate': np.random.randint(2000, 5000),
            'revenue': np.random.randint(50000, 300000)
        }
        record['profit'] = record['revenue'] * 0.7  # 70% прибыль
        
        data.append(record)
    
    df = pd.DataFrame(data)
    df.to_csv('consulting_data.csv', index=False)
    return df

# Создаем дашборд
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Консалтинговые услуги - Аналитика", style={'textAlign': 'center'}),
    
    # Фильтры
    html.Div([
        dcc.Dropdown(
            id='service-filter',
            options=[{'label': 'Все услуги', 'value': 'all'}] + 
                    [{'label': s, 'value': s} for s in ['Стратегический консалтинг', 'IT-консалтинг', 'Финансовый консалтинг', 'HR-консалтинг']],
            value='all',
            style={'width': '250px', 'margin': '10px'}
        ),
        dcc.Dropdown(
            id='consultant-filter',
            options=[{'label': 'Все консультанты', 'value': 'all'}] + 
                    [{'label': c, 'value': c} for c in ['Консультант 1', 'Консультант 2', 'Консультант 3']],
            value='all',
            style={'width': '250px', 'margin': '10px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    
    # Графики
    html.Div([
        html.Div([dcc.Graph(id='revenue-chart')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='service-pie')], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='consultant-performance')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='client-scatter')], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Таблица
    html.Div([
        html.H3("Детальные данные по проектам"),
        dash_table.DataTable(id='data-table', page_size=10)
    ])
])

@app.callback(
    [Output('revenue-chart', 'figure'),
     Output('service-pie', 'figure'),
     Output('consultant-performance', 'figure'),
     Output('client-scatter', 'figure'),
     Output('data-table', 'data'),
     Output('data-table', 'columns')],
    [Input('service-filter', 'value'),
     Input('consultant-filter', 'value')]
)
def update_dashboard(service, consultant):
    try:
        df = pd.read_csv('consulting_data.csv')
    except:
        df = create_consulting_data()
    
    # Фильтрация
    if service != 'all':
        df = df[df['service'] == service]
    if consultant != 'all':
        df = df[df['consultant'] == consultant]
    
    # Графики
    revenue_fig = px.line(df, x='date', y='revenue', title='📈 Динамика выручки')
    service_fig = px.pie(df, names='service', values='revenue', title='🥧 Распределение по услугам')
    consultant_fig = px.bar(df, x='consultant', y='revenue', title='👨‍💼 Эффективность консультантов')
    client_fig = px.scatter(df, x='hours', y='revenue', color='client', title='🏢 Часы работы vs Выручка')
    
    # Таблица
    table_data = df.to_dict('records')
    table_columns = [{"name": col, "id": col} for col in df.columns]
    
    return revenue_fig, service_fig, consultant_fig, client_fig, table_data, table_columns

if __name__ == '__main__':
    app.run(debug=True)
