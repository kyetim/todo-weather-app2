from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import os
from datetime import datetime
from typing import List, Dict, Optional, Union
from functools import wraps
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# In-memory storage for demo purposes
todos = []
todo_counter = 0

# Weather API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'demo-key')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Decorator'lar - Python'un güçlü özelliklerinden biri
def handle_errors(f):
    """Hata yönetimi decorator'ı"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash(f'Hata oluştu: {str(e)}', 'error')
            return redirect(url_for('index'))
    return decorated_function

def require_method(method):
    """HTTP method kontrolü decorator'ı"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method != method:
                return jsonify({'error': 'Method not allowed'}), 405
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_input(required_fields):
    """Input doğrulama decorator'ı"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'{field} alanı zorunludur!', 'error')
                    return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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

def get_priority_order(priority):
    """Öncelik sırası için sayısal değer döndür"""
    priority_map = {'yüksek': 1, 'orta': 2, 'düşük': 3}
    return priority_map.get(priority, 2)

def validate_todo_text(text):
    """Todo metni doğrulama"""
    return 2 <= len(text) <= 500

def get_todo_statistics():
    """Todo istatistiklerini hesapla"""
    total = len(todos)
    completed = len([todo for todo in todos if todo.get('completed', False)])
    pending = total - completed
    
    high_priority = len([todo for todo in todos if todo.get('priority') == 'yüksek'])
    medium_priority = len([todo for todo in todos if todo.get('priority') == 'orta'])
    low_priority = len([todo for todo in todos if todo.get('priority') == 'düşük'])
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': round((completed / total * 100), 1) if total > 0 else 0,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority
    }

@app.route('/')
@handle_errors
def index():
    """Ana sayfa - todo listesi ve hava durumu"""
    # Query parametrelerini al
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    # Hava durumu verilerini al
    weather_data = get_weather(city)
    
    # Todo'ları filtrele
    filtered_todos = todos
    if filter_priority:
        filtered_todos = [todo for todo in todos if todo.get('priority') == filter_priority]
    
    # Todo'ları öncelik sırasına göre sırala (lambda fonksiyonu)
    sorted_todos = sorted(
        filtered_todos, 
        key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
    )
    
    # İstatistikleri hesapla
    stats = get_todo_statistics()
    
    return render_template(
        'index.html', 
        todos=sorted_todos, 
        weather=weather_data, 
        current_city=city, 
        current_filter=filter_priority,
        stats=stats,
        user=None  # Basit versiyonda kullanıcı sistemi yok
    )

@app.route('/add', methods=['POST'])
@handle_errors
@require_method('POST')
@validate_input(['todo'])
def add_todo():
    """Yeni todo ekle"""
    global todo_counter
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    
    # Input doğrulama
    if not validate_todo_text(todo_text):
        flash('Todo metni 2-500 karakter arasında olmalıdır!', 'error')
        return redirect(url_for('index'))
    
    # Yeni todo oluştur
    todo_counter += 1
    new_todo = {
        'id': todo_counter,
        'text': todo_text,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    todos.append(new_todo)
    flash(f'Todo başarıyla eklendi!', 'success')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
@handle_errors
def complete_todo(todo_id):
    """Todo'yu tamamla/tamamlanmamış yap"""
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            flash('Todo durumu güncellendi!', 'success')
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
@handle_errors
def delete_todo(todo_id):
    """Todo'yu sil"""
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    flash('Todo başarıyla silindi!', 'info')
    return redirect(url_for('index'))

@app.route('/weather')
@handle_errors
def weather():
    """Sadece hava durumu sayfası"""
    city = request.args.get('city', 'Istanbul')
    weather_data = get_weather(city)
    return render_template('weather.html', weather=weather_data, current_city=city)

# REST API Endpoints
@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    """Tüm todo'ları JSON olarak döndür - REST API"""
    return jsonify({
        'success': True,
        'data': todos,
        'count': len(todos)
    })

@app.route('/api/todos', methods=['POST'])
def api_create_todo():
    """Yeni todo oluştur - REST API"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Text field required'}), 400
    
    if not validate_todo_text(data['text']):
        return jsonify({'success': False, 'error': 'Invalid text length'}), 400
    
    global todo_counter
    todo_counter += 1
    priority = data.get('priority', 'orta')
    new_todo = {
        'id': todo_counter,
        'text': data['text'],
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    todos.append(new_todo)
    
    return jsonify({
        'success': True,
        'data': new_todo
    }), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    """Todo güncelle - REST API"""
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'success': False, 'error': 'Todo not found'}), 404
    
    data = request.get_json()
    if 'text' in data:
        todo['text'] = data['text']
    if 'priority' in data:
        todo['priority'] = data['priority']
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    return jsonify({
        'success': True,
        'data': todo
    })

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    """Todo sil - REST API"""
    global todos
    original_length = len(todos)
    todos = [t for t in todos if t['id'] != todo_id]
    
    if len(todos) < original_length:
        return jsonify({'success': True, 'message': 'Todo deleted'})
    return jsonify({'success': False, 'error': 'Todo not found'}), 404

@app.route('/api/weather/<city>')
def api_get_weather(city):
    """Hava durumu API endpoint'i"""
    weather_data = get_weather(city)
    if weather_data:
        return jsonify({
            'success': True,
            'data': weather_data
        })
    return jsonify({
        'success': False,
        'error': 'Weather data not found'
    }), 404

# Context processor
@app.context_processor
def inject_global_vars():
    """Template'lere global değişkenler enjekte et"""
    return {
        'app_name': 'Todo & Hava Durumu',
        'version': '1.0.0',
        'current_year': datetime.now().year
    }

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """404 hata yönetimi"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 hata yönetimi"""
    return render_template('500.html'), 500

# Vercel için WSGI uygulaması
handler = app
