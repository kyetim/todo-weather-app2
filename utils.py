"""
Yardımcı Fonksiyonlar
Python Flask Uygulaması için yardımcı fonksiyonlar
"""

from datetime import datetime
import requests
import os

def get_priority_order(priority):
    """
    Öncelik sıralaması için sayısal değer döndür
    
    Args:
        priority (str): Öncelik seviyesi (yüksek, orta, düşük)
    
    Returns:
        int: Sıralama için sayısal değer
    """
    priority_order = {'yüksek': 1, 'orta': 2, 'düşük': 3}
    return priority_order.get(priority, 2)

def get_weather_data(city, api_key):
    """
    Hava durumu bilgilerini API'den al
    
    Args:
        city (str): Şehir adı
        api_key (str): OpenWeatherMap API anahtarı
    
    Returns:
        dict: Hava durumu bilgileri veya None
    """
    # Demo modu - API anahtarı yoksa demo veri döndür
    if api_key == 'demo-key':
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
            'appid': api_key,
            'units': 'metric',
            'lang': 'tr'
        }
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
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
    except Exception as e:
        print(f"Hava durumu API hatası: {e}")
        return None

def format_datetime():
    """
    Mevcut tarih ve saati formatla
    
    Returns:
        str: Formatlanmış tarih ve saat
    """
    return datetime.now().strftime('%d.%m.%Y %H:%M')

def validate_todo_text(text):
    """
    Todo metnini doğrula
    
    Args:
        text (str): Todo metni
    
    Returns:
        bool: Geçerli mi?
    """
    if not text or not text.strip():
        return False
    if len(text.strip()) < 2:
        return False
    if len(text.strip()) > 500:
        return False
    return True

def get_todo_statistics(todos):
    """
    Todo istatistiklerini hesapla
    
    Args:
        todos (list): Todo listesi
    
    Returns:
        dict: İstatistik verileri
    """
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
