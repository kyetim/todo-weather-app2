from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
from datetime import datetime
from typing import List, Dict, Optional, Union
from functools import wraps
import json

# Kendi modüllerimizi import edelim
from models import Todo, WeatherData, TodoManager
from utils import get_priority_order, get_weather_data, format_datetime, validate_todo_text, get_todo_statistics
from config import config
from database import db_manager
from auth import (
    login_required, get_current_user, login_user, logout_user, 
    is_logged_in, get_user_todos, create_user_todo, update_user_todo, 
    delete_user_todo, toggle_user_todo, get_user_todos_by_priority, get_user_statistics
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Konfigürasyon
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Todo yöneticisi (Singleton pattern)
todo_manager = TodoManager()

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

# Lambda fonksiyonları ve list comprehension örnekleri
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
@handle_errors
def index():
    """Ana sayfa - todo listesi ve hava durumu"""
    # Query parametrelerini al
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    # Hava durumu verilerini al (OOP kullanarak)
    weather_data = get_weather_data(city, app.config['WEATHER_API_KEY'])
    
    # Kullanıcı giriş kontrolü
    if not is_logged_in():
        return render_template('login.html', weather=weather_data, current_city=city)
    
    # Todo'ları veritabanından al (PostgreSQL)
    all_todos = get_user_todos()
    filtered_todos = (
        get_user_todos_by_priority(filter_priority) 
        if filter_priority 
        else all_todos
    )
    
    # Todo'ları öncelik sırasına göre sırala (lambda fonksiyonu)
    sorted_todos = sorted(
        filtered_todos, 
        key=lambda x: (get_priority_order(x.get('priority', 'orta')), x['created_at'])
    )
    
    # İstatistikleri hesapla (veritabanından)
    stats = get_user_statistics()
    
    return render_template(
        'index.html', 
        todos=sorted_todos, 
        weather=weather_data, 
        current_city=city, 
        current_filter=filter_priority,
        stats=stats,
        user=get_current_user()
    )

@app.route('/add', methods=['POST'])
@handle_errors
@require_method('POST')
@validate_input(['todo'])
@login_required
def add_todo():
    """Yeni todo ekle - Veritabanı ile"""
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    
    # Input doğrulama (Python fonksiyon kullanarak)
    if not validate_todo_text(todo_text):
        flash('Todo metni 2-500 karakter arasında olmalıdır!', 'error')
        return redirect(url_for('index'))
    
    # Veritabanına todo ekle (PostgreSQL)
    new_todo = create_user_todo(todo_text, priority)
    
    if new_todo:
        flash(f'Todo başarıyla eklendi!', 'success')
    else:
        flash('Todo eklenirken hata oluştu!', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<string:todo_id>')
@handle_errors
@login_required
def complete_todo(todo_id):
    """Todo'yu tamamla/tamamlanmamış yap - Veritabanı ile"""
    if toggle_user_todo(todo_id):
        flash('Todo durumu güncellendi!', 'success')
    else:
        flash('Todo bulunamadı veya güncellenemedi!', 'error')
    return redirect(url_for('index'))

@app.route('/delete/<string:todo_id>')
@handle_errors
@login_required
def delete_todo(todo_id):
    """Todo'yu sil - Veritabanı ile"""
    if delete_user_todo(todo_id):
        flash('Todo başarıyla silindi!', 'info')
    else:
        flash('Todo bulunamadı veya silinemedi!', 'error')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
@handle_errors
def login():
    """Kullanıcı giriş sayfası"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        if not username:
            flash('Kullanıcı adı gerekli!', 'error')
            return render_template('login.html')
        
        if login_user(username, email):
            flash(f'Hoş geldiniz, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Giriş yapılamadı!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@handle_errors
def logout():
    """Kullanıcı çıkış"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/weather')
@handle_errors
def weather():
    """Sadece hava durumu sayfası"""
    city = request.args.get('city', 'Istanbul')
    weather_data = get_weather_data(city, app.config['WEATHER_API_KEY'])
    return render_template('weather.html', weather=weather_data, current_city=city)

# REST API Endpoints - Python'un güçlü özelliklerini gösterir
@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    """Tüm todo'ları JSON olarak döndür - REST API"""
    todos = todo_manager.get_all_todos()
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
    
    priority = data.get('priority', 'orta')
    new_todo = todo_manager.add_todo(data['text'], priority)
    
    return jsonify({
        'success': True,
        'data': new_todo.to_dict()
    }), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def api_update_todo(todo_id):
    """Todo güncelle - REST API"""
    todo = todo_manager.get_todo(todo_id)
    if not todo:
        return jsonify({'success': False, 'error': 'Todo not found'}), 404
    
    data = request.get_json()
    if 'text' in data:
        todo.update_text(data['text'])
    if 'priority' in data:
        todo.update_priority(data['priority'])
    if 'completed' in data:
        if data['completed'] != todo.completed:
            todo.toggle_complete()
    
    return jsonify({
        'success': True,
        'data': todo.to_dict()
    })

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def api_delete_todo(todo_id):
    """Todo sil - REST API"""
    if todo_manager.delete_todo(todo_id):
        return jsonify({'success': True, 'message': 'Todo deleted'})
    return jsonify({'success': False, 'error': 'Todo not found'}), 404

@app.route('/api/weather/<city>')
def api_get_weather(city):
    """Hava durumu API endpoint'i"""
    weather_data = get_weather_data(city, app.config['WEATHER_API_KEY'])
    if weather_data:
        return jsonify({
            'success': True,
            'data': weather_data
        })
    return jsonify({
        'success': False,
        'error': 'Weather data not found'
    }), 404

# Context processor - Python'un güçlü özelliklerinden biri
@app.context_processor
def inject_global_vars():
    """Template'lere global değişkenler enjekte et"""
    return {
        'app_name': 'Todo & Hava Durumu',
        'version': '1.0.0',
        'current_year': datetime.now().year
    }

# Error handlers - Python exception handling
@app.errorhandler(404)
def not_found_error(error):
    """404 hata yönetimi"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 hata yönetimi"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
