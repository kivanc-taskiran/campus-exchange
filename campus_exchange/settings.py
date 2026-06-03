"""
Campus Exchange — Django Proje Ayarları
Bu dosya projenin tüm yapılandırmasını içerir.
"""

from pathlib import Path

# Projenin kök dizinini belirle (bu dosyanın 2 üst klasörü = proje kökü)
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# GÜVENLİK AYARLARI
# ─────────────────────────────────────────────
# Gizli anahtar: Django'nun şifreleme ve oturum için kullandığı benzersiz anahtar
# UYARI: Gerçek canlı ortamda (production) bu anahtar değiştirilmeli ve gizli tutulmalı!
SECRET_KEY = 'django-insecure-2c-7ja@oi^!$_axf!!7(l*rj7-mhx@j54x-n-j-h)r&iu&5#cb'

# DEBUG=True → hata sayfaları detaylı gösterilir (geliştirme ortamında kullanılır)
# Canlı sunucuda mutlaka False yapılmalı!
DEBUG = True

# Hangi domain adlarından erişime izin verilir (DEBUG=True'da boş bırakılabilir)
ALLOWED_HOSTS = []


# ─────────────────────────────────────────────
# KURULU UYGULAMALAR
# Django'nun ve üçüncü parti kütüphanelerin modülleri burada tanımlanır
# ─────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',        # Admin paneli
    'django.contrib.auth',         # Kimlik doğrulama (giriş/çıkış/kayıt)
    'django.contrib.contenttypes', # İçerik tipleri sistemi
    'django.contrib.sessions',     # Oturum yönetimi
    'django.contrib.messages',     # Flash mesajlar (başarı/hata bildirimleri)
    'django.contrib.staticfiles',  # Statik dosya yönetimi (CSS, JS, resimler)

    # Üçüncü parti kütüphaneler
    'crispy_forms',         # Form görünümünü Bootstrap ile güzelleştirmek için
    'crispy_bootstrap5',    # Crispy forms'un Bootstrap 5 desteği

    # Bizim oluşturduğumuz uygulama
    'marketplace',
]

# ─────────────────────────────────────────────
# MIDDLEWARE (ARA KATMANLAR)
# Her HTTP isteği/cevabı bu katmanlardan sırayla geçer
# ─────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Güvenlik başlıkları
    'django.contrib.sessions.middleware.SessionMiddleware',     # Oturum yönetimi
    'django.middleware.common.CommonMiddleware',                # Genel URL düzenlemeleri
    'django.middleware.csrf.CsrfViewMiddleware',                # CSRF saldırı koruması
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Kullanıcı kimlik doğrulama
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash mesaj sistemi
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking koruması
]

# Ana URL dosyasının konumu
ROOT_URLCONF = 'campus_exchange.urls'

# ─────────────────────────────────────────────
# ŞABLON (TEMPLATE) AYARLARI
# HTML dosyalarının nerede aranacağını belirtir
# ─────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Proje kökündeki 'templates' klasörünü de tara
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # Her uygulamanın kendi templates/ klasörünü de tara
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',   # request nesnesini şablonlara aktar
                'django.contrib.auth.context_processors.auth',  # Kullanıcı bilgilerini şablonlara aktar
                'django.contrib.messages.context_processors.messages',  # Flash mesajları şablonlara aktar
            ],
        },
    },
]

# WSGI uygulaması (web sunucusu ile Django arasındaki köprü)
WSGI_APPLICATION = 'campus_exchange.wsgi.application'


# ─────────────────────────────────────────────
# VERİTABANI AYARLARI
# SQLite kullanıyoruz → tek bir dosya (db.sqlite3), kurulum gerektirmez
# Gerçek projede PostgreSQL veya MySQL tercih edilir
# ─────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Veritabanı dosyasının konumu
    }
}


# ─────────────────────────────────────────────
# ŞİFRE DOĞRULAMA
# Boş bırakıldığı için herhangi bir şifre kabul edilir (sunum/test için)
# Gerçek projede minimum uzunluk, büyük harf vb. kurallar eklenmeli
# ─────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = []


# ─────────────────────────────────────────────
# ULUSLARARASILAŞTIRMA AYARLARI
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'  # Dil kodu
TIME_ZONE = 'UTC'        # Saat dilimi
USE_I18N = True          # Çeviri desteği
USE_TZ = True            # Zaman dilimi duyarlı tarih/saat


# ─────────────────────────────────────────────
# STATİK DOSYA AYARLARI
# CSS, JavaScript ve resim dosyaları 'static/' klasöründe tutulur
# ─────────────────────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Statik dosyaların konumu


# ─────────────────────────────────────────────
# MEDYA DOSYASI AYARLARI
# Kullanıcıların yüklediği görseller (ilan resimleri) 'media/' klasörüne kaydedilir
# ─────────────────────────────────────────────
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Görsellerin fiziksel olarak saklandığı klasör


# ─────────────────────────────────────────────
# CRISPY FORMS AYARLARI
# Form görünümlerinde Bootstrap 5 stilini kullan
# ─────────────────────────────────────────────
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Veritabanı primary key için varsayılan alan tipi (BigAutoField = 64-bit integer)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────
# GİRİŞ/ÇIKIŞ YÖNLENDİRME AYARLARI
# ─────────────────────────────────────────────
# Başarılı girişten sonra ana sayfaya yönlendir
LOGIN_REDIRECT_URL = 'index'
# Çıkış yaptıktan sonra ana sayfaya yönlendir
LOGOUT_REDIRECT_URL = 'index'
