@echo off
echo ========================================
echo    Campus Exchange - Kurulum Baslıyor
echo ========================================
echo.

echo [1/5] Python sanal ortami olusturuluyor...
python -m venv venv

echo.
echo [2/5] Gerekli kutuphaneler yukleniyor...
venv\Scripts\pip install -r requirements.txt

echo.
echo [3/5] Veritabani olusturuluyor...
venv\Scripts\python manage.py migrate

echo.
echo [4/5] Ornek ilanlar yukleniyor...
venv\Scripts\python seed_data.py

echo.
echo [5/5] Admin hesabi kontrol ediliyor...
venv\Scripts\python -c "import os,django; os.environ['DJANGO_SETTINGS_MODULE']='campus_exchange.settings'; django.setup(); from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@campus.com','admin123'); print('Admin hazir.')"

echo.
echo ========================================
echo  KURULUM TAMAMLANDI!
echo.
echo  Tarayıcıdan su adresi ac:
echo  http://127.0.0.1:8000
echo.
echo  Admin paneli: http://127.0.0.1:8000/admin
echo  Admin giris:  admin / admin123
echo  Demo hesap:   ahmet_k / 1234
echo ========================================
echo.
echo Sunucu baslatılıyor... (Kapatmak icin CTRL+C)
echo.
venv\Scripts\python manage.py runserver
pause
