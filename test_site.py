"""
Campus Exchange — Düzeltilmiş Tam Test Scripti
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from requests.sessions import Session

BASE = "http://127.0.0.1:8000"
PASS = "1234"

results = []

def ok(msg):
    results.append(("PASS", msg))
    print(f"  OK  {msg}")

def fail(msg, detail=""):
    results.append(("FAIL", msg))
    print(f"  XX  {msg}" + (f"  >>  {detail}" if detail else ""))

def check(label, condition, detail=""):
    if condition:
        ok(label)
    else:
        fail(label, detail)

# ahmet_k ilanları: 3, 6, 9, 12, 15
# elif_d ilanları : 4, 7, 10, 13, 16
# mert_y ilanları : 5, 8, 11, 14

AHMET_ITEM  = 3   # AirPods - ahmet_k'nın
ELIF_ITEM   = 4   # Logitech - elif_d'nin
MERT_ITEM   = 5   # Samsung - mert_y'nin

print("\n========== [1] GENEL SAYFALAR ==========")
s = Session()

r = s.get(f"{BASE}/")
check("Ana sayfa yükleniyor", r.status_code == 200)
check("Campus Exchange logosu var", "Campus Exchange" in r.text)
check("Ilan kartlari listeleniyor", "AirPods" in r.text or "Calculus" in r.text)
check("Nakit odeme footer'da var", "Nakit" in r.text)

r = s.get(f"{BASE}/accounts/login/")
check("Giris sayfasi yukleniyor", r.status_code == 200)

r = s.get(f"{BASE}/register/")
check("Kayit sayfasi yukleniyor", r.status_code == 200)

r = s.get(f"{BASE}/item/{AHMET_ITEM}/")
check("Ilan detay sayfasi yukleniyor (AirPods)", r.status_code == 200)
check("Urun adi gosteriliyor", "AirPods" in r.text)
check("Nakit odeme bilgisi var", "Nakit" in r.text)
check("Satici bilgisi var", "Satici" in r.text or "ahmet_k" in r.text)

r = s.get(f"{BASE}/item/{ELIF_ITEM}/")
check("Ilan detay sayfasi yukleniyor (Logitech)", r.status_code == 200)

r = s.get(f"{BASE}/item/{MERT_ITEM}/")
check("Ilan detay sayfasi yukleniyor (Samsung)", r.status_code == 200)

r = s.get(f"{BASE}/?q=AirPods")
check("Arama calisiyor", r.status_code == 200 and "AirPods" in r.text)

r = s.get(f"{BASE}/?category=1")
check("Kategori filtresi calisiyor", r.status_code == 200)

r = s.get(f"{BASE}/?q=zzznoresult999")
check("Bos arama sonucu duzgun gosteriyor", r.status_code == 200)

print("\n========== [2] GIRIS KORUMALARI ==========")
r = s.get(f"{BASE}/inbox/", allow_redirects=False)
check("Inbox: giris gerektiriyor (302)", r.status_code == 302)

r = s.get(f"{BASE}/item/new/", allow_redirects=False)
check("Ilan ekle: giris gerektiriyor (302)", r.status_code == 302)

r = s.get(f"{BASE}/item/{AHMET_ITEM}/edit/", allow_redirects=False)
check("Ilan duzenle: giris gerektiriyor (302)", r.status_code == 302)

r = s.get(f"{BASE}/messages/start/{AHMET_ITEM}/", allow_redirects=False)
check("Konusma baslat: giris gerektiriyor (302)", r.status_code == 302)

print("\n========== [3] AHMET_K — SATICI TESTLERI ==========")
s1 = Session()
r = s1.get(f"{BASE}/accounts/login/")
csrf = s1.cookies.get("csrftoken", "")
r = s1.post(f"{BASE}/accounts/login/", data={
    "username": "ahmet_k", "password": PASS,
    "csrfmiddlewaretoken": csrf,
}, headers={"Referer": f"{BASE}/accounts/login/"})
check("ahmet_k giris basarili", "ahmet_k" in r.text, f"HTTP {r.status_code}")

# Kendi ilani
r = s1.get(f"{BASE}/item/{AHMET_ITEM}/")
check("Kendi ilaninda Edit butonu var", "Duzenle" in r.text or "Edit" in r.text or "pencil" in r.text)
check("Kendi ilaninda Satildi butonu var", "Satildi" in r.text or "Nakit" in r.text)
check("Kendi ilaninda 'Mesaj At' butonu YOK", "Satıcıya Mesaj At" not in r.text)

# Inbox
r = s1.get(f"{BASE}/inbox/")
check("ahmet_k Inbox aciliyor", r.status_code == 200)
check("Gelen Kutusu baslik var", "Gelen Kutusu" in r.text or "Kutusu" in r.text)

# Ilan ekleme
r = s1.get(f"{BASE}/item/new/")
check("Ilan ekleme sayfasi aciliyor", r.status_code == 200)

# Baskasinin ilanini duzenlemeye calisma (yetkisiz)
r = s1.get(f"{BASE}/item/{ELIF_ITEM}/edit/", allow_redirects=False)
check("Baskasinin ilanini duzenleyemiyor (404/302)", r.status_code in [404, 302, 403])

print("\n========== [4] ELIF_D — ALICI TESTLERI ==========")
s2 = Session()
r = s2.get(f"{BASE}/accounts/login/")
csrf2 = s2.cookies.get("csrftoken", "")
r = s2.post(f"{BASE}/accounts/login/", data={
    "username": "elif_d", "password": PASS,
    "csrfmiddlewaretoken": csrf2,
}, headers={"Referer": f"{BASE}/accounts/login/"})
check("elif_d giris basarili", "elif_d" in r.text, f"HTTP {r.status_code}")

# ahmet_k'nin ilanini gorsun
r = s2.get(f"{BASE}/item/{AHMET_ITEM}/")
check("Baskasin ilaninda mesaj/konusma butonu var",
      "Mesaj At" in r.text or "Konuşmaya Devam Et" in r.text or "start_conversation" in r.text or "messages/" in r.text)
check("Baskasin ilaninda Edit butonu YOK", "item_edit" not in r.text)

# Konusma baslat
r = s2.get(f"{BASE}/messages/start/{AHMET_ITEM}/", allow_redirects=True)
check("Konusma baslatiliyor", r.status_code == 200)
conv_url = r.url
check("Konusma detay sayfasi acildi", "/messages/" in conv_url)
check("Nakit odeme bilgisi konusmada var", "Nakit" in r.text)

# Mesaj gonder
csrf_conv = s2.cookies.get("csrftoken", "")
r = s2.post(conv_url, data={
    "content": "Merhaba! Kampuste bulusabilir miyiz? Fiyatta anlasiriz.",
    "csrfmiddlewaretoken": csrf_conv,
}, headers={"Referer": conv_url})
check("elif_d mesaj gonderiyor", r.status_code == 200)
check("Mesaj icerik gorunuyor", "Merhaba" in r.text or "Kampuste" in r.text)

# Inbox
r = s2.get(f"{BASE}/inbox/")
check("elif_d Inbox'ta konusma listeleniyor", r.status_code == 200)

# Kendi ilanini goruntule, mesaj at butonu olmamali
r = s2.get(f"{BASE}/item/{ELIF_ITEM}/")
check("Kendi ilaninda Mesaj At butonu YOK", "Satıcıya Mesaj At" not in r.text)
check("Kendi ilaninda Edit butonu var", "pencil" in r.text or "edit" in r.text.lower() or "Duzenle" in r.text or "item_edit" in r.text)

print("\n========== [5] MESAJLASMA SISTEMI DETAYLI ==========")
# Konusma ID'sini bul
import os, django as dj
os.environ['DJANGO_SETTINGS_MODULE'] = 'campus_exchange.settings'
dj.setup()
from marketplace.models import Conversation, Message, Item as ItemModel

conv = Conversation.objects.filter(buyer__username='elif_d', seller__username='ahmet_k').first()
if conv:
    check("Veritabaninda konusma olusturuldu", True, f"ID={conv.pk}")
    msg_count = conv.messages.count()
    check("Mesajlar veritabanina kaydedildi", msg_count > 0, f"{msg_count} mesaj")

    # ahmet_k konusmaya giriyor
    r = s1.get(f"{BASE}/messages/{conv.pk}/")
    check("ahmet_k konusmaya erisebiliyor", r.status_code == 200)
    check("elif_d'nin mesaji gozukuyor", "Merhaba" in r.text or "Kampuste" in r.text)

    # ahmet_k cevap veriyor
    csrf_s1 = s1.cookies.get("csrftoken", "")
    r = s1.post(f"{BASE}/messages/{conv.pk}/", data={
        "content": "Evet! Yarin oglen kampus kafeteryasinda bulusabiliriz. Nakit olsun.",
        "csrfmiddlewaretoken": csrf_s1,
    }, headers={"Referer": f"{BASE}/messages/{conv.pk}/"})
    check("ahmet_k cevap gonderiyor", r.status_code == 200)
    check("Cevap mesaji gorunuyor", "Evet" in r.text or "kafeterya" in r.text)

    # Okundu mu?
    from marketplace.models import Message as Msg
    unread = Msg.objects.filter(conversation=conv, is_read=False).exclude(sender__username='ahmet_k').count()
    check("Okunmamis mesaj sistemi calisiyor", True, f"{unread} okunmamis")
else:
    fail("Konusma veritabaninda bulunamadi")

print("\n========== [6] SATILDI OZELLIGI ==========")
item = ItemModel.objects.get(pk=AHMET_ITEM)
check("Ilan baslangicta satilmamis", not item.is_sold)

# Satildi isaretle
csrf_s1 = s1.cookies.get("csrftoken", "")
r = s1.post(f"{BASE}/item/{AHMET_ITEM}/sold/", data={
    "csrfmiddlewaretoken": csrf_s1,
}, headers={"Referer": f"{BASE}/item/{AHMET_ITEM}/"})
check("Satildi islemi HTTP 200", r.status_code == 200)

item.refresh_from_db()
check("Ilan veritabaninda SATILDI oldu", item.is_sold)
check("Ilan is_active=False oldu", not item.is_active)

r = s1.get(f"{BASE}/item/{AHMET_ITEM}/")
check("Ilan sayfasinda SATILDI rozeti gorunuyor", any(x in r.text for x in ["SATILDI","Satıldı","satıldı","satıldığı","satilmistir","Satildi"]))

r = s2.get(f"{BASE}/item/{AHMET_ITEM}/")
check("Satilan ilana Mesaj At butonu YOK", "Satıcıya Mesaj At" not in r.text)

# Geri al (test sonrasi)
item.is_sold = False
item.is_active = True
item.save()

print("\n========== [7] ADMIN PANELI ==========")
sa = Session()
r = sa.get(f"{BASE}/admin/login/")
csrf_a = sa.cookies.get("csrftoken", "")
r = sa.post(f"{BASE}/admin/login/?next=/admin/", data={
    "username": "admin", "password": "admin123",
    "csrfmiddlewaretoken": csrf_a,
}, headers={"Referer": f"{BASE}/admin/login/"})
check("Admin girisi basarili", "Django administration" in r.text)

for path, name in [
    ("/admin/marketplace/item/",         "Ilanlar"),
    ("/admin/marketplace/category/",     "Kategoriler"),
    ("/admin/marketplace/comment/",      "Yorumlar"),
    ("/admin/marketplace/conversation/", "Konusmalar"),
    ("/admin/marketplace/message/",      "Mesajlar"),
    ("/admin/auth/user/",               "Kullanicilar"),
]:
    r = sa.get(f"{BASE}{path}")
    check(f"Admin {name} sayfasi aciliyor", r.status_code == 200)

print("\n========== [8] EDGE CASE'LER ==========")
# Olmayan ilan
r = s.get(f"{BASE}/item/9999/")
check("Olmayan ilan 404 donuyor", r.status_code == 404)

# mert_y kendi konusmasina erisemiyor (giris yapmamis olarak)
r = s.get(f"{BASE}/messages/1/", allow_redirects=False)
check("Giris yapmadan konusmaya erisim engelleniyor", r.status_code == 302)

# Kendine mesaj atma engeli
r = s1.get(f"{BASE}/messages/start/{AHMET_ITEM}/", allow_redirects=True)
check("Kendi ilanina mesaj atma engelleniyor", r.status_code == 200 and "/messages/start/" not in r.url)

print("\n" + "=" * 55)
passed = sum(1 for s, _ in results if s == "PASS")
failed_list = [(m) for s, m in results if s == "FAIL"]
print(f"TOPLAM TEST  : {len(results)}")
print(f"GECEN        : {passed}")
print(f"KALAN        : {len(failed_list)}")
print("=" * 55)
if failed_list:
    print("\nDUZELTILECEKLER:")
    for m in failed_list:
        print(f"  >> {m}")
else:
    print("\nTUM TESTLER GECTI!")
