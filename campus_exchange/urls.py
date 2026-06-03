"""
Campus Exchange — Ana URL Yapılandırması

Bu dosya projenin en üst seviye URL yönlendirme noktasıdır.
Gelen tüm URL istekleri burada ilgili uygulamalara dağıtılır.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django'nun yerleşik admin paneli
    # URL: /admin/  →  veritabanı kayıtlarını görsel olarak yönetmek için
    path('admin/', admin.site.urls),

    # Marketplace uygulamasının URL'leri
    # URL: /  →  marketplace/urls.py dosyasına yönlendir
    # Tüm ilan ve yorum URL'leri orada tanımlıdır
    path('', include('marketplace.urls')),

    # Django'nun yerleşik kimlik doğrulama URL'leri
    # URL: /accounts/login/   →  Giriş sayfası
    # URL: /accounts/logout/  →  Çıkış işlemi
    # URL: /accounts/password_change/ vb. gibi hazır sayfalar
    path('accounts/', include('django.contrib.auth.urls')),
]

# ─────────────────────────────────────────────
# GELİŞTİRME ORTAMINDA MEDYA DOSYASI SUNUMU
# DEBUG=True iken kullanıcıların yüklediği görselleri Django kendi sunar
# Canlı sunucuda bu iş Nginx/Apache gibi web sunucularına bırakılır
# ─────────────────────────────────────────────
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
