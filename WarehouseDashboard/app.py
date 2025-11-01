from flask import Flask, render_template_string
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Создаем тестовые данные
def create_data():
    np.random.seed(42)
    products = ['Ноутбуки', 'Смартфоны', 'Мониторы', 'Клавиатуры']
    data = []
    for i in range(50):
        data.append({
            'product': np.random.choice(products),
            'quantity': np.random.randint(10, 100),
            'price': np.random.randint(1000, 5000)
        })
    return pd.DataFrame(data)

@app.route('/')
def dashboard():
    df = create_data()
    
    # Создаем простой график
    fig = px.bar(df, x='product', y='quantity', title='Запасы на складе')
    plot_html = pio.to_html(fig, include_plotlyjs='cdn')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Дашборд склада</title>
    </head>
    <body>
        <h1>🏪 Управление складом</h1>
        {plot_html}
        <p>📊 Всего товаров: {len(df)}</p>
        <p>📦 Общее количество: {df['quantity'].sum()}</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)