# Todo & Hava Durumu Uygulaması
## 🎓 Python Eğitimi Bitirme Projesi

Bu proje, **Python eğitimi bitirme projesi** olarak geliştirilmiş kapsamlı bir web uygulamasıdır. Python Flask framework kullanılarak geliştirilmiş olan uygulama, kullanıcıların görevlerini yönetmelerine olanak tanırken aynı zamanda hava durumu bilgilerini de sunar.

### 🐍 Python Dilinde Kullanılan Özellikler

Bu proje, Python eğitiminde öğrenilen tüm temel ve gelişmiş özellikleri kapsamlı bir şekilde kullanmaktadır:

#### **Object-Oriented Programming (OOP)**
- **Sınıflar (Classes)**: `Todo`, `WeatherData`, `TodoManager`, `Config`
- **Nesneler (Objects)**: Todo instance'ları oluşturma ve yönetme
- **Methodlar**: `toggle_complete()`, `update_text()`, `add_todo()`, `delete_todo()`
- **Encapsulation**: Private/public methodlar ve veri gizleme
- **Inheritance**: Config sınıfları için kalıtım kullanımı
- **Polymorphism**: Farklı sınıflarda aynı method isimlerinin farklı davranışları

#### **Functions (Fonksiyonlar)**
- **Decorator'lar**: `@handle_errors`, `@require_method`, `@validate_input`, `@wraps`
- **Lambda Fonksiyonları**: Sıralama ve filtreleme işlemlerinde
- **List Comprehension**: Veri filtreleme ve dönüştürme
- **Higher-Order Functions**: `sorted()`, `filter()`, `map()`
- **Nested Functions**: Decorator'lar içinde iç fonksiyonlar
- **Closure**: Decorator'larda closure kullanımı

#### **Python Gelişmiş Özellikler**
- **Exception Handling**: `try/except/finally` blokları
- **Context Managers**: `@app.context_processor`
- **Error Handlers**: `@app.errorhandler(404)`, `@app.errorhandler(500)`
- **Type Hints**: Python 3.7+ tip belirtimleri (`str`, `int`, `List`, `Dict`, `Optional`)
- **Docstrings**: Tüm fonksiyon ve sınıflarda detaylı açıklamalar
- **Module System**: Ayrı dosyalarda organize edilmiş modüler yapı

#### **Python Best Practices**
- **Clean Code**: Okunabilir ve sürdürülebilir kod yapısı
- **DRY Principle**: Don't Repeat Yourself prensibi
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution
- **PEP 8**: Python kodlama standartlarına uygunluk
- **Configuration Management**: Environment variables ve config sınıfları
- **REST API Design**: RESTful endpoint'ler ve JSON responses

#### **Python Veri Yapıları**
- **Lists**: Todo listesi yönetimi
- **Dictionaries**: JSON responses ve veri yapıları
- **Tuples**: Sıralama anahtarları
- **Sets**: Benzersiz değer yönetimi
- **Generators**: Bellek verimli veri işleme

#### **Python Kütüphaneleri**
- **Flask**: Web framework
- **Requests**: HTTP istekleri
- **Datetime**: Tarih ve saat işlemleri
- **Typing**: Tip belirtimleri
- **Functools**: Decorator yardımcıları
- **JSON**: Veri serileştirme

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
├── app.py                 # Ana Flask uygulaması (OOP, Decorators, REST API)
├── main.py               # Uygulama giriş noktası
├── config.py             # Konfigürasyon yönetimi (OOP)
├── models.py              # Veri modelleri (OOP Classes)
├── utils.py               # Yardımcı fonksiyonlar (Functions)
├── __init__.py            # Paket başlatma dosyası
├── setup.py               # Python paket yapılandırması
├── requirements.txt       # Python bağımlılıkları
├── vercel.json           # Vercel deployment yapılandırması
├── Procfile              # Heroku deployment
├── .gitignore            # Git ignore dosyası
├── README.md             # Proje dokümantasyonu
├── templates/            # HTML şablonları
│   ├── base.html         # Temel şablon
│   ├── index.html        # Ana sayfa
│   └── weather.html      # Hava durumu sayfası
└── static/               # Statik dosyalar
    └── style.css         # Özel CSS stilleri
```

### 🐍 Python Dosya Açıklamaları

- **`app.py`**: Ana Flask uygulaması - Decorator'lar, OOP, REST API endpoints
- **`models.py`**: Veri modelleri - Todo, WeatherData, TodoManager sınıfları
- **`utils.py`**: Yardımcı fonksiyonlar - Pure functions, type hints
- **`config.py`**: Konfigürasyon yönetimi - OOP inheritance kullanımı
- **`main.py`**: Uygulama giriş noktası - Production deployment
- **`setup.py`**: Python paket yapılandırması - Professional packaging

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

**Kyetim** - Python Eğitimi Bitirme Projesi

### 🎓 Eğitim Bilgileri
- **Kurs**: Python Programlama Eğitimi
- **Proje Türü**: Bitirme Projesi
- **Teknoloji**: Python Flask Web Framework
- **Seviye**: İleri Seviye Python Özellikleri

### 🐍 Python Eğitiminde Öğrenilen Konular
Bu proje, Python eğitiminde öğrenilen tüm konuları pratik olarak uygulamaktadır:

1. **Temel Python**: Değişkenler, veri tipleri, operatörler
2. **Fonksiyonlar**: Function definition, parameters, return values
3. **OOP**: Classes, objects, inheritance, polymorphism
4. **Decorators**: Function decorators, class decorators
5. **Exception Handling**: Try/except, custom exceptions
6. **Modules & Packages**: Import system, package structure
7. **Advanced Features**: Lambda, list comprehension, generators
8. **Web Development**: Flask framework, REST API design
9. **Best Practices**: Clean code, PEP 8, documentation

## 📞 İletişim

- **GitHub**: [@kyetim](https://github.com/kyetim)
- **Proje Linki**: [https://github.com/kyetim/todo-weather-app2](https://github.com/kyetim/todo-weather-app2)
- **Canlı Demo**: Vercel deployment linki

## 🏆 Proje Başarıları

- ✅ **Python OOP** tam olarak uygulandı
- ✅ **Functions & Decorators** profesyonel seviyede kullanıldı
- ✅ **Exception Handling** kapsamlı şekilde uygulandı
- ✅ **REST API** endpoints geliştirildi
- ✅ **Modüler yapı** ve **clean code** prensipleri uygulandı
- ✅ **Production deployment** başarıyla tamamlandı

---

⭐ Bu Python eğitimi bitirme projesini beğendiyseniz yıldız vermeyi unutmayın!
