# 儲存模式說明

## 🎯 USE_GCS Flag

這個 flag 控制圖片和 session 資料的儲存位置。

### 預設值

```env
USE_GCS=false  # 預設使用本地儲存
```

## 📁 兩種模式比較

### 模式 1: 本地儲存 (USE_GCS=false) ⭐ 預設

**設定**:
```env
USE_GCS=false
BASE_URL=http://localhost:8000
```

**儲存位置**:
```
nasa2025/
├── input/          # 使用者上傳的圖片
├── result/         # AI 生成的圖片
└── sessions/       # Session JSON 檔案
```

**圖片 URL 格式**:
```
http://localhost:8000/images/uuid.jpg
```

**優點**:
- ✅ 不需要 GCP 認證
- ✅ 完全免費
- ✅ 快速存取
- ✅ 適合本地開發和測試

**缺點**:
- ❌ 只能在本機存取
- ❌ 無法跨裝置分享
- ❌ 伺服器重啟後檔案仍在，但 URL 可能改變

**適用場景**:
- 本地開發
- 測試功能
- 不需要分享的情況

---

### 模式 2: GCS 儲存 (USE_GCS=true)

**設定**:
```env
USE_GCS=true
GCS_BUCKET_NAME=team-bubu
BASE_URL=http://localhost:8000
```

**儲存位置**:
```
gs://team-bubu/
├── input/          # 使用者上傳的圖片
├── result/         # AI 生成的圖片
└── json/           # Session JSON 檔案

本地備份:
nasa2025/
├── result/         # 圖片備份
└── sessions/       # Session JSON 備份
```

**圖片 URL 格式**:
```
https://storage.googleapis.com/team-bubu/result/uuid.jpg
```

**優點**:
- ✅ 可公開分享
- ✅ 永久儲存
- ✅ 跨裝置存取
- ✅ 適合生產環境

**缺點**:
- ❌ 需要 GCP 認證
- ❌ 有儲存成本（約 $0.02/GB/月）
- ❌ 需要網路連線

**適用場景**:
- 生產環境
- 需要分享功能
- App Engine 部署

## 🔄 切換模式

### 從本地切換到 GCS

1. 編輯 `.env`:
   ```env
   USE_GCS=true
   ```

2. 確認 GCP 認證:
   ```bash
   gcloud auth application-default login
   ```

3. 重啟服務:
   ```bash
   python app.py
   ```

應該看到:
```
✅ GCS enabled: using bucket team-bubu
```

### 從 GCS 切換到本地

1. 編輯 `.env`:
   ```env
   USE_GCS=false
   ```

2. 重啟服務:
   ```bash
   python app.py
   ```

應該看到:
```
📁 Using local storage
```

## 🧪 測試不同模式

### 測試本地模式

```bash
# 1. 設定環境
echo "USE_GCS=false" >> .env

# 2. 啟動服務
python app.py

# 3. 產生圖片
# 開啟 http://localhost:8000

# 4. 檢查檔案
ls result/
ls sessions/

# 5. 檢查 URL
# 應該是: http://localhost:8000/images/xxx.jpg
```

### 測試 GCS 模式

```bash
# 1. 設定環境
echo "USE_GCS=true" >> .env

# 2. 認證
gcloud auth application-default login

# 3. 啟動服務
python app.py

# 4. 產生圖片
# 開啟 http://localhost:8000

# 5. 檢查 GCS
gsutil ls gs://team-bubu/result/
gsutil ls gs://team-bubu/json/

# 6. 檢查 URL
# 應該是: https://storage.googleapis.com/team-bubu/result/xxx.jpg
```

## 📊 儲存行為詳細說明

### 圖片儲存

| 動作 | 本地模式 | GCS 模式 |
|------|---------|---------|
| 上傳圖片 | 存到 `input/` | 存到 `gs://team-bubu/input/` |
| 生成圖片 | 存到 `result/` | 存到 `gs://team-bubu/result/` + 本地備份 |
| 返回 URL | `http://localhost:8000/images/xxx.jpg` | `https://storage.googleapis.com/team-bubu/result/xxx.jpg` |

### Session JSON 儲存

| 動作 | 本地模式 | GCS 模式 |
|------|---------|---------|
| 建立 session | 存到 `sessions/` | 存到 `gs://team-bubu/json/` + 本地備份 |
| 更新 history | 更新 `sessions/{id}.json` | 更新 `gs://team-bubu/json/{id}.json` + 本地備份 |
| 讀取 session | 從 `sessions/` 讀取 | 優先從 GCS 讀取，失敗則從本地讀取 |

### 備份機制

**GCS 模式下的本地備份**:
- 所有圖片都會同時儲存到本地 `result/` 資料夾
- 所有 session JSON 都會同時儲存到本地 `sessions/` 資料夾
- 如果 GCS 上傳失敗，至少還有本地備份

## 🔍 除錯

### 檢查當前模式

啟動服務時會顯示:
```bash
# 本地模式
📁 Using local storage

# GCS 模式
✅ GCS enabled: using bucket team-bubu
```

### 檢查環境變數

```bash
# 查看 .env 檔案
cat .env | grep USE_GCS

# 在 Python 中檢查
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'USE_GCS={os.getenv(\"USE_GCS\")}')"
```

### 常見問題

**Q: 為什麼設定 USE_GCS=true 但還是用本地儲存？**

A: 可能原因:
1. GCP 認證失敗 → 執行 `gcloud auth application-default login`
2. Bucket 不存在 → 檢查 `GCS_BUCKET_NAME`
3. 沒有權限 → 檢查 IAM 權限

系統會自動 fallback 到本地儲存並顯示警告訊息。

**Q: 可以混合使用嗎？**

A: 不建議。選擇一種模式並保持一致。如果切換模式，舊的資料不會自動遷移。

**Q: 如何遷移資料？**

A: 從本地遷移到 GCS:
```bash
# 遷移圖片
gsutil -m cp -r result/* gs://team-bubu/result/

# 遷移 session
gsutil -m cp -r sessions/* gs://team-bubu/json/
```

從 GCS 下載到本地:
```bash
# 下載圖片
gsutil -m cp -r gs://team-bubu/result/* result/

# 下載 session
gsutil -m cp -r gs://team-bubu/json/* sessions/
```

## 🎯 建議設定

### 開發環境
```env
USE_GCS=false
BASE_URL=http://localhost:8000
```

### 測試 GCS 功能
```env
USE_GCS=true
GCS_BUCKET_NAME=team-bubu
BASE_URL=http://localhost:8000
```

### 生產環境 (App Engine)
在 `app.yaml` 中:
```yaml
env_variables:
  USE_GCS: "true"
  GCS_BUCKET_NAME: "team-bubu"
  BASE_URL: "https://team-bubu.appspot.com"
```

## 📝 總結

- **預設值**: `USE_GCS=false` (本地儲存)
- **本地開發**: 使用 `false`，快速且免費
- **生產部署**: 使用 `true`，可分享且永久儲存
- **自動備份**: GCS 模式下仍會保留本地備份
- **自動降級**: GCS 失敗時自動切換到本地儲存
