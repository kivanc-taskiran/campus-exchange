@echo off
echo ========================================
echo    Campus Exchange - Kurulum Baslıyor
echo ========================================
echo.

echo [1/5] Gerekli kutuphaneler yukleniyor...
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo [2/5] Veritabani olusturuluyor...
python manage.py migrate

echo.
echo [3/5] Ornek ilanlar yukleniyor...
python seed_data.py

echo.
echo [4/5] Admin hesabi olusturuluyor...
python -c "import os,django; os.environ['DJANGO_SETTINGS_MODULE']='campus_exchange.settings'; django.setup(); from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@campus.com','admin123'); print('Admin: admin / admin123')"

echo.
echo [5/5] Sunucu baslatiliyor...
echo.
echo ========================================
echo  Site aciliyor: http://127.0.0.1:8000
echo  Admin paneli:  http://127.0.0.1:8000/admin
echo  Admin sifre:   admin / admin123
echo  Demo kullanici: ahmet_k / 1234
echo ========================================
echo.
python manage.py runserver
pause
