# Session 管理與分享功能指南

## 🎯 功能概述

每個使用者開啟 `index.html` 時會自動獲得一個 session ID，所有產生的圖片都會記錄在這個 session 中，並可以透過分享連結查看完整的創作歷程。

## 📋 工作流程

### 1. Session 建立

當使用者開啟 `http://localhost:8000` 時：

```javascript
// 自動產生 session ID
sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
// 例如: sess_1728024000000_abc123xyz
```

### 2. 圖片生成與記錄

每次使用者點擊 Submit 按鈕：

1. **前端** (`index.html`)：
   ```javascript
   formData.append('session_id', sessionId);
   ```

2. **後端** (`app.py`)：
   - 檢查 `gs://team-bubu/json/{session_id}.json` 是否存在
   - 如果不存在，建立新的 JSON：
     ```json
     {
       "id": "sess_1728024000000_abc123xyz",
       "created_at": "2025-10-04T15:00:00",
       "history": []
     }
     ```
   - 圖片生成後，更新 history：
     ```json
     {
       "id": "sess_1728024000000_abc123xyz",
       "created_at": "2025-10-04T15:00:00",
       "updated_at": "2025-10-04T15:05:00",
       "history": [
         "https://storage.googleapis.com/team-bubu/result/uuid1.jpg",
         "https://storage.googleapis.com/team-bubu/result/uuid2.jpg"
       ]
     }
     ```

### 3. 分享功能

使用者點擊 Share 按鈕：

1. **複製連結**：
   ```
   http://localhost:8000/share/sess_1728024000000_abc123xyz
   ```

2. **自動開啟新分頁**：
   - 顯示 `share.html`
   - 載入該 session 的所有圖片
   - 提供 slideshow 播放功能

## 🗂️ 儲存位置

### GCS Bucket 結構

```
gs://team-bubu/
├── input/                    # 使用者上傳的原始圖片
├── result/                   # AI 生成的結果圖片
│   ├── uuid1.jpg
│   ├── uuid2.jpg
│   └── ...
└── json/                     # Session 資料
    ├── sess_xxx.json
    ├── sess_yyy.json
    └── ...
```

### 本地備份

即使使用 GCS，系統仍會在本地保存備份：

```
nasa2025/
├── result/                   # 圖片備份
│   ├── uuid1.jpg
│   └── uuid2.jpg
└── sessions/                 # Session JSON 備份
    ├── sess_xxx.json
    └── sess_yyy.json
```

## 🔍 API 端點

### 1. 圖片編輯（含 session 記錄）

```bash
POST /api/edit
Content-Type: multipart/form-data

file: [圖片檔案]
prompt: "將背景改成藍色"
session_id: "sess_1728024000000_abc123xyz"
```

**回應**：
```json
{
  "status": "success",
  "image_urls": [
    "https://storage.googleapis.com/team-bubu/result/uuid.jpg"
  ]
}
```

**副作用**：
- 圖片上傳到 `gs://team-bubu/result/`
- Session JSON 更新並上傳到 `gs://team-bubu/json/`

### 2. 取得 Session 資料

```bash
GET /api/session/{session_id}
```

**回應**：
```json
{
  "status": "success",
  "session": {
    "id": "sess_1728024000000_abc123xyz",
    "created_at": "2025-10-04T15:00:00",
    "updated_at": "2025-10-04T15:05:00",
    "history": [
      "https://storage.googleapis.com/team-bubu/result/uuid1.jpg",
      "https://storage.googleapis.com/team-bubu/result/uuid2.jpg"
    ]
  }
}
```

### 3. 分享頁面

```bash
GET /share/{session_id}
```

返回 `share.html` 頁面，該頁面會：
1. 從 URL 取得 session_id
2. 呼叫 `/api/session/{session_id}` 取得資料
3. 顯示所有圖片的 slideshow

## 🎨 Slideshow 功能

### 控制項

- **播放按鈕**（右下角）：
  - 點擊開始自動播放
  - 每張圖片顯示 500ms
  - Fade in/out 效果
  - 播放到最後自動停止

- **導航箭頭**（左右）：
  - 手動切換上一張/下一張

- **計數器**（左下角）：
  - 顯示當前圖片編號 / 總數

- **鍵盤快捷鍵**：
  - `←` / `→`：切換圖片
  - `Space`：播放/暫停

## 🧪 測試流程

### 1. 啟動服務

```bash
# 確保 .env 設定正確
USE_GCS=true
GCS_BUCKET_NAME=team-bubu

# 啟動
python app.py
```

應該看到：
```
✅ GCS enabled: using bucket team-bubu
```

### 2. 測試圖片生成

1. 開啟 http://localhost:8000
2. 選擇起始場景
3. 產生幾張圖片
4. 觀察終端輸出：
   ```
   ✅ Session sess_xxx saved to GCS
   💾 Session sess_xxx: 1 images
   💾 Session sess_xxx: 2 images
   ```

### 3. 驗證 GCS 儲存

```bash
# 檢查 JSON 檔案
gsutil cat gs://team-bubu/json/sess_xxx.json

# 檢查圖片
gsutil ls gs://team-bubu/result/
```

### 4. 測試分享功能

1. 點擊 Share 按鈕
2. 應該會：
   - 複製連結到剪貼簿
   - 開啟新分頁顯示 slideshow
3. 在 slideshow 頁面測試：
   - 播放按鈕
   - 左右箭頭
   - 鍵盤快捷鍵

### 5. 直接存取分享連結

```bash
# 複製 session ID
# 在新瀏覽器分頁開啟
http://localhost:8000/share/sess_xxx
```

應該能看到該 session 的所有圖片。

## 📊 監控與除錯

### 查看 Session 資料

```bash
# 本地
cat sessions/sess_xxx.json

# GCS
gsutil cat gs://team-bubu/json/sess_xxx.json
```

### 查看所有 Sessions

```bash
# 本地
ls sessions/

# GCS
gsutil ls gs://team-bubu/json/
```

### 刪除舊 Session

```bash
# 本地
rm sessions/sess_xxx.json

# GCS
gsutil rm gs://team-bubu/json/sess_xxx.json
```

## ⚠️ 注意事項

### 1. Session ID 格式

目前使用：`sess_{timestamp}_{random}`

優點：
- 唯一性高
- 包含時間資訊
- 易於除錯

缺點：
- 較長（約 30 字元）
- URL 不夠簡潔

### 2. 公開存取

- 所有 session JSON 都是公開的
- 任何人知道 session ID 就能查看
- 不適合存放敏感資料

### 3. 儲存成本

- JSON 檔案很小（< 1KB）
- 主要成本在圖片儲存
- 建議定期清理舊 session

### 4. 錯誤處理

如果 session 不存在：
- API 返回 404
- share.html 顯示錯誤訊息

## 🚀 未來改進

1. **短網址**：
   - 使用 8 字元隨機 ID
   - 更簡潔的分享連結

2. **過期機制**：
   - 自動刪除 30 天前的 session
   - GCS lifecycle policy

3. **私人 session**：
   - 加入密碼保護
   - 只有知道密碼的人才能查看

4. **社群分享**：
   - 一鍵分享到 Twitter/Facebook
   - Open Graph meta tags

5. **下載功能**：
   - 下載單張圖片
   - 下載整個 session 為 ZIP

## 📚 相關檔案

- `app.py` - 後端 API 和 session 管理
- `static/index.html` - 主介面（產生 session ID）
- `static/share.html` - 分享頁面（slideshow）
- `GCS_SETUP.md` - GCS 設定指南
