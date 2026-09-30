# prediction_of_ACP_2025 — Google Colab Sürümü

Bu repo, [OzgenOzan/prediction_of_ACP](https://github.com/OzgenOzan/prediction_of_ACP) reposunun **2025 (tez) sürümünü** (ilk commit, `56ab158`) Google Colab'da uçtan uca çalıştırmak için hazırlanmıştır. Veri ve orijinal dosyalar çalışma zamanında orijinal repodan klonlanır; **hesaplama mantığına dokunulmamıştır** — yalnızca Windows'a özgü dosya yolları (`C:\Users\oozgen\...`) ve `file_path` / `file_name.csv` yer tutucuları Colab'a uyarlanmıştır.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OzgenOzan/prediction_of_ACP_2025/blob/main/ACP_2025_Colab.ipynb)

## Baştan sona çalıştırma (özet)

1. Yukarıdaki **Open in Colab** rozetine tıklayın.
   (Alternatif: [colab.research.google.com](https://colab.research.google.com) → **Dosya → Not defteri aç → GitHub** → `OzgenOzan/prediction_of_ACP_2025` → `ACP_2025_Colab.ipynb`)
2. Üst menüden **Çalışma Zamanı → Tümünü çalıştır** (Runtime → Run all).
3. ~5-10 dakika bekleyin. Notebook sırasıyla şunları yapar:

| Bölüm | İçerik |
|---|---|
| 0 | Orijinal repoyu ilk commit'e sabitleyerek klonlar (2025 verisi) |
| 1 | Sekans → sayısal kodlama (26 sembol) |
| 2 | AAC + DPC (+ one-hot) özellik hesaplama |
| 3 | RF / LR / SVM / KNN model karşılaştırması |
| 4 | GridSearchCV ile RF hiperparametre optimizasyonu |
| 5 | Final RF modeli + 10-katlı çapraz doğrulama |
| 6 | Bağımsız set ile doğrulama |
| 7 | ~10.000 antimikrobiyel peptitte tahmin |
| 8 | (İsteğe bağlı) PepFun çözünürlük özellikleri |

4. Çıktılar (`predictions.csv`, `filtered_predictions.csv`, `filtered_predictions.fasta`, `model_scores*.xlsx`, `model_predictions*.xlsx`, `peptide_properties.csv`) son bölümde indirilebilir veya Colab'ın sol panelindeki dosya gezgininden alınabilir.

## `AKIS` anahtarı

Notebook'un ilk hücresindeki `AKIS` değişkeni yalnızca 7. bölümdeki (tahmin) ölçekleme davranışını değiştirir:

- `"2025"` (varsayılan): tezdeki orijinal akış — tahmin verisine yeni bir `StandardScaler` fit edilir (`scaler.fit_transform`).
- `"2026"`: 2026 kod denetiminin düzelttiği akış — eğitimde fit edilmiş scaler kullanılır (`scaler.transform`).

## Bilinen notlar

- **Adım 0 (UCLUST kümeleme) atlanmıştır:** orijinal `usearch.exe` bir Windows binary'sidir ve Colab'da (Linux) çalışmaz. Kümeleme çıktıları (`merged-main-working.csv`, `merged-ind-working.csv`, `prediction_set.csv`) orijinal repoda hazır durumda olduğundan pipeline buna ihtiyaç duymaz.
- **Orijinal kayıtlı model:** 6. bölüm, orijinal repodaki `RF_acc_dpc_bestModel.joblib` dosyasını yüklemeyi dener; Colab'ın scikit-learn sürümüyle uyumsuzsa otomatik olarak 5. bölümde yeniden eğitilen modele geçer.
- **PepFun (8. bölüm):** eski `Bio.pairwise2` modülüne bağımlıdır; güncel Biopython sürümlerinde bu modül kaldırılmış olabilir. Hata durumunda yeni bir hücrede `pip install "biopython<1.84"` çalıştırıp çalışma zamanını yeniden başlatın.
- Orijinal repo README'sindeki uyarı geçerlidir: sonuçlar revizyon altındadır; 2026 denetim notları için orijinal repodaki açık PR'lara bakınız.

## İlişkili repo

- Orijinal: https://github.com/OzgenOzan/prediction_of_ACP
