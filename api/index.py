from flask import Flask, jsonify, request
import os
from datetime import datetime

app = Flask(__name__)

# In-memory storage
todos = []
todo_counter = 0

# Weather API configuration
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'e73f50fbc7e75e1594e9c58d5a2f451e')
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

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
        import requests
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
    return jsonify({
        'message': 'Todo & Hava Durumu API',
        'status': 'working',
        'endpoints': {
            'todos': '/api/todos',
            'weather': '/api/weather/<city>',
            'add_todo': '/api/todos (POST)'
        }
    })

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify({
        'success': True,
        'data': todos,
        'count': len(todos)
    })

@app.route('/api/todos', methods=['POST'])
def create_todo():
    global todo_counter
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Text field required'}), 400
    
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
def update_todo(todo_id):
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
def delete_todo(todo_id):
    global todos
    original_length = len(todos)
    todos = [t for t in todos if t['id'] != todo_id]
    
    if len(todos) < original_length:
        return jsonify({'success': True, 'message': 'Todo deleted'})
    return jsonify({'success': False, 'error': 'Todo not found'}), 404

@app.route('/api/weather/<city>')
def get_weather_api(city):
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

# Vercel handler
handler = app