from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# In-memory storage
todos = []
todo_counter = 0

# Weather API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'demo-key')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return decorated_function

def get_weather(city):
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
    priority_map = {'yüksek': 1, 'orta': 2, 'düşük': 3}
    return priority_map.get(priority, 2)

def validate_todo_text(text):
    return 2 <= len(text) <= 500

@app.route('/')
@handle_errors
def index():
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    weather_data = get_weather(city)
    
    filtered_todos = todos
    if filter_priority:
        filtered_todos = [todo for todo in todos if todo.get('priority') == filter_priority]
    
    sorted_todos = sorted(
        filtered_todos, 
        key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
    )
    
    return render_template(
        'index.html', 
        todos=sorted_todos, 
        weather=weather_data, 
        current_city=city, 
        current_filter=filter_priority,
        stats={'total': len(todos), 'completed': len([t for t in todos if t.get('completed', False)])},
        user=None
    )

@app.route('/add', methods=['POST'])
@handle_errors
def add_todo():
    global todo_counter
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    
    if not validate_todo_text(todo_text):
        flash('Todo metni 2-500 karakter arasında olmalıdır!', 'error')
        return redirect(url_for('index'))
    
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
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            flash('Todo durumu güncellendi!', 'success')
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
@handle_errors
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    flash('Todo başarıyla silindi!', 'info')
    return redirect(url_for('index'))

@app.route('/weather')
@handle_errors
def weather():
    city = request.args.get('city', 'Istanbul')
    weather_data = get_weather(city)
    return render_template('weather.html', weather=weather_data, current_city=city)

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    return jsonify({
        'success': True,
        'data': todos,
        'count': len(todos)
    })

@app.route('/api/todos', methods=['POST'])
def api_create_todo():
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

@app.route('/api/weather/<city>')
def api_get_weather(city):
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

@app.context_processor
def inject_global_vars():
    return {
        'app_name': 'Todo & Hava Durumu',
        'version': '1.0.0',
        'current_year': datetime.now().year
    }

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Vercel handler
handler = app