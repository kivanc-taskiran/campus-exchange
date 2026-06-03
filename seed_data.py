"""
Campus Exchange - Örnek Veri Yükleme Script'i
Çalıştır: python seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_exchange.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Category, Item

# ─── Demo kullanıcılar oluştur ───────────────────────────────────────────────
users_data = [
    {'username': 'ahmet_k',   'password': '1234', 'first_name': 'Ahmet',  'last_name': 'Kaya'},
    {'username': 'elif_d',    'password': '1234', 'first_name': 'Elif',   'last_name': 'Demir'},
    {'username': 'mert_y',    'password': '1234', 'first_name': 'Mert',   'last_name': 'Yıldız'},
]

created_users = []
for u in users_data:
    user, created = User.objects.get_or_create(username=u['username'])
    if created:
        user.set_password(u['password'])
        user.first_name = u['first_name']
        user.last_name  = u['last_name']
        user.save()
        print(f"  ✓ Kullanıcı oluşturuldu: {u['username']}")
    else:
        print(f"  – Kullanıcı zaten var:    {u['username']}")
    created_users.append(user)

ahmet, elif_, mert = created_users

# ─── Kategorileri al ─────────────────────────────────────────────────────────
elektronik = Category.objects.get(slug='elektronik')
kitap      = Category.objects.get(slug='kitap')
ev         = Category.objects.get(slug='ev-esyasi')
giyim      = Category.objects.get(slug='giyim')
diger      = Category.objects.get(slug='diger')

# ─── Örnek ilanlar ───────────────────────────────────────────────────────────
items_data = [
    # Elektronik
    {
        'title': 'Apple AirPods Pro (2. Nesil)',
        'description': 'Çok az kullanılmış, kutusu ve tüm aksesuarları mevcut. Gürültü engelleme özelliği çalışıyor. Batarya sağlığı %94. Kampüste teslim.',
        'price': 2500,
        'category': elektronik,
        'owner': ahmet,
    },
    {
        'title': 'Logitech MX Master 3 Mouse',
        'description': 'Ergonomik kablosuz mouse, 1 yıl kullandım. Çizik yok, mükemmel durumda. Faturası var. Öğrenci indirimli alındı.',
        'price': 850,
        'category': elektronik,
        'owner': elif_,
    },
    {
        'title': 'Samsung 27" 4K Monitör',
        'description': '4K IPS panel, 60Hz, USB-C bağlantısı var. Mezun olduğum için satıyorum. Orijinal kutusu var, hasar yok.',
        'price': 4200,
        'category': elektronik,
        'owner': mert,
    },
    {
        'title': 'Mechanical Klavye (Red Switch)',
        'description': 'RGB aydınlatmalı, compact 75% layout. Kablolu, USB-C çıkış. Çok temiz kullanıldı.',
        'price': 650,
        'category': elektronik,
        'owner': ahmet,
    },
    # Kitap
    {
        'title': 'Calculus - James Stewart (8. Baskı)',
        'description': 'Mühendislik fakültesi öğrencileri için standart Calculus kitabı. Birkaç sayfada kalem notu var, genel durumu iyi. Takas da olur.',
        'price': 200,
        'category': kitap,
        'owner': elif_,
    },
    {
        'title': 'Introduction to Algorithms (CLRS)',
        'description': 'Bilgisayar bilimleri için temel algoritma kitabı. Türkçe baskı, temiz durumda, hiç yazı yok.',
        'price': 350,
        'category': kitap,
        'owner': mert,
    },
    {
        'title': 'Yapay Zeka: Modern Bir Yaklaşım (Türkçe)',
        'description': 'Russell & Norvig, 4. baskı Türkçe çevirisi. Ders kitabı olarak kullandım, bazı bölümlerde altı çizili.',
        'price': 280,
        'category': kitap,
        'owner': ahmet,
    },
    {
        'title': 'Python ile Veri Bilimi (O\'Reilly)',
        'description': 'Yeni gibi, sadece ilk 3 bölümü okudum. Pandas, NumPy, Matplotlib konularını içeriyor.',
        'price': 0,  # Takas
        'category': kitap,
        'owner': elif_,
    },
    # Ev Eşyası
    {
        'title': 'Çift Kişilik Yatak Örtüsü Seti',
        'description': 'Yurt odasından taşındım, artık ihtiyacım yok. Temizlenmiş, iyi durumda. 2 yastık kılıfı dahil.',
        'price': 150,
        'category': ev,
        'owner': mert,
    },
    {
        'title': 'Elektrikli Çaydanlık - Arçelik',
        'description': 'Yurt odasında kullanıyordum, 1.5 litre. Çok temiz, sorunsuz çalışıyor.',
        'price': 120,
        'category': ev,
        'owner': ahmet,
    },
    # Giyim
    {
        'title': 'Nike Dri-FIT Spor Tişört (L Beden)',
        'description': 'Sadece 2 kez giyildi. Siyah renk, L beden. Spor için ideal.',
        'price': 180,
        'category': giyim,
        'owner': elif_,
    },
    {
        'title': 'Kışlık Mont (M Beden, Erkek)',
        'description': 'Geçen kış aldım, bu yıl büyük geldi. Koyu mavi, dolgu yok, su geçirmez.',
        'price': 400,
        'category': giyim,
        'owner': mert,
    },
    # Diğer
    {
        'title': 'Bisiklet Kilidi + Pompa Seti',
        'description': 'Kampüste bisiklet kullananlar için. Kablo kilit + mini pompa seti. Takas olur.',
        'price': 90,
        'category': diger,
        'owner': ahmet,
    },
    {
        'title': 'Ders Notları - Diferansiyel Denklemler',
        'description': 'El yazısı notlar, sınav öncesi çok işe yarıyor. Fotokopi alabilirsin ya da orijinali satıyorum.',
        'price': 50,
        'category': diger,
        'owner': elif_,
    },
]

print("\n📦 İlanlar oluşturuluyor...")
created_count = 0
for data in items_data:
    item, created = Item.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'price':       data['price'],
            'category':    data['category'],
            'owner':       data['owner'],
            'is_active':   True,
        }
    )
    if created:
        print(f"  ✓ {item.title}")
        created_count += 1
    else:
        print(f"  – Zaten var: {item.title}")

print(f"\n✅ Tamamlandı! {created_count} yeni ilan eklendi.")
print(f"📊 Toplam ilan sayısı: {Item.objects.count()}")
print("\n🔑 Demo hesaplar:")
print("   Kullanıcı adı: ahmet_k  | Şifre: 1234")
print("   Kullanıcı adı: elif_d   | Şifre: 1234")
print("   Kullanıcı adı: mert_y   | Şifre: 1234")
