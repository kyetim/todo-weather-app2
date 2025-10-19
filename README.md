# Todo & Hava Durumu Uygulaması

Bu proje, Python Flask framework kullanılarak geliştirilmiş bir todo listesi uygulamasıdır. Uygulama, kullanıcıların görevlerini yönetmelerine olanak tanırken aynı zamanda hava durumu bilgilerini de sunar.

## 🚀 Özellikler

- ✅ **Todo Yönetimi**: Görev ekleme, tamamlama ve silme
- 🌤️ **Hava Durumu**: Gerçek zamanlı hava durumu bilgileri
- 📱 **Responsive Tasarım**: Mobil ve masaüstü uyumlu
- 🎨 **Modern UI**: Bootstrap 5 ile güzel arayüz
- 📊 **İstatistikler**: Todo tamamlama oranları

## 🛠️ Teknolojiler

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **API**: OpenWeatherMap API
- **Icons**: Font Awesome
- **Deployment**: Vercel

## 📦 Kurulum

### Gereksinimler
- Python 3.7+
- pip (Python paket yöneticisi)

### Adımlar

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/kyetim/todo-weather-app2.git
cd todo-weather-app2
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv venv
```

3. **Sanal ortamı aktifleştirin:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

5. **OpenWeatherMap API anahtarı alın:**
   - [OpenWeatherMap](https://openweathermap.org/api) sitesine gidin
   - Ücretsiz hesap oluşturun
   - API anahtarınızı alın

6. **API anahtarını ayarlayın:**
   - `app.py` dosyasındaki `WEATHER_API_KEY` değişkenini güncelleyin

7. **Uygulamayı çalıştırın:**
```bash
python app.py
```

8. **Tarayıcınızda açın:**
   - http://localhost:5000 adresine gidin

## 🌐 Canlı Demo

Uygulama Vercel üzerinde canlı olarak çalışmaktadır:
[Demo Linki](https://todo-weather-app2.vercel.app)

## 📱 Kullanım

### Todo Yönetimi
- Ana sayfada "Yeni todo ekle" alanına görevinizi yazın
- "Ekle" butonuna tıklayın
- Tamamlanan görevleri işaretleyin
- Gereksiz görevleri silin

### Hava Durumu
- Şehir adını girin (örn: İstanbul, Ankara)
- Güncel hava durumu bilgilerini görün
- Detaylı hava durumu sayfasına gidin

## 🔧 API Kullanımı

Uygulama, hava durumu bilgileri için OpenWeatherMap API'sini kullanır:

```python
# API çağrısı örneği
def get_weather(city):
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }
    response = requests.get(WEATHER_API_URL, params=params)
    return response.json()
```

## 📁 Proje Yapısı

```
todo-weather-app2/
├── app.py                 # Ana Flask uygulaması
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Proje dokümantasyonu
├── templates/            # HTML şablonları
│   ├── base.html         # Temel şablon
│   ├── index.html        # Ana sayfa
│   └── weather.html      # Hava durumu sayfası
└── static/               # Statik dosyalar
    └── style.css         # Özel CSS stilleri
```

## 🚀 Deployment (Vercel)

1. **Vercel CLI yükleyin:**
```bash
npm i -g vercel
```

2. **Vercel'e giriş yapın:**
```bash
vercel login
```

3. **Projeyi deploy edin:**
```bash
vercel
```

4. **Environment variables ayarlayın:**
   - Vercel dashboard'da `WEATHER_API_KEY` değişkenini ekleyin

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**Kyetim** - Python Flask Todo & Hava Durumu Uygulaması

## 📞 İletişim

- GitHub: [@kyetim](https://github.com/kyetim)
- Proje Linki: [https://github.com/kyetim/todo-weather-app2](https://github.com/kyetim/todo-weather-app2)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
