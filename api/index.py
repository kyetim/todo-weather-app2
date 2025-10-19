import sys
import os

# Proje kök dizinini Python path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_simple import app

# Vercel için WSGI uygulaması
handler = app
