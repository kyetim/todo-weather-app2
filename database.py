"""
Veritabanı Yönetimi
Supabase PostgreSQL entegrasyonu
"""

import os
from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class DatabaseManager:
    """
    Supabase veritabanı yönetim sınıfı
    """
    
    def __init__(self):
        """Veritabanı bağlantısını başlat"""
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL ve SUPABASE_KEY environment variables gerekli!")
        
        self.supabase: Client = create_client(self.url, self.key)
    
    def create_user(self, username: str, email: str) -> Dict:
        """
        Yeni kullanıcı oluştur
        
        Args:
            username (str): Kullanıcı adı
            email (str): E-posta adresi
        
        Returns:
            dict: Oluşturulan kullanıcı bilgileri
        """
        try:
            user_data = {
                'username': username,
                'email': email
            }
            
            result = self.supabase.table('users').insert(user_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Kullanıcı adına göre kullanıcı getir
        
        Args:
            username (str): Kullanıcı adı
        
        Returns:
            dict: Kullanıcı bilgileri veya None
        """
        try:
            result = self.supabase.table('users').select('*').eq('username', username).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Kullanıcı getirme hatası: {e}")
            return None
    
    def create_todo(self, user_id: str, text: str, priority: str = 'orta') -> Dict:
        """
        Yeni todo oluştur
        
        Args:
            user_id (str): Kullanıcı ID'si
            text (str): Todo metni
            priority (str): Öncelik seviyesi
        
        Returns:
            dict: Oluşturulan todo bilgileri
        """
        try:
            todo_data = {
                'user_id': user_id,
                'text': text,
                'priority': priority,
                'completed': False
            }
            
            result = self.supabase.table('todos').insert(todo_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Todo oluşturma hatası: {e}")
            return None
    
    def get_user_todos(self, user_id: str) -> List[Dict]:
        """
        Kullanıcının todo'larını getir
        
        Args:
            user_id (str): Kullanıcı ID'si
        
        Returns:
            list: Todo listesi
        """
        try:
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Todo'ları getirme hatası: {e}")
            return []
    
    def update_todo(self, todo_id: str, **kwargs) -> bool:
        """
        Todo güncelle
        
        Args:
            todo_id (str): Todo ID'si
            **kwargs: Güncellenecek alanlar
        
        Returns:
            bool: Güncelleme başarılı mı?
        """
        try:
            result = self.supabase.table('todos').update(kwargs).eq('id', todo_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Todo güncelleme hatası: {e}")
            return False
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        Todo sil
        
        Args:
            todo_id (str): Todo ID'si
        
        Returns:
            bool: Silme başarılı mı?
        """
        try:
            result = self.supabase.table('todos').delete().eq('id', todo_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Todo silme hatası: {e}")
            return False
    
    def toggle_todo_complete(self, todo_id: str) -> bool:
        """
        Todo tamamla/tamamlanmamış yap
        
        Args:
            todo_id (str): Todo ID'si
        
        Returns:
            bool: İşlem başarılı mı?
        """
        try:
            # Önce mevcut durumu al
            result = self.supabase.table('todos').select('completed').eq('id', todo_id).execute()
            if not result.data:
                return False
            
            current_status = result.data[0]['completed']
            new_status = not current_status
            
            # Durumu güncelle
            update_result = self.supabase.table('todos').update({'completed': new_status}).eq('id', todo_id).execute()
            return len(update_result.data) > 0
        except Exception as e:
            print(f"Todo durum güncelleme hatası: {e}")
            return False
    
    def get_todos_by_priority(self, user_id: str, priority: str) -> List[Dict]:
        """
        Önceliğe göre todo'ları getir
        
        Args:
            user_id (str): Kullanıcı ID'si
            priority (str): Öncelik seviyesi
        
        Returns:
            list: Filtrelenmiş todo listesi
        """
        try:
            result = self.supabase.table('todos').select('*').eq('user_id', user_id).eq('priority', priority).order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Öncelik bazlı todo getirme hatası: {e}")
            return []
    
    def get_todo_statistics(self, user_id: str) -> Dict:
        """
        Kullanıcının todo istatistiklerini hesapla
        
        Args:
            user_id (str): Kullanıcı ID'si
        
        Returns:
            dict: İstatistik verileri
        """
        try:
            todos = self.get_user_todos(user_id)
            
            total = len(todos)
            completed = len([todo for todo in todos if todo.get('completed', False)])
            pending = total - completed
            
            # Öncelik bazlı istatistikler
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
        except Exception as e:
            print(f"İstatistik hesaplama hatası: {e}")
            return {
                'total': 0,
                'completed': 0,
                'pending': 0,
                'completion_rate': 0,
                'high_priority': 0,
                'medium_priority': 0,
                'low_priority': 0
            }

# Global veritabanı yöneticisi
db_manager = DatabaseManager()
