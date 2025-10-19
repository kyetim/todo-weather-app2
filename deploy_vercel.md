# Vercel Deployment Rehberi

## 1. Vercel CLI Kurulumu
```bash
npm i -g vercel
```

## 2. Vercel'e Giriş
```bash
vercel login
```

## 3. Proje Deploy Etme
```bash
vercel
```

## 4. Environment Variables Ayarlama
Vercel dashboard'da aşağıdaki environment variables'ları ekleyin:

- `WEATHER_API_KEY`: OpenWeatherMap API anahtarınız
- `SECRET_KEY`: Flask secret key (opsiyonel)

## 5. Production URL
Deployment tamamlandıktan sonra Vercel size bir URL verecek.

## Önemli Notlar:
- `api/index.py` dosyası Vercel'in Python runtime'ı için gerekli
- `vercel.json` dosyası routing'i yönetir
- `requirements_vercel.txt` sadece gerekli paketleri içerir
- Static dosyalar otomatik olarak serve edilir
