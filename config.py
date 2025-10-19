"""
Konfigürasyon Dosyası
Python Flask Uygulaması için ayarlar
"""

import os

class Config:
    """Uygulama konfigürasyon sınıfı"""
    
    # Flask ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Hava durumu API ayarları
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'e73f50fbc7e75e1594e9c58d5a2f451e'
    WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'
    
    # Veritabanı ayarları (gelecekte kullanım için)
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Debug modu
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    """Geliştirme ortamı konfigürasyonu"""
    DEBUG = True

class ProductionConfig(Config):
    """Üretim ortamı konfigürasyonu"""
    DEBUG = False

# Konfigürasyon sözlüğü
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
