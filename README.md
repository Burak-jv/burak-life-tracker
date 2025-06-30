# burak-life-tracker
-Python ile Geliştirilmiş Günlük Rutinleri Değerlendiren Ve Aklında Tutan Akıllı Günlük
-Bu uygulama, günlük olarak kişisel gelişim verilerini kaydetmek ve aylık performans raporu oluşturmak için geliştirilmiştir. Veriler kullanıcı arayüzü üzerinden girilir, yerel JSON dosyalarına kaydedilir ve ay sonunda PDF formatında raporlanır.

Özellikler;
Takvim Entegrasyonu;
-Günlük veri girişi yapılan günler ✓, yapılmamış geçmiş günler ?, gelecek günler X olarak takvimde gösterilir.

Günlük Giriş Alanları;
-Ruh hali, kitap okuma, uyku, su, adım, antrenman, kodlama süresi, müzik, proje, vitamin, yalnızlık vb. alanlara dair 14 adet soru içerir.

Aylık PDF Raporu Oluşturma;
-Toplam sayfa, kod süresi, adım, moral ortalaması gibi veriler hesaplanır.
Bir motivasyon cümlesi ve grafikle birlikte PDF oluşturulur.

Veri Kaydı;
-Veriler data/ klasöründe aylık JSON dosyalarına kaydedilir. Raporlar reports/ klasörüne kaydedilir.

Kullanılan Teknolojiler
-Python 3.10
-Tkinter (GUI)
-Matplotlib (grafik)
-FPDF (PDF oluşturma)

Not;
PDF raporunun doğru çalışması için DejaVuSans.ttf font dosyası, LifeTracker.py ile aynı klasörde bulunmalıdır.


