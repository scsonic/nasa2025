# GCS Storage 設定指南

## ✅ 已完成的設定

1. **GCP 登入**: `scsonic@gmail.com`
2. **專案**: `team-bubu`
3. **Bucket**: `gs://team-bubu` (已設為公開存取)
4. **測試**: https://storage.googleapis.com/team-bubu/json/moon.png ✅

## 📦 安裝步驟

### 1. 安裝 Python 套件

```bash
pip install -r requirements.txt
```

這會安裝 `google-cloud-storage>=2.10.0`

### 2. 設定環境變數

編輯 `.env` 檔案（如果沒有，複製 `.env.example`）：

```bash
cp .env.example .env
```

在 `.env` 中設定：

```env
# Gemini API Key
GOOGLE_API_KEY=你的_API_KEY

# 啟用 GCS
USE_GCS=true

# Bucket 名稱
GCS_BUCKET_NAME=team-bubu

# 服務 URL
BASE_URL=http://localhost:8000
```

### 3. GCP 認證

確保你已經登入正確的帳號：

```bash
gcloud auth login scsonic@gmail.com
gcloud config set project team-bubu
```

或使用 Application Default Credentials：

```bash
gcloud auth application-default login
```

### 4. 測試連線

啟動服務：

```bash
python app.py
```

你應該會看到：

```
✅ GCS enabled: using bucket team-bubu
```

## 🎯 功能說明

### 自動上傳到 GCS

當 `USE_GCS=true` 時，所有生成的圖片會：

1. **上傳到 GCS bucket**
   - 路徑：`gs://team-bubu/result/{uuid}.jpg`
   - 公開 URL：`https://storage.googleapis.com/team-bubu/result/{uuid}.jpg`

2. **同時備份到本地**
   - 路徑：`./result/{uuid}.jpg`
   - 用於本地預覽和備份

### Bucket 結構

```
gs://team-bubu/
├── input/          # 使用者上傳的圖片
├── result/         # AI 生成的結果圖片
└── json/           # Session 資料（未來使用）
```

### 返回的 URL

- **GCS 模式**: `https://storage.googleapis.com/team-bubu/result/abc123.jpg`
- **本地模式**: `http://localhost:8000/images/abc123.jpg`

## 🔍 驗證設定

### 測試 1: 檢查 bucket 權限

```bash
gsutil iam get gs://team-bubu
```

應該看到 `allUsers` 有 `roles/storage.objectViewer` 權限。

### 測試 2: 上傳測試檔案

```bash
echo "test" > test.txt
gsutil cp test.txt gs://team-bubu/result/test.txt
curl -I https://storage.googleapis.com/team-bubu/result/test.txt
```

應該返回 `HTTP/2 200`

### 測試 3: 透過 API 測試

```bash
# 啟動服務
python app.py

# 在另一個終端測試
curl -X POST -F "file=@test_image.jpg" -F "prompt=test" http://localhost:8000/api/edit
```

檢查返回的 `image_urls` 是否包含 GCS URL。

## ⚠️ 注意事項

### 權限

- Bucket 已設為**公開讀取**
- 所有上傳的檔案都可以透過公開 URL 存取
- 不要上傳敏感資料

### 成本

- **儲存**: ~$0.02/GB/month
- **網路傳輸**: 前 1GB 免費，之後約 $0.12/GB
- **操作**: Class A (寫入) $0.05/10,000 次

### 本地備份

即使使用 GCS，系統仍會在本地 `result/` 資料夾保存一份備份，方便：
- 本地開發和測試
- 快速預覽
- 災難恢復

## 🐛 故障排除

### 錯誤: GCS initialization failed

**原因**: 未登入或權限不足

**解決**:
```bash
gcloud auth application-default login
```

### 錯誤: 403 Forbidden

**原因**: Bucket 權限設定錯誤

**解決**:
```bash
gsutil iam ch allUsers:objectViewer gs://team-bubu
```

### 錯誤: Bucket not found

**原因**: Bucket 名稱錯誤或不存在

**解決**:
```bash
# 檢查 bucket 是否存在
gsutil ls gs://team-bubu

# 檢查 .env 中的 GCS_BUCKET_NAME
```

### 想切換回本地模式

在 `.env` 中設定：
```env
USE_GCS=false
```

重啟服務即可。

## 📚 相關文件

- [Google Cloud Storage 文件](https://cloud.google.com/storage/docs)
- [Python Client Library](https://cloud.google.com/python/docs/reference/storage/latest)
- [IAM 權限管理](https://cloud.google.com/storage/docs/access-control/iam)
