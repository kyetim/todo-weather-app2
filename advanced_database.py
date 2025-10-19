"""
Gelişmiş Veritabanı Yönetimi
Orta seviye Python özellikleri ile
"""

import os
from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime
import uuid
from advanced_models import User, Category, Todo, WeatherRecord, Priority, Status

class AdvancedDatabaseManager:
    """
    Gelişmiş veritabanı yönetim sınıfı
    Orta seviye Python OOP özellikleri
    """
    
    def __init__(self):
        """Veritabanı bağlantısını başlat"""
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL ve SUPABASE_KEY environment variables gerekli!")
        
        self.supabase: Client = create_client(self.url, self.key)
    
    # Kullanıcı işlemleri
    def create_user(self, username: str, email: str) -> Optional[User]:
        """Yeni kullanıcı oluştur"""
        try:
            user_data = {
                'username': username,
                'email': email,
                'is_active': True
            }
            
            result = self.supabase.table('users').insert(user_data).execute()
            if result.data:
                user_dict = result.data[0]
                return User(
                    id=user_dict['id'],
                    username=user_dict['username'],
                    email=user_dict['email'],
                    is_active=user_dict['is_active'],
                    created_at=datetime.fromisoformat(user_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(user_dict['updated_at'].replace('Z', '+00:00'))
                )
            return None
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Kullanıcı adına göre kullanıcı getir"""
        try:
            result = self.supabase.table('users').select('*').eq('username', username).execute()
            if result.data:
                user_dict = result.data[0]
                return User(
                    id=user_dict['id'],
                    username=user_dict['username'],
                    email=user_dict['email'],
                    is_active=user_dict['is_active'],
                    last_login=datetime.fromisoformat(user_dict['last_login'].replace('Z', '+00:00')) if user_dict['last_login'] else None,
                    created_at=datetime.fromisoformat(user_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(user_dict['updated_at'].replace('Z', '+00:00'))
                )
            return None
        except Exception as e:
            print(f"Kullanıcı getirme hatası: {e}")
            return None
    
    # Kategori işlemleri
    def create_category(self, user_id: str, name: str, color: str = '#007bff') -> Optional[Category]:
        """Yeni kategori oluştur"""
        try:
            category_data = {
                'user_id': user_id,
                'name': name,
                'color': color
            }
            
            result = self.supabase.table('categories').insert(category_data).execute()
            if result.data:
                cat_dict = result.data[0]
                return Category(
                    id=cat_dict['id'],
                    user_id=cat_dict['user_id'],
                    name=cat_dict['name'],
                    color=cat_dict['color'],
                    created_at=datetime.fromisoformat(cat_dict['created_at'].replace('Z', '+00:00'))
                )
            return None
        except Exception as e:
            print(f"Kategori oluşturma hatası: {e}")
            return None
    
    def get_user_categories(self, user_id: str) -> List[Category]:
        """Kullanıcının kategorilerini getir"""
        try:
            result = self.supabase.table('categories').select('*').eq('user_id', user_id).execute()
            categories = []
            for cat_dict in result.data:
                categories.append(Category(
                    id=cat_dict['id'],
                    user_id=cat_dict['user_id'],
                    name=cat_dict['name'],
                    color=cat_dict['color'],
                    created_at=datetime.fromisoformat(cat_dict['created_at'].replace('Z', '+00:00'))
                ))
            return categories
        except Exception as e:
            print(f"Kategoriler getirme hatası: {e}")
            return []
    
    # Todo işlemleri
    def create_todo(self, user_id: str, text: str, **kwargs) -> Optional[Todo]:
        """Yeni todo oluştur"""
        try:
            todo_data = {
                'user_id': user_id,
                'text': text,
                'description': kwargs.get('description'),
                'priority': kwargs.get('priority', 'orta'),
                'status': kwargs.get('status', 'pending'),
                'completed': kwargs.get('completed', False),
                'due_date': kwargs.get('due_date'),
                'tags': kwargs.get('tags', []),
                'category_id': kwargs.get('category_id')
            }
            
            result = self.supabase.table('todos').insert(todo_data).execute()
            if result.data:
                todo_dict = result.data[0]
                return Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                )
            return None
        except Exception as e:
            print(f"Todo oluşturma hatası: {e}")
            return None
    
    def get_user_todos(self, user_id: str) -> List[Todo]:
        """Kullanıcının todo'larını getir"""
        try:
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            todos = []
            for todo_dict in result.data:
                todos.append(Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                ))
            return todos
        except Exception as e:
            print(f"Todo'ları getirme hatası: {e}")
            return []
    
    def get_todos_by_priority(self, user_id: str, priority: str) -> List[Todo]:
        """Önceliğe göre todo'ları getir"""
        try:
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).eq('priority', priority).order('created_at', desc=True).execute()
            todos = []
            for todo_dict in result.data:
                todos.append(Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                ))
            return todos
        except Exception as e:
            print(f"Öncelik bazlı todo getirme hatası: {e}")
            return []
    
    def get_todos_by_category(self, user_id: str, category_id: str) -> List[Todo]:
        """Kategoriye göre todo'ları getir"""
        try:
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).eq('category_id', category_id).order('created_at', desc=True).execute()
            todos = []
            for todo_dict in result.data:
                todos.append(Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                ))
            return todos
        except Exception as e:
            print(f"Kategori bazlı todo getirme hatası: {e}")
            return []
    
    def update_todo(self, todo_id: str, **kwargs) -> bool:
        """Todo güncelle"""
        try:
            # Enum değerlerini string'e çevir
            if 'priority' in kwargs and isinstance(kwargs['priority'], Priority):
                kwargs['priority'] = kwargs['priority'].value
            if 'status' in kwargs and isinstance(kwargs['status'], Status):
                kwargs['status'] = kwargs['status'].value
            
            result = self.supabase.table('todos').update(kwargs).eq('id', todo_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Todo güncelleme hatası: {e}")
            return False
    
    def delete_todo(self, todo_id: str) -> bool:
        """Todo sil"""
        try:
            result = self.supabase.table('todos').delete().eq('id', todo_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Todo silme hatası: {e}")
            return False
    
    def toggle_todo_complete(self, todo_id: str) -> bool:
        """Todo tamamla/tamamlanmamış yap"""
        try:
            # Önce mevcut durumu al
            result = self.supabase.table('todos').select('completed').eq('id', todo_id).execute()
            if not result.data:
                return False
            
            current_status = result.data[0]['completed']
            new_status = not current_status
            
            # Durumu güncelle
            update_data = {'completed': new_status}
            if new_status:
                update_data['status'] = 'completed'
            else:
                update_data['status'] = 'pending'
            
            update_result = self.supabase.table('todos').update(update_data).eq('id', todo_id).execute()
            return len(update_result.data) > 0
        except Exception as e:
            print(f"Todo durum güncelleme hatası: {e}")
            return False
    
    def search_todos(self, user_id: str, query: str) -> List[Todo]:
        """Todo'ları ara"""
        try:
            # PostgreSQL full-text search kullanarak
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).text_search('text', query).execute()
            todos = []
            for todo_dict in result.data:
                todos.append(Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                ))
            return todos
        except Exception as e:
            print(f"Todo arama hatası: {e}")
            return []
    
    def get_overdue_todos(self, user_id: str) -> List[Todo]:
        """Süresi geçmiş todo'ları getir"""
        try:
            now = datetime.now().isoformat()
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).lt('due_date', now).eq('completed', False).execute()
            todos = []
            for todo_dict in result.data:
                todos.append(Todo(
                    id=todo_dict['id'],
                    user_id=todo_dict['user_id'],
                    category_id=todo_dict['category_id'],
                    text=todo_dict['text'],
                    description=todo_dict['description'],
                    priority=Priority(todo_dict['priority']),
                    status=Status(todo_dict['status']),
                    completed=todo_dict['completed'],
                    due_date=datetime.fromisoformat(todo_dict['due_date'].replace('Z', '+00:00')) if todo_dict['due_date'] else None,
                    tags=todo_dict['tags'] or [],
                    created_at=datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(todo_dict['updated_at'].replace('Z', '+00:00'))
                ))
            return todos
        except Exception as e:
            print(f"Süresi geçmiş todo getirme hatası: {e}")
            return []
    
    def get_todo_statistics(self, user_id: str) -> Dict:
        """Gelişmiş istatistikler"""
        try:
            todos = self.get_user_todos(user_id)
            
            total = len(todos)
            completed = len([t for t in todos if t.completed])
            pending = total - completed
            overdue = len(self.get_overdue_todos(user_id))
            
            # Öncelik bazlı istatistikler
            high_priority = len([t for t in todos if t.priority == Priority.HIGH])
            medium_priority = len([t for t in todos if t.priority == Priority.MEDIUM])
            low_priority = len([t for t in todos if t.priority == Priority.LOW])
            
            # Durum bazlı istatistikler
            in_progress = len([t for t in todos if t.status == Status.IN_PROGRESS])
            cancelled = len([t for t in todos if t.status == Status.CANCELLED])
            
            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'overdue': overdue,
                'completion_rate': round((completed / total * 100), 1) if total > 0 else 0,
                'high_priority': high_priority,
                'medium_priority': medium_priority,
                'low_priority': low_priority,
                'in_progress': in_progress,
                'cancelled': cancelled
            }
        except Exception as e:
            print(f"İstatistik hesaplama hatası: {e}")
            return {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'overdue': 0,
                'completion_rate': 0,
                'high_priority': 0,
                'medium_priority': 0,
                'low_priority': 0,
                'in_progress': 0,
                'cancelled': 0
            }
    
    def save_weather_record(self, user_id: str, city: str, weather_data: Dict) -> Optional[WeatherRecord]:
        """Hava durumu kaydı oluştur"""
        try:
            weather_record_data = {
                'user_id': user_id,
                'city': city,
                'temperature': weather_data.get('temperature'),
                'description': weather_data.get('description'),
                'humidity': weather_data.get('humidity'),
                'icon': weather_data.get('icon')
            }
            
            result = self.supabase.table('weather_history').insert(weather_record_data).execute()
            if result.data:
                record_dict = result.data[0]
                return WeatherRecord(
                    id=record_dict['id'],
                    user_id=record_dict['user_id'],
                    city=record_dict['city'],
                    temperature=record_dict['temperature'],
                    description=record_dict['description'],
                    humidity=record_dict['humidity'],
                    icon=record_dict['icon'],
                    created_at=datetime.fromisoformat(record_dict['created_at'].replace('Z', '+00:00'))
                )
            return None
        except Exception as e:
            print(f"Hava durumu kaydı oluşturma hatası: {e}")
            return None

# Global gelişmiş veritabanı yöneticisi
advanced_db_manager = AdvancedDatabaseManager()
