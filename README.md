# Document Scanner

Bu proje, OpenCV ve Python kullanarak belgeleri tarayan bir uygulamayı içerir. Uygulama, belgedeki konturları tespit eder, en büyük konturu seçer ve belgeyi düzleştirir. Son olarak, adaptif eşikleme uygulayarak taranan belgeyi işleyip kaydeder.

## Özellikler

- Web kamerası veya yüklenmiş bir resim ile çalışma
- Gri tonlama, Gaussian Blur ve Canny kenar algılama
- En büyük konturu bulma ve perspektif düzeltme (warp perspective)
- Adaptif eşikleme ve medyan bulanıklık uygulama
- Tarama sonuçlarını kaydetme ve görselleştirme

## Gereksinimler

- Python 3.x
- OpenCV
- NumPy

## Kurulum

Öncelikle gerekli kütüphaneleri yükleyin:

```bash
pip install opencv-python-headless numpy
```

## Kullanım
- webCamFeed değişkenini True yaparak web kamerası kullanabilirsiniz, ya da False yaparak bir resim dosyasını işleyebilirsiniz.

- pathImage değişkenine, işlemek istediğiniz resmin yolunu girin.

- Programı çalıştırın:

```bash
python document_scanner.py
```
- Görüntüleme penceresinde, 's' tuşuna basarak taranan belgeyi kaydedebilirsiniz.

## Kod Açıklamaları
- utlis.initializeTrackbars(): Eşik değerlerini kontrol etmek için izleyicileri başlatır.
- utlis.biggestContour(): En büyük konturu bulur.
- utlis.reorder(): Kontur köşelerini doğru sırayla düzenler.
- utlis.drawRectangle(): Konturu ve sınırlarını çizer.
- utlis.stackImages(): Birden fazla görüntüyü birleştirir ve etiketler.
