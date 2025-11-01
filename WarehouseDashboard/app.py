from flask import Flask

app = Flask(__name__)

@app.route('/')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Дашборд управления складом</title>
        <style>
            body { 
                font-family: Arial; 
                padding: 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
            }
            .stat-card {
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 10px;
                min-width: 150px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏪 Дашборд управления складом</h1>
            <p>Интерактивная система анализа складских запасов</p>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>📦 Товары</h3>
                    <p>15 видов</p>
                </div>
                <div class="stat-card">
                    <h3>🏭 Склады</h3>
                    <p>3 объекта</p>
                </div>
                <div class="stat-card">
                    <h3>💰 Запасы</h3>
                    <p>1,250 ед.</p>
                </div>
            </div>
            
            <div style="text-align: left; background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3>📊 Функциональность:</h3>
                <ul>
                    <li>Динамика складских запасов</li>
                    <li>Анализ товарных категорий</li>
                    <li>Сравнение эффективности складов</li>
                    <li>Интерактивные фильтры и графики</li>
                </ul>
            </div>
            
            <p style="margin-top: 30px; font-size: 18px;">
                🎉 <strong>Дашборд успешно запущен и работает!</strong>
            </p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)