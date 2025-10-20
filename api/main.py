from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# In-memory storage
todos = []
todo_counter = 0
categories = [
    {'id': 1, 'name': 'Genel', 'color': '#007bff'},
    {'id': 2, 'name': 'İş', 'color': '#28a745'},
    {'id': 3, 'name': 'Kişisel', 'color': '#ffc107'},
    {'id': 4, 'name': 'Acil', 'color': '#dc3545'}
]
category_counter = 4

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

def get_todo_statistics():
    total = len(todos)
    completed = len([todo for todo in todos if todo.get('completed', False)])
    pending = total - completed
    
    high_priority = len([todo for todo in todos if todo.get('priority') == 'yüksek'])
    medium_priority = len([todo for todo in todos if todo.get('priority') == 'orta'])
    low_priority = len([todo for todo in todos if todo.get('priority') == 'düşük'])
    
    overdue = 0
    for todo in todos:
        if todo.get('due_date'):
            try:
                due_date = datetime.strptime(todo['due_date'], '%Y-%m-%dT%H:%M')
                if due_date < datetime.now() and not todo.get('completed', False):
                    overdue += 1
            except:
                pass
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': round((completed / total * 100), 1) if total > 0 else 0,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'overdue': overdue
    }

@app.route('/')
def index():
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    weather_data = get_weather(city)
    
    filtered_todos = todos
    if filter_priority:
        if filter_priority == 'overdue':
            filtered_todos = []
            for todo in todos:
                if todo.get('due_date'):
                    try:
                        due_date = datetime.strptime(todo['due_date'], '%Y-%m-%dT%H:%M')
                        if due_date < datetime.now() and not todo.get('completed', False):
                            filtered_todos.append(todo)
                    except:
                        pass
        else:
            filtered_todos = [todo for todo in todos if todo.get('priority') == filter_priority]
    
    sorted_todos = sorted(
        filtered_todos, 
        key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
    )
    
    stats = get_todo_statistics()
    
    return render_template(
        'index.html', 
        todos=sorted_todos, 
        weather=weather_data, 
        current_city=city, 
        current_filter=filter_priority,
        stats=stats,
        user=None
    )

@app.route('/advanced')
def advanced_index():
    city = request.args.get('city', 'Istanbul')
    filter_priority = request.args.get('filter')
    
    weather_data = get_weather(city)
    
    filtered_todos = todos
    if filter_priority:
        if filter_priority == 'overdue':
            filtered_todos = []
            for todo in todos:
                if todo.get('due_date'):
                    try:
                        due_date = datetime.strptime(todo['due_date'], '%Y-%m-%dT%H:%M')
                        if due_date < datetime.now() and not todo.get('completed', False):
                            filtered_todos.append(todo)
                    except:
                        pass
        else:
            filtered_todos = [todo for todo in todos if todo.get('priority') == filter_priority]
    
    sorted_todos = sorted(
        filtered_todos, 
        key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
    )
    
    stats = get_todo_statistics()
    
    return render_template(
        'advanced_index.html', 
        todos=sorted_todos, 
        weather=weather_data, 
        current_city=city, 
        current_filter=filter_priority,
        stats=stats,
        categories=categories,
        user=None
    )

@app.route('/add', methods=['POST'])
def add_todo():
    global todo_counter
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    
    if not validate_todo_text(todo_text):
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
    return redirect(url_for('index'))

@app.route('/add_advanced_todo', methods=['POST'])
def add_advanced_todo():
    global todo_counter
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    category_id = request.form.get('category_id')
    description = request.form.get('description', '')
    due_date = request.form.get('due_date')
    tags = request.form.get('tags', '')
    
    if not validate_todo_text(todo_text):
        return redirect(url_for('advanced_index'))
    
    todo_counter += 1
    new_todo = {
        'id': todo_counter,
        'text': todo_text,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'description': description,
        'due_date': due_date,
        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
        'category_id': int(category_id) if category_id else None
    }
    
    todos.append(new_todo)
    return redirect(url_for('advanced_index'))

@app.route('/add_category', methods=['POST'])
def add_category():
    global category_counter
    name = request.form.get('name')
    color = request.form.get('color', '#007bff')
    
    if not name:
        return redirect(url_for('advanced_index'))
    
    if not color.startswith('#'):
        color = '#' + color
    
    category_counter += 1
    new_category = {
        'id': category_counter,
        'name': name,
        'color': color
    }
    
    categories.append(new_category)
    return redirect(url_for('advanced_index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    referer = request.headers.get('Referer', '')
    if '/advanced' in referer:
        return redirect(url_for('advanced_index'))
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    referer = request.headers.get('Referer', '')
    if '/advanced' in referer:
        return redirect(url_for('advanced_index'))
    return redirect(url_for('index'))

@app.route('/weather')
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

if __name__ == '__main__':
    app.run(debug=True)
