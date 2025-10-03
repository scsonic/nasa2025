# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

此專案是一個室內設計網站，使用 Nano Banana API（Google Gemini 2.5 Flash）進行圖像編輯的 FastAPI 服務。
整合圖像上傳、AI 處理和靜態檔案服務於單一應用程式中，專為 localhost 本地運行設計。

### 室內設計網站功能

**核心功能：**
- 使用者可以透過拖放方式放置家具（沙發等物件）
- 可以搭配文字說明來描述設計需求
- 每次進入網頁會產生一個 session ID 用於追蹤創作過程
- 使用者可以分享臨時 ID 來展示創作過程

**起始場景：**
- 提供四個起始圖供選擇：space.png, moon.png, mars.png, ship.png（800x600）
- 選擇的起始圖會成為 history 的第一張圖

**左側面板（對話區）：**
- Dr. Bubu 對話視窗，包含頭像（100x100）和對話文字框
- `dr_talk(text)` 函數：逐字顯示文字效果
- 文字輸入區（textarea）供使用者輸入需求
- Submit 按鈕：
  - 有修改時為彩色
  - 送出後變灰色
  - 觸發 Nano Banana API 呼叫

**右側主畫面：**
- Canvas 顯示當前圖片（history 最後一張）
- 上層 Canvas 用於家具拖放操作
- 家具清單：可捲動的家具圖片列表（item1.png ~ item20.png）
- 家具放置記錄 array：記錄每個家具的坐標位置

**圖片生成流程：**
1. 使用者按下 submit
2. 生成一個 canvas，包含：
   - History 最後一張圖作為背景
   - 每個家具位置用箭頭和線條標示
3. 將此 canvas 轉為 PNG 送給 Nano Banana edit API
4. 顯示半透明 overlay + 施工中圖片 + "產生中 請等待" 文字
5. API 回傳後，新圖加入 history
6. 清空家具放置記錄和 textarea
7. Dr. Bubu 說："Construction complete. Here is your new home."

## 系統架構

**簡化的單一服務架構：**

```
使用者 → FastAPI (port 8000) → Gemini 2.5 Flash API → 回傳結果
         ├─ 圖像上傳 (POST /upload)
         ├─ 圖像編輯 (POST /edit)
         ├─ 圖像存取 (GET /images/<filename>)
         └─ 健康檢查 (GET /health)
```

### 核心功能

1. **圖像上傳** - 接收並儲存圖片到 `input/` 目錄
2. **AI 處理** - 使用 Gemini 2.5 Flash Image Preview 模型編輯圖像
3. **靜態服務** - 提供生成圖片的 HTTP 存取（`/images/` 端點）
4. **整合 API** - 單一端點完成上傳+處理（`/edit`）

## 開發環境設定

### 必要條件
- Python 3.11+
- Google AI Studio API Key

### 初始化設定

1. **安裝相依套件**
   ```bash
   cd simon-nb
   pip install -r requirements.txt
   ```

2. **設定環境變數**

   確認 `.env` 檔案包含：
   ```
   GOOGLE_API_KEY="your-api-key-from-google-ai-studio"
   BASE_URL="http://localhost:8000"
   ```

   從 [Google AI Studio](https://aistudio.google.com/app/apikey) 取得 API 金鑰

3. **建立必要目錄**
   ```bash
   mkdir -p input result
   ```

## 常用指令

### 啟動服務

```bash
# 開發模式（自動重載）
python app.py

# 或使用 uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

服務啟動後會在 http://localhost:8000

### API 測試

```bash
# 查看 API 資訊
curl http://localhost:8000/

# 健康檢查
curl http://localhost:8000/health

# 上傳圖片
curl -X POST -F "file=@/path/to/image.jpg" http://localhost:8000/upload

# 上傳並編輯圖片
curl -X POST \
  -F "file=@/path/to/image.jpg" \
  -F "prompt=將背景改成藍色" \
  http://localhost:8000/edit
```

### API 文件

FastAPI 自動產生的互動式文件：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 核心技術細節

### AI 模型配置
- 圖像生成模型: `gemini-2.5-flash-image-preview`
- Temperature: 1
- Top-p: 0.95
- Max tokens: 32768
- 支援 TEXT 和 IMAGE 雙模態輸出

### API 端點說明

#### GET `/`
取得 API 基本資訊和端點列表

#### POST `/upload`
上傳圖片到伺服器
- **Input**: `file` (multipart/form-data)
- **Output**: `{"status": "success", "file_path": "...", "filename": "..."}`

#### POST `/edit`
上傳並編輯圖片（一步完成）
- **Input**:
  - `file` (multipart/form-data) - 圖片檔案
  - `prompt` (form field) - 編輯指令
- **Output**: `{"status": "success", "image_urls": [...], "text": "..."}`

#### POST `/edit-from-path`
從已上傳的圖片進行編輯
- **Input**:
  - `file_path` (form field) - 已上傳圖片路徑
  - `prompt` (form field) - 編輯指令
- **Output**: `{"status": "success", "image_urls": [...], "text": "..."}`

#### GET `/images/{filename}`
存取生成的圖片（靜態檔案服務）

#### GET `/health`
健康檢查端點
- **Output**: `{"status": "healthy", "api_key_set": true/false}`

### 資料流程

1. 使用者透過 `/edit` 上傳圖片和提示
2. FastAPI 儲存圖片到 `input/` 目錄
3. 呼叫 `generate_nano_banana()` 函數：
   - 讀取圖片並轉換為 Base64
   - 傳送給 Gemini API
   - 接收生成的圖片
   - 儲存到 `result/` 目錄
4. 回傳圖片 URL：`http://localhost:8000/images/{uuid}.jpg`

### 目錄結構

```
simon-nb/
├── app.py              # FastAPI 主程式
├── .env                # 環境變數配置
├── requirements.txt    # Python 相依套件
├── input/              # 上傳的原始圖片
├── result/             # AI 生成的圖片
├── README.md           # 專案說明（英文）
└── README_zhtw.md      # 專案說明（繁中）
```

### 環境變數

- `GOOGLE_API_KEY` - Google AI Studio API 金鑰（必填）
- `BASE_URL` - 服務基礎 URL（預設: http://localhost:8000）

## 錯誤處理

常見錯誤和解決方法：

1. **ValueError: 請設定 GOOGLE_API_KEY 環境變數**
   - 確認 `.env` 檔案存在且包含有效的 API 金鑰

2. **圖片不存在錯誤**
   - 檢查 `input/` 目錄是否存在
   - 確認檔案路徑正確

3. **Gemini API 錯誤**
   - 檢查 API 金鑰是否有效
   - 確認網路連線正常
   - 檢查 API 配額是否用完

## 開發注意事項

1. **本地運行** - 此服務設計為 localhost 運行，URL 固定為 `http://localhost:8000`
2. **檔案清理** - `input/` 和 `result/` 目錄不會自動清理，需要手動管理
3. **API 限制** - 遵守 Google AI Studio 的 API 使用限制
4. **圖片格式** - 目前預設處理 JPEG 格式，其他格式可能需要調整

## 相關連結

- [Google AI Studio](https://aistudio.google.com/)
- [Google Gemini API 文件](https://ai.google.dev/gemini-api/docs)
- [FastAPI 文件](https://fastapi.tiangolo.com/)
