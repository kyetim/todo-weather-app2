"""
Todo & Hava Durumu Uygulaması
Python Flask Web Uygulaması

Bu paket Python Flask framework kullanılarak geliştirilmiş
bir todo listesi ve hava durumu uygulamasıdır.

Özellikler:
- Todo yönetimi (ekleme, tamamlama, silme)
- Öncelik seviyeleri (yüksek, orta, düşük)
- Hava durumu API entegrasyonu
- Responsive web tasarımı
- Modern UI/UX

Teknolojiler:
- Python 3.7+
- Flask 2.3.3
- HTML5, CSS3, JavaScript
- Bootstrap 5
- OpenWeatherMap API

Geliştirici: Kyetim
Lisans: MIT
"""

__version__ = "1.0.0"
__author__ = "Kyetim"
__email__ = "kyetim@example.com"
__description__ = "Python Flask Todo & Hava Durumu Uygulaması"

# Ana uygulama modülü
from app import app

# Konfigürasyon
from config import config

# Yardımcı fonksiyonlar
from utils import (
    get_priority_order,
    get_weather_data,
    format_datetime,
    validate_todo_text,
    get_todo_statistics
)

# Veri modelleri
from models import Todo, WeatherData, TodoManager

__all__ = [
    'app',
    'config',
    'get_priority_order',
    'get_weather_data',
    'format_datetime',
    'validate_todo_text',
    'get_todo_statistics',
    'Todo',
    'WeatherData',
    'TodoManager'
]
