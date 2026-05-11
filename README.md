# Campus Exchange (Üniversite İçi İkinci El / Takas Platformu)

Merhaba! Bu proje, üniversite öğrencileri arasında kitap, elektronik veya ev eşyası gibi ürünlerin alım-satımını ve takasını kolaylaştırmak için yapılmış bir web sitesidir. 

**Eğer kodlamadan hiç anlamıyorsan endişelenme!** Aşağıdaki adımları sırasıyla okuyarak bu siteyi kendi bilgisayarında çok rahat bir şekilde çalıştırabilirsin.

---

## 🛠️ Kurulum Adımları (Adım Adım Rehber)

Siteyi kendi bilgisayarında çalıştırmak için önce bazı programların bilgisayarında yüklü olması gerekiyor.

### Adım 1: Python'ı Yükle
Eğer bilgisayarında Python yüklü değilse, sitenin altyapısı çalışmaz.
1. [Python İndirme Sayfası](https://www.python.org/downloads/)'na gir ve en güncel sürümü indir.
2. İndirdiğin kurulum dosyasını çalıştır.
3. **ÇOK ÖNEMLİ:** Kurulum ekranının en altındaki **"Add python.exe to PATH"** yazan kutucuğu mutlaka işaretle! Sonra "Install Now" diyerek kur.

### Adım 2: Projeyi Bilgisayarına İndir
1. Bu sayfanın sağ üst köşesindeki yeşil renkli **"<> Code"** butonuna tıkla.
2. Açılan menüden **"Download ZIP"** seçeneğini seç.
3. İnen ZIP dosyasını klasöre çıkart (Masaüstüne çıkarabilirsin).

### Adım 3: Siyah Ekranı (Terminal) Açma
1. Projeyi çıkardığın klasörün içine gir. (İçinde `manage.py`, `README.md` gibi dosyalar olmalı).
2. Klasör açıkken, yukarıdaki dosya yolu çubuğuna (örneğin "C:\Users\Masaüstü\campus-exchange" yazan yere) bir kere tıkla.
3. O yazıyı silip yerine **`cmd`** yaz ve Enter'a bas. Karşına siyah bir komut ekranı açılacak.

### Adım 4: Gerekli Paketleri Yükleme
Açılan siyah ekrana sırasıyla şu komutları kopyala yapıştır ve her birinden sonra Enter'a basıp işlemin bitmesini bekle:

1. Sanal ortam (bir nevi özel bir kutu) oluşturuyoruz:
   ```bash
   python -m venv venv
   ```
2. O oluşturduğumuz kutunun içine giriyoruz:
   *(Windows için)*
   ```bash
   .\venv\Scripts\activate
   ```
   *(Eğer Mac kullanıyorsan şunu yaz: `source venv/bin/activate`)*
   *(Bunu yazınca satırın başında `(venv)` yazısı çıkmalı)*

3. Gerekli kütüphaneleri internetten indiriyoruz:
   ```bash
   pip install -r requirements.txt
   ```

4. Veritabanını (bilgilerin tutulduğu tabloyu) hazırlıyoruz:
   ```bash
   python manage.py migrate
   ```

### Adım 5: Siteyi Çalıştırma! 🚀
Her şey hazır! Şimdi tek yapman gereken siteyi yayına almak.
Aynı siyah ekrana son olarak şu komutu yaz:
```bash
python manage.py runserver
```

Ekranda yazılar akacak ve alt kısımlarda `Starting development server at http://127.0.0.1:8000/` gibi bir yazı göreceksin.

Artık Google Chrome veya Safari'yi açıp adres çubuğuna şunu yazabilirsin:
👉 **http://127.0.0.1:8000/**

Tebrikler! Siten karşında. Gönlünce üye olup ilan açabilirsin. Siyah ekranı kapattığında site de kapanır. Tekrar girmek istersen sadece `Adım 3` ve `Adım 5`i yapman yeterli.
