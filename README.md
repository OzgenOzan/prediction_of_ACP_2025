# prediction_of_ACP_2025

Tez çalışmasının **2025 sürümü** — antikanser peptit (ACP) tahmin hattı, Google Colab'da uçtan uca çalışır. Bu repo kendi kendine yeter: tüm veri ve model dosyaları içindedir, orijinal repoya ([OzgenOzan/prediction_of_ACP](https://github.com/OzgenOzan/prediction_of_ACP), ilk commit `56ab158`) veya yerel dosyalara erişim gerekmez.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/OzgenOzan/prediction_of_ACP_2025/blob/main/ACP_2025_Colab.ipynb)

## Baştan sona çalıştırma

### 1. Notebook'u Colab'da aç

Yukarıdaki **Open in Colab** rozetine tıklayın (veya Colab'da *Dosya → Not defteri aç → GitHub* sekmesinden `OzgenOzan/prediction_of_ACP_2025` reposunu seçin).

### 2. Tek seferlik: veri ve model dosyalarını repoya aktarın (bir kez, ~2 dakika)

Bazı dosyalar (ör. eğitilmiş model `RF_acc_dpc_bestModel.joblib` ve ~300 KB'lık `prediction_set.csv`) büyük/ikili olduğu için repoya küçük bir GitHub Actions iş akışıyla kopyalanır. **Bunu yalnızca bir kez yapmanız gerekir:**

1. Bu repo sayfasında **Add file → Create new file** deyin.
2. Dosya adı olarak tam olarak şunu yazın: `.github/workflows/import_2025_files.yml`
3. Aşağıdaki içeriği **olduğu gibi** yapıştırın ve **Commit changes** deyin:

```yaml
name: Import 2025 files
on:
  push:
    branches: [main]
    paths: [.github/workflows/import_2025_files.yml]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  import-2025-files:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout this repo
        uses: actions/checkout@v4
      - name: Clone original repo and switch to the 2025 (initial) commit
        run: |
          git clone -q https://github.com/OzgenOzan/prediction_of_ACP.git /tmp/orig
          cd /tmp/orig
          git checkout -q 56ab158b9eb4a6d0a697b7b3dd2d25da31617265
          git log --oneline -1
      - name: Copy the full 2025 snapshot into this repo (keep our README)
        run: |
          rsync -a --exclude='.git' --exclude='README.md' /tmp/orig/ "$GITHUB_WORKSPACE/"
          ls -la
      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "Import full 2025 snapshot from OzgenOzan/prediction_of_ACP@56ab158" || echo "No changes to commit"
          git push
```

4. **Actions** sekmesine gidin: "Import 2025 files" işi commit'le otomatik başlar; yeşil ✔ görünene kadar bekleyin (~1 dakika). Başlamadıysa soldan iş akışını seçip **Run workflow** deyin.

Bu kadar — orijinal reponun 2025 sürümündeki **tüm dosyalar** (veri kümeleri, eğitilmiş model, PepFun modülü, tez script'leri) artık bu repoda.

### 3. Notebook'u çalıştırın

Colab'da **Çalışma Zamanı → Tümünü çalıştır** (Runtime → Run all). Süre ~5-10 dakika. Notebook 0. hücrede gerekli dosyaların repoda olduğunu denetler; 2. adım atlandıysa sizi yönlendiren açık bir hata verir.

### 4. Çıktıları alın

Son hücre `predictions.csv` dosyasını otomatik indirir. Diğer çıktılar (`filtered_predictions.csv`, `filtered_predictions.fasta`, `model_scores.xlsx`, `peptide_properties.csv` vb.) sol paneldeki dosya gezginindedir.

## Repo içeriği (2. adımdan sonra)

| Yol | İçerik |
|---|---|
| `ACP_2025_Colab.ipynb` | Colab'da çalıştırılan tek dosya — tüm hattı uçtan uca çalıştırır |
| `_dataset_raw & UCLUST/working/` | Kümelenmiş + dengelenmiş 2025 verisi: `merged-main-working.csv` (eğitim), `merged-ind-working.csv` (bağımsız doğrulama), `prediction_set.csv` (~10k antimikrobiyel peptit) |
| `5. work model/RF_acc_dpc_bestModel.joblib` | Tezde eğitilmiş orijinal Random Forest modeli |
| `8. solubility/pepfun.py` | Çözünürlük özellikleri için PepFun modülü |
| `1.`–`8.` klasörleri | Tezdeki orijinal notebook'lar (referans amaçlı; Colab için gerekmez) |

## Notebook ne yapıyor?

Tezdeki akışı bölüm bölüm izler: sayısal kodlama → AAC/DPC özellikleri → RF/LR/SVM/KNN karşılaştırması → GridSearchCV hiperparametre optimizasyonu → final RF modeli (10-katlı CV) → bağımsız set doğrulaması → ~10.000 peptitte tahmin → (isteğe bağlı) PepFun çözünürlük.

**`AKIS` anahtarı** (0. hücre): `"2025"` tezdeki orijinal akışı (tahmin verisine yeni scaler fit edilir), `"2026"` ise düzeltilmiş akışı (eğitim scaler'ı kullanılır) çalıştırır.

## Bilinen notlar

- **Adım 0 (UCLUST kümeleme)** Windows'a özel `usearch.exe` gerektirdiğinden Colab'da atlanır; kümeleme çıktıları repoda hazırdır.
- **8. bölüm (PepFun)**, eski Biopython `pairwise2` modülüne bağımlıdır. Hata verirse notebook'taki yönergeyi izleyin (`pip install "biopython<1.84"` + çalışma zamanını yeniden başlatma) ya da `CALISTIR_PEPFUN = False` ile atlayın.
- Metriklerde scikit-learn sürüm farkından kaynaklanan küçük sapmalar normaldir (referans: eğitim testi Accuracy ≈ 0.894 / ROC AUC ≈ 0.928, bağımsız set Accuracy ≈ 0.7875 / ROC AUC ≈ 0.872).
