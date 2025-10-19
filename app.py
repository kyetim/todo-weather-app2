from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Hava durumu API anahtarı (ücretsiz OpenWeatherMap API)
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'e73f50fbc7e75e1594e9c58d5a2f451e')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Todo listesi (gerçek uygulamada veritabanı kullanılmalı)
todos = []

def get_priority_order(priority):
    """Öncelik sıralaması için sayısal değer döndür"""
    priority_order = {'yüksek': 1, 'orta': 2, 'düşük': 3}
    return priority_order.get(priority, 2)

def get_weather(city):
    """Hava durumu bilgilerini API'den al"""
    # Demo modu - API anahtarı yoksa demo veri döndür
    if WEATHER_API_KEY == 'demo-key':
        return {
            'city': city,
            'temperature': 22,
            'description': 'açık',
            'humidity': 65,
            'icon': '01d'
        }
    
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'tr'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'icon': data['weather'][0]['icon']
            }
        else:
            return None
    except:
        return None

@app.route('/')
def index():
    """Ana sayfa - todo listesi ve hava durumu"""
    weather_data = None
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    if city:
        weather_data = get_weather(city)
    
    # Todo'ları filtrele
    filtered_todos = todos
    if filter_priority:
        filtered_todos = [todo for todo in todos if todo.get('priority') == filter_priority]
    
    # Todo'ları öncelik sırasına göre sırala
    sorted_todos = sorted(filtered_todos, key=lambda x: (get_priority_order(x.get('priority', 'orta')), x['id']))
    
    return render_template('index.html', todos=sorted_todos, weather=weather_data, current_city=city, current_filter=filter_priority)

@app.route('/add', methods=['POST'])
def add_todo():
    """Yeni todo ekle"""
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')  # Varsayılan öncelik: orta
    
    if todo_text:
        todo = {
            'id': len(todos) + 1,
            'text': todo_text,
            'completed': False,
            'priority': priority,
            'created_at': datetime.now().strftime('%d.%m.%Y %H:%M')
        }
        todos.append(todo)
        flash('Todo başarıyla eklendi!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """Todo'yu tamamla/tamamlanmamış yap"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Todo'yu sil"""
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    flash('Todo silindi!', 'info')
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    """Sadece hava durumu sayfası"""
    city = request.args.get('city', 'Istanbul')
    weather_data = get_weather(city)
    return render_template('weather.html', weather=weather_data, current_city=city)

if __name__ == '__main__':
    app.run(debug=True)
