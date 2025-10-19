"""
Gelişmiş Veri Modelleri
Orta seviye Python OOP özellikleri
"""

from datetime import datetime, date
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum
import uuid

class Priority(Enum):
    """Öncelik seviyeleri enum"""
    LOW = 'düşük'
    MEDIUM = 'orta'
    HIGH = 'yüksek'

class Status(Enum):
    """Todo durumları enum"""
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

@dataclass
class User:
    """Kullanıcı modeli - Dataclass kullanımı"""
    id: str
    username: str
    email: str
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        """Dataclass post-init method"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Kullanıcıyı sözlük olarak döndür"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_last_login(self):
        """Son giriş zamanını güncelle"""
        self.last_login = datetime.now()
        self.updated_at = datetime.now()

@dataclass
class Category:
    """Kategori modeli"""
    id: str
    user_id: str
    name: str
    color: str = '#007bff'
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@dataclass
class Todo:
    """Gelişmiş Todo modeli"""
    id: str
    user_id: str
    category_id: Optional[str] = None
    text: str = ""
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    completed: bool = False
    due_date: Optional[datetime] = None
    tags: List[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Todo'yu sözlük olarak döndür"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'text': self.text,
            'description': self.description,
            'priority': self.priority.value,
            'status': self.status.value,
            'completed': self.completed,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def toggle_complete(self):
        """Todo'yu tamamla/tamamlanmamış yap"""
        self.completed = not self.completed
        if self.completed:
            self.status = Status.COMPLETED
        else:
            self.status = Status.PENDING
        self.updated_at = datetime.now()
    
    def update_text(self, new_text: str):
        """Todo metnini güncelle"""
        self.text = new_text
        self.updated_at = datetime.now()
    
    def update_priority(self, new_priority: Priority):
        """Todo önceliğini güncelle"""
        self.priority = new_priority
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Etiket ekle"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """Etiket kaldır"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Todo süresi geçmiş mi?"""
        if not self.due_date:
            return False
        return datetime.now() > self.due_date and not self.completed
    
    def days_until_due(self) -> Optional[int]:
        """Kaç gün kaldı?"""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.now()
        return delta.days

@dataclass
class WeatherRecord:
    """Hava durumu kaydı modeli"""
    id: str
    user_id: str
    city: str
    temperature: float
    description: str
    humidity: int
    icon: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'city': self.city,
            'temperature': self.temperature,
            'description': self.description,
            'humidity': self.humidity,
            'icon': self.icon,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TodoManager:
    """Gelişmiş Todo yöneticisi sınıfı"""
    
    def __init__(self):
        self.todos: List[Todo] = []
        self.categories: List[Category] = []
        self.next_id = 1
    
    def create_todo(self, user_id: str, text: str, **kwargs) -> Todo:
        """Yeni todo oluştur"""
        todo = Todo(
            id=str(uuid.uuid4()),
            user_id=user_id,
            text=text,
            **kwargs
        )
        self.todos.append(todo)
        return todo
    
    def create_category(self, user_id: str, name: str, color: str = '#007bff') -> Category:
        """Yeni kategori oluştur"""
        category = Category(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            color=color
        )
        self.categories.append(category)
        return category
    
    def get_user_todos(self, user_id: str) -> List[Todo]:
        """Kullanıcının todo'larını getir"""
        return [todo for todo in self.todos if todo.user_id == user_id]
    
    def get_user_categories(self, user_id: str) -> List[Category]:
        """Kullanıcının kategorilerini getir"""
        return [cat for cat in self.categories if cat.user_id == user_id]
    
    def get_todos_by_priority(self, user_id: str, priority: Priority) -> List[Todo]:
        """Önceliğe göre todo'ları getir"""
        return [todo for todo in self.get_user_todos(user_id) if todo.priority == priority]
    
    def get_todos_by_category(self, user_id: str, category_id: str) -> List[Todo]:
        """Kategoriye göre todo'ları getir"""
        return [todo for todo in self.get_user_todos(user_id) if todo.category_id == category_id]
    
    def get_overdue_todos(self, user_id: str) -> List[Todo]:
        """Süresi geçmiş todo'ları getir"""
        return [todo for todo in self.get_user_todos(user_id) if todo.is_overdue()]
    
    def search_todos(self, user_id: str, query: str) -> List[Todo]:
        """Todo'ları ara"""
        user_todos = self.get_user_todos(user_id)
        query_lower = query.lower()
        return [
            todo for todo in user_todos 
            if query_lower in todo.text.lower() or 
               (todo.description and query_lower in todo.description.lower()) or
               any(query_lower in tag.lower() for tag in todo.tags)
        ]
    
    def get_todo_statistics(self, user_id: str) -> Dict:
        """Gelişmiş istatistikler"""
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
