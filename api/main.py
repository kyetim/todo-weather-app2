from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from datetime import datetime
import requests

# Point Flask to project-level templates and static directories using absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'templates'))
STATIC_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'static'))

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# In-memory user store: username -> per-user state
USERS = {}

def get_current_username():
    return session.get('username')

def ensure_user(username):
    if username not in USERS:
        USERS[username] = {
            'todos': [],
            'todo_counter': 0,
            'categories': [
                {'id': 1, 'name': 'Genel', 'color': '#007bff'},
                {'id': 2, 'name': 'İş', 'color': '#28a745'},
                {'id': 3, 'name': 'Kişisel', 'color': '#ffc107'},
                {'id': 4, 'name': 'Acil', 'color': '#dc3545'}
            ],
            'category_counter': 4,
        }

def require_login_redirect():
    username = get_current_username()
    if not username:
        return redirect(url_for('login'))
    return None

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
    # auth gate
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    try:
        city = request.args.get('city', 'Istanbul')
        filter_priority = request.args.get('filter')
        weather_data = get_weather(city)

        filtered_todos = user_state['todos']
        if filter_priority:
            if filter_priority == 'overdue':
                filtered_todos = []
                for todo in user_state['todos']:
                    if todo.get('due_date'):
                        try:
                            due_date = datetime.strptime(todo['due_date'], '%Y-%m-%dT%H:%M')
                            if due_date < datetime.now() and not todo.get('completed', False):
                                filtered_todos.append(todo)
                        except:
                            pass
            else:
                filtered_todos = [todo for todo in user_state['todos'] if todo.get('priority') == filter_priority]

        sorted_todos = sorted(
            filtered_todos,
            key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
        )

        # compute stats for this user
        todos_ref = user_state['todos']
        total = len(todos_ref)
        completed = len([t for t in todos_ref if t.get('completed')])
        pending = total - completed
        high_priority = len([t for t in todos_ref if t.get('priority') == 'yüksek'])
        medium_priority = len([t for t in todos_ref if t.get('priority') == 'orta'])
        low_priority = len([t for t in todos_ref if t.get('priority') == 'düşük'])
        overdue = 0
        for t in todos_ref:
            if t.get('due_date'):
                try:
                    due_date = datetime.strptime(t['due_date'], '%Y-%m-%dT%H:%M')
                    if due_date < datetime.now() and not t.get('completed', False):
                        overdue += 1
                except:
                    pass
        stats = {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': round((completed / total * 100), 1) if total > 0 else 0,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'overdue': overdue
        }

        return render_template(
            'index.html',
            todos=sorted_todos,
            weather=weather_data,
            current_city=city,
            current_filter=filter_priority,
            stats=stats,
            user=username
        )
    except Exception as e:
        app.logger.exception('Index route failed')
        return jsonify({
            'error': str(e),
            'hint': 'Template render failed',
            'template_dir': TEMPLATE_DIR,
            'static_dir': STATIC_DIR
        }), 500

@app.route('/advanced')
def advanced_index():
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    try:
        city = request.args.get('city', 'Istanbul')
        filter_priority = request.args.get('filter')
        weather_data = get_weather(city)

        filtered_todos = user_state['todos']
        if filter_priority:
            if filter_priority == 'overdue':
                filtered_todos = []
                for todo in user_state['todos']:
                    if todo.get('due_date'):
                        try:
                            due_date = datetime.strptime(todo['due_date'], '%Y-%m-%dT%H:%M')
                            if due_date < datetime.now() and not todo.get('completed', False):
                                filtered_todos.append(todo)
                        except:
                            pass
            else:
                filtered_todos = [todo for todo in user_state['todos'] if todo.get('priority') == filter_priority]

        sorted_todos = sorted(
            filtered_todos,
            key=lambda x: (get_priority_order(x.get('priority', 'orta')), x.get('created_at', ''))
        )

        # same stats as index for this user
        todos_ref = user_state['todos']
        total = len(todos_ref)
        completed = len([t for t in todos_ref if t.get('completed')])
        pending = total - completed
        high_priority = len([t for t in todos_ref if t.get('priority') == 'yüksek'])
        medium_priority = len([t for t in todos_ref if t.get('priority') == 'orta'])
        low_priority = len([t for t in todos_ref if t.get('priority') == 'düşük'])
        overdue = 0
        for t in todos_ref:
            if t.get('due_date'):
                try:
                    due_date = datetime.strptime(t['due_date'], '%Y-%m-%dT%H:%M')
                    if due_date < datetime.now() and not t.get('completed', False):
                        overdue += 1
                except:
                    pass
        stats = {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': round((completed / total * 100), 1) if total > 0 else 0,
            'high_priority': high_priority,
            'medium_priority': medium_priority,
            'low_priority': low_priority,
            'overdue': overdue
        }

        return render_template(
            'advanced_index.html',
            todos=sorted_todos,
            weather=weather_data,
            current_city=city,
            current_filter=filter_priority,
            stats=stats,
            categories=user_state['categories'],
            user=username
        )
    except Exception as e:
        app.logger.exception('Advanced index route failed')
        return jsonify({
            'error': str(e),
            'hint': 'Template render failed',
            'template_dir': TEMPLATE_DIR,
            'static_dir': STATIC_DIR
        }), 500

@app.route('/add', methods=['POST'])
def add_todo():
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    
    if not validate_todo_text(todo_text):
        return redirect(url_for('index'))
    
    user_state['todo_counter'] += 1
    new_todo = {
        'id': user_state['todo_counter'],
        'text': todo_text,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    user_state['todos'].append(new_todo)
    return redirect(url_for('index'))

@app.route('/add_advanced_todo', methods=['POST'])
def add_advanced_todo():
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    todo_text = request.form.get('todo')
    priority = request.form.get('priority', 'orta')
    category_id = request.form.get('category_id')
    description = request.form.get('description', '')
    due_date = request.form.get('due_date')
    tags = request.form.get('tags', '')
    
    if not validate_todo_text(todo_text):
        return redirect(url_for('advanced_index'))
    
    user_state['todo_counter'] += 1
    new_todo = {
        'id': user_state['todo_counter'],
        'text': todo_text,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'description': description,
        'due_date': due_date,
        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
        'category_id': int(category_id) if category_id else None
    }
    user_state['todos'].append(new_todo)
    return redirect(url_for('advanced_index'))

@app.route('/add_category', methods=['POST'])
def add_category():
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    name = request.form.get('name')
    color = request.form.get('color', '#007bff')
    
    if not name:
        return redirect(url_for('advanced_index'))
    
    if not color.startswith('#'):
        color = '#' + color
    
    user_state['category_counter'] += 1
    new_category = {
        'id': user_state['category_counter'],
        'name': name,
        'color': color
    }
    user_state['categories'].append(new_category)
    return redirect(url_for('advanced_index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    for todo in user_state['todos']:
        if todo['id'] == todo_id:
            todo['completed'] = not todo['completed']
            break
    referer = request.headers.get('Referer', '')
    if '/advanced' in referer:
        return redirect(url_for('advanced_index'))
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    gate = require_login_redirect()
    if gate:
        return gate
    username = get_current_username()
    ensure_user(username)
    user_state = USERS[username]
    user_state['todos'] = [todo for todo in user_state['todos'] if todo['id'] != todo_id]
    referer = request.headers.get('Referer', '')
    if '/advanced' in referer:
        return redirect(url_for('advanced_index'))
    return redirect(url_for('index'))

@app.route('/weather')
def weather():
    city = request.args.get('city', 'Istanbul')
    weather_data = get_weather(city)
    return render_template('weather.html', weather=weather_data, current_city=city)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        if not username:
            return render_template('login.html')
        session['username'] = username
        ensure_user(username)
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    username = get_current_username()
    if not username or username not in USERS:
        return jsonify({'success': False, 'error': 'auth required'}), 401
    todos_ref = USERS[username]['todos']
    return jsonify({'success': True, 'data': todos_ref, 'count': len(todos_ref)})

@app.route('/api/todos', methods=['POST'])
def api_create_todo():
    username = get_current_username()
    if not username or username not in USERS:
        return jsonify({'success': False, 'error': 'auth required'}), 401
    user_state = USERS[username]
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Text field required'}), 400
    
    user_state['todo_counter'] += 1
    priority = data.get('priority', 'orta')
    new_todo = {
        'id': user_state['todo_counter'],
        'text': data['text'],
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    user_state['todos'].append(new_todo)
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
    return ("Not Found", 404)

@app.errorhandler(500)
def internal_error(error):
    return ("Internal Server Error", 500)

@app.route('/health')
def health():
    return jsonify({"ok": True}), 200

@app.route('/favicon.ico')
def favicon_ico():
    # Return 204 to avoid error spam when no favicon exists
    return ('', 204)

@app.route('/favicon.png')
def favicon_png():
    # Return 204 to avoid error spam when no favicon exists
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
