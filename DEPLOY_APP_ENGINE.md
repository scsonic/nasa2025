# Google App Engine 部署指南

## ✅ 已完成的設定

- **GCP Project ID**: `team-bubu`
- **GCS Bucket**: `gs://team-bubu` (已設為公開存取)
- **App Engine URL**: `https://team-bubu.appspot.com`

## 📋 部署前檢查清單

### 1. 確認 GCP 設定

```bash
# 確認登入的帳號
gcloud auth list

# 確認當前專案
gcloud config get-value project

# 如果不是 team-bubu，設定專案
gcloud config set project team-bubu
```

### 2. 確認 Bucket 權限

```bash
# 檢查 bucket 是否可公開存取
gsutil iam get gs://team-bubu | grep allUsers

# 應該看到：
# "members": [
#   "allUsers"
# ],
# "role": "roles/storage.objectViewer"
```

### 3. 設定 API Key

App Engine 需要 `GOOGLE_API_KEY` 環境變數。有兩種方式：

#### 方式 A: 使用 Secret Manager（推薦）

```bash
# 1. 啟用 Secret Manager API
gcloud services enable secretmanager.googleapis.com

# 2. 建立 secret
echo -n "你的_GEMINI_API_KEY" | gcloud secrets create GOOGLE_API_KEY --data-file=-

# 3. 給予 App Engine 存取權限
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member=serviceAccount:team-bubu@appspot.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# 4. 更新 app.yaml
```

在 `app.yaml` 中加入：
```yaml
env_variables:
  USE_GCS: "true"
  GCS_BUCKET_NAME: "team-bubu"
  BASE_URL: "https://team-bubu.appspot.com"
  GOOGLE_API_KEY: ${GOOGLE_API_KEY}
```

#### 方式 B: 直接在 app.yaml 設定（不推薦）

```yaml
env_variables:
  GOOGLE_API_KEY: "你的_API_KEY"
  USE_GCS: "true"
  GCS_BUCKET_NAME: "team-bubu"
  BASE_URL: "https://team-bubu.appspot.com"
```

⚠️ **注意**: 不要將含有 API Key 的 app.yaml 提交到 git！

## 🚀 部署步驟

### 1. 初始化 App Engine（首次部署）

```bash
# 檢查 App Engine 是否已啟用
gcloud app describe

# 如果未啟用，建立 App Engine 應用程式
gcloud app create --region=asia-east1
```

### 2. 部署應用程式

```bash
# 在專案根目錄執行
cd /Users/yougangkuo/Documents/nasa2025

# 部署
gcloud app deploy

# 系統會詢問：
# Do you want to continue (Y/n)? 
# 輸入 Y
```

部署過程約需 5-10 分鐘。

### 3. 查看部署狀態

```bash
# 查看應用程式資訊
gcloud app describe

# 查看版本
gcloud app versions list

# 查看服務
gcloud app services list
```

### 4. 開啟應用程式

```bash
# 在瀏覽器開啟
gcloud app browse

# 或直接訪問
open https://team-bubu.appspot.com
```

## 📊 監控與日誌

### 查看即時日誌

```bash
# 即時日誌
gcloud app logs tail -s default

# 查看最近的日誌
gcloud app logs read --limit=50
```

### 在 GCP Console 查看

1. 前往 [App Engine Dashboard](https://console.cloud.google.com/appengine)
2. 選擇專案 `team-bubu`
3. 查看：
   - **版本**: 管理不同版本
   - **實例**: 查看運行中的實例
   - **日誌**: 詳細的應用程式日誌

## 🧪 測試部署

### 1. 測試首頁

```bash
curl https://team-bubu.appspot.com/
```

應該返回 HTML 內容。

### 2. 測試健康檢查

```bash
curl https://team-bubu.appspot.com/health
```

應該返回：
```json
{
  "status": "healthy",
  "api_key_set": true
}
```

### 3. 測試圖片生成

在瀏覽器開啟：
```
https://team-bubu.appspot.com
```

1. 選擇起始場景
2. 產生圖片
3. 檢查是否成功上傳到 GCS
4. 測試分享功能

### 4. 驗證 GCS 儲存

```bash
# 檢查 result 資料夾
gsutil ls gs://team-bubu/result/

# 檢查 json 資料夾
gsutil ls gs://team-bubu/json/

# 查看某個 session
gsutil cat gs://team-bubu/json/sess_xxx.json
```

## 🔧 更新應用程式

修改程式碼後重新部署：

```bash
# 部署新版本
gcloud app deploy

# 查看所有版本
gcloud app versions list

# 刪除舊版本（節省成本）
gcloud app versions delete VERSION_ID
```

## 💰 成本管理

### 預估成本

- **F2 Instance**: ~$0.10/hour
- **最小實例數**: 0（無流量時不收費）
- **GCS 儲存**: ~$0.02/GB/month
- **網路傳輸**: 前 1GB 免費

### 節省成本的設定

在 `app.yaml` 中已設定：
```yaml
automatic_scaling:
  min_instances: 0  # 無流量時關閉實例
  max_instances: 10
```

### 監控成本

1. 前往 [Billing Dashboard](https://console.cloud.google.com/billing)
2. 查看 `team-bubu` 專案的費用
3. 設定預算警報

## ⚠️ 常見問題

### 1. 部署失敗：Permission denied

**解決方法**:
```bash
# 確認有 App Engine Admin 權限
gcloud projects get-iam-policy team-bubu

# 如果沒有，請專案擁有者加入權限
```

### 2. 503 Service Unavailable

**可能原因**:
- 應用程式啟動失敗
- API Key 未設定

**解決方法**:
```bash
# 查看日誌
gcloud app logs tail -s default

# 檢查環境變數
gcloud app describe
```

### 3. 圖片無法顯示

**可能原因**:
- Bucket 權限設定錯誤
- CORS 設定問題

**解決方法**:
```bash
# 重新設定 bucket 權限
gsutil iam ch allUsers:objectViewer gs://team-bubu

# 設定 CORS
echo '[{"origin": ["*"], "method": ["GET", "HEAD", "PUT", "POST", "DELETE"], "responseHeader": ["Content-Type"], "maxAgeSeconds": 3600}]' > cors.json
gsutil cors set cors.json gs://team-bubu
```

### 4. Session 找不到

**可能原因**:
- JSON 未上傳到 GCS
- 權限問題

**解決方法**:
```bash
# 檢查 service account 權限
gcloud projects get-iam-policy team-bubu \
  --flatten="bindings[].members" \
  --filter="bindings.members:team-bubu@appspot.gserviceaccount.com"
```

## 🔒 安全性建議

### 1. 使用 Secret Manager

不要在 `app.yaml` 中直接寫入 API Key。

### 2. 設定 IAM 權限

```bash
# 只給予必要的權限
gcloud projects add-iam-policy-binding team-bubu \
  --member=serviceAccount:team-bubu@appspot.gserviceaccount.com \
  --role=roles/storage.objectAdmin
```

### 3. 啟用 HTTPS

在 `app.yaml` 中已設定：
```yaml
handlers:
- url: /.*
  secure: always  # 強制 HTTPS
```

## 📚 相關資源

- [App Engine 文件](https://cloud.google.com/appengine/docs)
- [Python 3 Runtime](https://cloud.google.com/appengine/docs/standard/python3)
- [app.yaml 參考](https://cloud.google.com/appengine/docs/standard/python3/config/appref)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)

## 🎯 部署檢查清單

- [ ] GCP 專案設定為 `team-bubu`
- [ ] Bucket `gs://team-bubu` 已設為公開存取
- [ ] GOOGLE_API_KEY 已設定（Secret Manager 或 app.yaml）
- [ ] App Engine 已啟用
- [ ] `app.yaml` 已更新正確的設定
- [ ] `requirements.txt` 包含所有依賴
- [ ] 執行 `gcloud app deploy`
- [ ] 測試 `https://team-bubu.appspot.com`
- [ ] 測試圖片生成功能
- [ ] 測試分享功能
- [ ] 檢查 GCS 儲存
- [ ] 查看日誌確認無錯誤

完成以上步驟後，你的應用程式就成功部署到 App Engine 了！🎉
