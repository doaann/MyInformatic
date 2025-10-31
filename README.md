# İnformatik — Wikipedia Bilgi Uygulaması 🧠

**Kısa Açıklama**

Bu proje, **Türkçe Wikipedia** üzerinden konu araması yaparak ilgili makaleyi getirip kullanıcıya gösteren, **Tkinter** arayüzüyle hazırlanmış bir masaüstü uygulamadır.  
Uygulama, arka planda **Selenium** kullanarak web’den veriyi çeker, arayüz donmadan sonuçları listeler ve kullanıcı dostu bir deneyim sunar.

---

## 🚀 Özellikler

- Türkçe Wikipedia’dan otomatik bilgi getirme dolayısıyla kaynak doğru olur.
- Çok satırlı, kaydırılabilir metin alanı  
- Arama işlemini arka planda (thread) yaparak donmayan GUI  
- “Enter” tuşu veya buton ile arama başlatma  
- İlk arama sonucu tıklama ve tam makale içeriğini getirme  
- Kullanıcıya bilgilendirici açılış mesajı  

---

## 🧩 Gereksinimler

- **Python 3.8+** (3.10 veya üzeri önerilir)  
- Aşağıdaki Python paketleri:

```bash
pip install selenium webdriver-manager
