# Дашборд для управления складом - лабораторная работа
# Студент: Семёнов Ярослав Олегович
# Группа: 4ИБ-1
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# Интерактивные элементы:
# - Фильтры по товарам и складам
# - 4 типа графиков
# - Таблица с данными

# Создаем тестовые данные для склада
def create_warehouse_data():
    np.random.seed(42)
    
    products = ['Ноутбуки', 'Смартфоны', 'Мониторы', 'Клавиатуры', 'Мыши']
    warehouses = ['Склад А', 'Склад Б', 'Склад В']
    
    data = []
    start_date = datetime(2024, 1, 1)
    
    for i in range(50):
        product = np.random.choice(products)
        warehouse = np.random.choice(warehouses)
        
        record = {
            'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
            'product': product,
            'warehouse': warehouse,
            'quantity': np.random.randint(10, 500),
            'price': np.random.randint(100, 2000),
            'sales': np.random.randint(0, 50)
        }
        record['value'] = record['quantity'] * record['price']
        
        data.append(record)
    
    df = pd.DataFrame(data)
    df.to_csv('warehouse_data.csv', index=False)
    print("Данные созданы!")
    return df

# Создаем дашборд
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🏪 Управление складом", style={'textAlign': 'center', 'color': 'blue'}),
    
    # Фильтры
    html.Div([
        dcc.Dropdown(
            id='product-filter',
            options=[{'label': p, 'value': p} for p in ['Все'] + ['Ноутбуки', 'Смартфоны', 'Мониторы', 'Клавиатуры', 'Мыши']],
            value='Все',
            style={'width': '200px', 'margin': '10px'}
        ),
        dcc.Dropdown(
            id='warehouse-filter', 
            options=[{'label': w, 'value': w} for w in ['Все'] + ['Склад А', 'Склад Б', 'Склад В']],
            value='Все',
            style={'width': '200px', 'margin': '10px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    
    # Графики
    html.Div([
        html.Div([
            dcc.Graph(id='stock-chart')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='category-chart') 
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='warehouse-chart')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='sales-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Таблица
    html.Div([
        html.H3("Данные по складу"),
        dash_table.DataTable(
            id='data-table',
            page_size=10
        )
    ])
])

@app.callback(
    [Output('stock-chart', 'figure'),
     Output('category-chart', 'figure'), 
     Output('warehouse-chart', 'figure'),
     Output('sales-chart', 'figure'),
     Output('data-table', 'data'),
     Output('data-table', 'columns')],
    [Input('product-filter', 'value'),
     Input('warehouse-filter', 'value')]
)
def update_dashboard(product, warehouse):
    # Загружаем данные
    try:
        df = pd.read_csv('warehouse_data.csv')
        print("Данные загружены из файла")
    except:
        print("Создаем новые данные...")
        df = create_warehouse_data()
    
    # Фильтруем
    if product != 'Все':
        df = df[df['product'] == product]
    if warehouse != 'Все':
        df = df[df['warehouse'] == warehouse]
    
    # График 1: Динамика запасов
    stock_fig = px.line(df, x='date', y='quantity', title='📈 Запасы на складе')
    
    # График 2: Распределение по товарам  
    category_fig = px.pie(df, names='product', values='quantity', title='📊 Распределение по товарам')
    
    # График 3: По складам
    warehouse_fig = px.bar(df, x='warehouse', y='quantity', title='🏭 Остатки по складам')
    
    # График 4: Продажи vs Запасы
    sales_fig = px.scatter(df, x='quantity', y='sales', color='product', title='💰 Запасы vs Продажи')
    
    # Таблица
    table_data = df.to_dict('records')
    table_columns = [{"name": col, "id": col} for col in df.columns]
    
    return stock_fig, category_fig, warehouse_fig, sales_fig, table_data, table_columns

if __name__ == '__main__':
    app.run(debug=True)

# Визуальное оформление завершено
# Все графики работают корректно