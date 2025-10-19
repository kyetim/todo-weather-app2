"""
Kullanıcı Oturum Yönetimi
Flask-Login entegrasyonu
"""

from flask import session, request, redirect, url_for, flash
from functools import wraps
from database import db_manager
import uuid

def login_required(f):
    """
    Giriş yapmış kullanıcı kontrolü decorator'ı
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfaya erişmek için giriş yapmalısınız!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    Mevcut kullanıcı bilgilerini getir
    
    Returns:
        dict: Kullanıcı bilgileri veya None
    """
    if 'user_id' not in session:
        return None
    
    user_id = session['user_id']
    return db_manager.get_user_by_username(session.get('username'))

def login_user(username: str, email: str = None):
    """
    Kullanıcıyı oturum aç
    
    Args:
        username (str): Kullanıcı adı
        email (str): E-posta adresi (opsiyonel)
    
    Returns:
        bool: Giriş başarılı mı?
    """
    try:
        # Kullanıcıyı veritabanında ara
        user = db_manager.get_user_by_username(username)
        
        if not user:
            # Kullanıcı yoksa oluştur
            if email:
                user = db_manager.create_user(username, email)
            else:
                # Demo kullanıcı oluştur
                user = db_manager.create_user(username, f"{username}@demo.com")
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            return True
        
        return False
    except Exception as e:
        print(f"Kullanıcı giriş hatası: {e}")
        return False

def logout_user():
    """
    Kullanıcıyı oturumdan çıkar
    """
    session.clear()
    flash('Başarıyla çıkış yaptınız!', 'info')

def is_logged_in():
    """
    Kullanıcı giriş yapmış mı?
    
    Returns:
        bool: Giriş durumu
    """
    return 'user_id' in session

def get_user_todos():
    """
    Mevcut kullanıcının todo'larını getir
    
    Returns:
        list: Todo listesi
    """
    if not is_logged_in():
        return []
    
    user_id = session['user_id']
    return db_manager.get_user_todos(user_id)

def create_user_todo(text: str, priority: str = 'orta'):
    """
    Mevcut kullanıcı için todo oluştur
    
    Args:
        text (str): Todo metni
        priority (str): Öncelik seviyesi
    
    Returns:
        dict: Oluşturulan todo veya None
    """
    if not is_logged_in():
        return None
    
    user_id = session['user_id']
    return db_manager.create_todo(user_id, text, priority)

def update_user_todo(todo_id: str, **kwargs):
    """
    Mevcut kullanıcının todo'sunu güncelle
    
    Args:
        todo_id (str): Todo ID'si
        **kwargs: Güncellenecek alanlar
    
    Returns:
        bool: Güncelleme başarılı mı?
    """
    if not is_logged_in():
        return False
    
    # Todo'nun kullanıcıya ait olduğunu kontrol et
    user_todos = get_user_todos()
    todo_exists = any(todo['id'] == todo_id for todo in user_todos)
    
    if not todo_exists:
        return False
    
    return db_manager.update_todo(todo_id, **kwargs)

def delete_user_todo(todo_id: str):
    """
    Mevcut kullanıcının todo'sunu sil
    
    Args:
        todo_id (str): Todo ID'si
    
    Returns:
        bool: Silme başarılı mı?
    """
    if not is_logged_in():
        return False
    
    # Todo'nun kullanıcıya ait olduğunu kontrol et
    user_todos = get_user_todos()
    todo_exists = any(todo['id'] == todo_id for todo in user_todos)
    
    if not todo_exists:
        return False
    
    return db_manager.delete_todo(todo_id)

def toggle_user_todo(todo_id: str):
    """
    Mevcut kullanıcının todo'sunu tamamla/tamamlanmamış yap
    
    Args:
        todo_id (str): Todo ID'si
    
    Returns:
        bool: İşlem başarılı mı?
    """
    if not is_logged_in():
        return False
    
    # Todo'nun kullanıcıya ait olduğunu kontrol et
    user_todos = get_user_todos()
    todo_exists = any(todo['id'] == todo_id for todo in user_todos)
    
    if not todo_exists:
        return False
    
    return db_manager.toggle_todo_complete(todo_id)

def get_user_todos_by_priority(priority: str):
    """
    Mevcut kullanıcının önceliğe göre todo'larını getir
    
    Args:
        priority (str): Öncelik seviyesi
    
    Returns:
        list: Filtrelenmiş todo listesi
    """
    if not is_logged_in():
        return []
    
    user_id = session['user_id']
    return db_manager.get_todos_by_priority(user_id, priority)

def get_user_statistics():
    """
    Mevcut kullanıcının todo istatistiklerini getir
    
    Returns:
        dict: İstatistik verileri
    """
    if not is_logged_in():
        return {
            'total': 0,
            'completed': 0,
            'pending': 0,
            'completion_rate': 0,
            'high_priority': 0,
            'medium_priority': 0,
            'low_priority': 0
        }
    
    user_id = session['user_id']
    return db_manager.get_todo_statistics(user_id)
