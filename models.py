"""
Veri Modelleri
Python Flask Uygulaması için veri modelleri
"""

from datetime import datetime
from typing import Dict, List, Optional

class Todo:
    """
    Todo sınıfı - Görev modeli
    """
    
    def __init__(self, text: str, priority: str = 'orta', todo_id: int = None):
        """
        Todo nesnesi oluştur
        
        Args:
            text (str): Todo metni
            priority (str): Öncelik seviyesi
            todo_id (int): Todo ID'si
        """
        self.id = todo_id
        self.text = text
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now().strftime('%d.%m.%Y %H:%M')
        self.updated_at = None
    
    def to_dict(self) -> Dict:
        """
        Todo nesnesini sözlük olarak döndür
        
        Returns:
            dict: Todo verileri
        """
        return {
            'id': self.id,
            'text': self.text,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def toggle_complete(self):
        """Todo'yu tamamla/tamamlanmamış yap"""
        self.completed = not self.completed
        self.updated_at = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    def update_text(self, new_text: str):
        """
        Todo metnini güncelle
        
        Args:
            new_text (str): Yeni metin
        """
        self.text = new_text
        self.updated_at = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    def update_priority(self, new_priority: str):
        """
        Todo önceliğini güncelle
        
        Args:
            new_priority (str): Yeni öncelik
        """
        self.priority = new_priority
        self.updated_at = datetime.now().strftime('%d.%m.%Y %H:%M')

class WeatherData:
    """
    Hava durumu veri modeli
    """
    
    def __init__(self, city: str, temperature: float, description: str, 
                 humidity: int, icon: str):
        """
        Hava durumu nesnesi oluştur
        
        Args:
            city (str): Şehir adı
            temperature (float): Sıcaklık
            description (str): Açıklama
            humidity (int): Nem oranı
            icon (str): İkon kodu
        """
        self.city = city
        self.temperature = temperature
        self.description = description
        self.humidity = humidity
        self.icon = icon
        self.timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    def to_dict(self) -> Dict:
        """
        Hava durumu verilerini sözlük olarak döndür
        
        Returns:
            dict: Hava durumu verileri
        """
        return {
            'city': self.city,
            'temperature': self.temperature,
            'description': self.description,
            'humidity': self.humidity,
            'icon': self.icon,
            'timestamp': self.timestamp
        }

class TodoManager:
    """
    Todo yönetim sınıfı
    """
    
    def __init__(self):
        """Todo yöneticisi oluştur"""
        self.todos: List[Todo] = []
        self.next_id = 1
    
    def add_todo(self, text: str, priority: str = 'orta') -> Todo:
        """
        Yeni todo ekle
        
        Args:
            text (str): Todo metni
            priority (str): Öncelik seviyesi
        
        Returns:
            Todo: Eklenen todo nesnesi
        """
        todo = Todo(text, priority, self.next_id)
        self.todos.append(todo)
        self.next_id += 1
        return todo
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        ID'ye göre todo getir
        
        Args:
            todo_id (int): Todo ID'si
        
        Returns:
            Todo: Todo nesnesi veya None
        """
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None
    
    def delete_todo(self, todo_id: int) -> bool:
        """
        Todo sil
        
        Args:
            todo_id (int): Todo ID'si
        
        Returns:
            bool: Silme başarılı mı?
        """
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                del self.todos[i]
                return True
        return False
    
    def get_all_todos(self) -> List[Dict]:
        """
        Tüm todo'ları getir
        
        Returns:
            list: Todo sözlükleri listesi
        """
        return [todo.to_dict() for todo in self.todos]
    
    def get_todos_by_priority(self, priority: str) -> List[Dict]:
        """
        Önceliğe göre todo'ları getir
        
        Args:
            priority (str): Öncelik seviyesi
        
        Returns:
            list: Filtrelenmiş todo listesi
        """
        filtered_todos = [todo for todo in self.todos if todo.priority == priority]
        return [todo.to_dict() for todo in filtered_todos]
