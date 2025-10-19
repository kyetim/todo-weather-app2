#!/usr/bin/env python3
"""
Todo & Hava Durumu Uygulaması - Ana Giriş Noktası
Python Flask Web Uygulaması

Bu dosya uygulamanın ana giriş noktasıdır.
Vercel deployment için gerekli.
"""

from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
