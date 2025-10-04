# Session 認證機制說明

## 🔒 安全機制

為了防止未授權的 API 呼叫，系統實作了 session 認證機制。

### 工作原理

1. **Session 生成**：每次開啟網頁時，前端向後端請求生成新的 session
2. **Secret 計算**：後端使用 HMAC-SHA256 從 session_id 生成對應的 secret
3. **驗證機制**：每次 API 呼叫都必須提供正確的 session_id 和 secret 配對
4. **一次性使用**：重新整理頁面後，secret 會消失，需要重新生成

## 📋 實作細節

### Session ID 格式

- **長度**: 5 個字元
- **字元集**: 大小寫英文字母 + 數字 (a-z, A-Z, 0-9)
- **範例**: `aB3xZ`, `K9mPq`, `tY7Wn`
- **生成方式**: 使用 Python `secrets` 模組（密碼學安全的隨機數）

### Secret 生成

```python
def generate_secret(session_id: str) -> str:
    """
    從 session_id 生成 secret
    使用 HMAC-SHA256 並取前 10 個字元
    """
    message = f"{session_id}{SECRET_SALT}".encode('utf-8')
    hash_obj = hashlib.sha256(message)
    return hash_obj.hexdigest()[:10]
```

- **演算法**: SHA256
- **Salt**: 從環境變數 `SESSION_SECRET_SALT` 讀取
- **輸出長度**: 10 個字元（hex）
- **範例**: 如果 session_id 是 `aB3xZ`，secret 可能是 `7f8a9b2c3d`

### 驗證流程

```python
def verify_session(session_id: str, secret: str) -> bool:
    """
    驗證 session_id 和 secret 是否匹配
    """
    expected_secret = generate_secret(session_id)
    return secrets.compare_digest(secret, expected_secret)
```

使用 `secrets.compare_digest()` 防止時序攻擊（timing attack）。

## 🔄 使用流程

### 1. 開啟網頁

```javascript
// index.html 載入時自動執行
async function init() {
    await generateSession();  // 向後端請求 session
    // ...
}

async function generateSession() {
    const response = await fetch('/api/session/generate', {
        method: 'POST'
    });
    
    const data = await response.json();
    sessionId = data.session_id;      // 例如: "aB3xZ"
    sessionSecret = data.secret;       // 例如: "7f8a9b2c3d"
}
```

**後端回應**:
```json
{
  "status": "success",
  "session_id": "aB3xZ",
  "secret": "7f8a9b2c3d"
}
```

### 2. 呼叫 API

```javascript
// 產生圖片時
const formData = new FormData();
formData.append('file', blob, 'design.png');
formData.append('prompt', 'test prompt');
formData.append('session_id', sessionId);    // 必須
formData.append('secret', sessionSecret);     // 必須

const response = await fetch('/api/edit', {
    method: 'POST',
    body: formData
});
```

**後端驗證**:
```python
@app.post("/api/edit")
async def edit_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    session_id: str = Form(...),
    secret: str = Form(...)
):
    # 驗證 session
    if not verify_session(session_id, secret):
        raise HTTPException(status_code=403, detail="Invalid session or secret")
    
    # 驗證通過，繼續處理...
```

### 3. 分享功能

分享時**只使用 session_id**，不包含 secret：

```javascript
function handleShare() {
    const shareUrl = `${window.location.origin}/share/${sessionId}`;
    // 只分享 session_id，secret 保持私密
}
```

分享連結範例：`http://localhost:8000/share/aB3xZ`

## 🛡️ 安全特性

### 1. 密碼學安全的隨機數

使用 Python `secrets` 模組生成 session_id，而非 `random`：

```python
import secrets
import string

chars = string.ascii_letters + string.digits
session_id = ''.join(secrets.choice(chars) for _ in range(5))
```

### 2. HMAC-SHA256

使用 SHA256 雜湊演算法，加上 secret salt：

```python
message = f"{session_id}{SECRET_SALT}".encode('utf-8')
hash_obj = hashlib.sha256(message)
secret = hash_obj.hexdigest()[:10]
```

### 3. 時序攻擊防護

使用 `secrets.compare_digest()` 進行常數時間比較：

```python
return secrets.compare_digest(secret, expected_secret)
```

### 4. Secret 不外洩

- Secret 只在記憶體中存在
- 不儲存在 localStorage 或 cookie
- 不出現在 URL 中
- 重新整理頁面後消失

### 5. 可配置的 Salt

透過環境變數設定 salt，增加安全性：

```env
SESSION_SECRET_SALT=your-custom-secret-salt-here
```

## 🧪 測試

使用測試腳本驗證功能：

```bash
python scripts/test_session_auth.py
```

測試項目：
1. ✅ 生成 session
2. ✅ 有效的 session 和 secret
3. ✅ 無效的 secret（應該被拒絕）
4. ✅ 無效的 session_id（應該被拒絕）
5. ✅ 多個 session 的唯一性

## 📊 錯誤處理

### 403 Forbidden

當 session 或 secret 無效時：

```json
{
  "detail": "Invalid session or secret"
}
```

**可能原因**:
- Secret 錯誤
- Session ID 錯誤
- Session ID 和 secret 不匹配

**解決方法**:
- 重新整理頁面獲取新的 session
- 檢查前端是否正確傳送 session_id 和 secret

## 🔍 除錯

### 查看 Session 生成

開啟瀏覽器 Console：

```javascript
console.log('Session ID:', sessionId);
console.log('Secret:', sessionSecret);
```

### 查看後端驗證

後端會輸出驗證結果：

```
✅ Session verified: aB3xZ
```

### 測試 Secret 生成

在 Python 中測試：

```python
from app import generate_session_id, generate_secret, verify_session

# 生成
session_id = generate_session_id()
secret = generate_secret(session_id)

print(f"Session ID: {session_id}")
print(f"Secret: {secret}")

# 驗證
is_valid = verify_session(session_id, secret)
print(f"Valid: {is_valid}")  # 應該是 True

# 測試錯誤的 secret
is_valid = verify_session(session_id, "wrongsecret")
print(f"Valid: {is_valid}")  # 應該是 False
```

## ⚠️ 注意事項

### 1. Secret Salt 安全

- **不要** 將 `SESSION_SECRET_SALT` 提交到 git
- **建議** 在生產環境使用強隨機字串
- **建議** 定期更換 salt（會使舊 session 失效）

### 2. Session 生命週期

- Session 只在當前瀏覽器 tab 有效
- 重新整理頁面會生成新的 session
- 沒有過期時間（stateless 設計）

### 3. 分享連結

- 分享連結只包含 session_id
- 任何人都可以查看分享的內容
- 但無法使用該 session_id 產生新圖片（因為沒有 secret）

### 4. 效能考量

- SHA256 計算非常快速（微秒級）
- 不需要資料庫查詢
- 完全 stateless，易於擴展

## 🎯 最佳實踐

### 開發環境

```env
SESSION_SECRET_SALT=dev-secret-2025
```

### 生產環境

```env
SESSION_SECRET_SALT=prod-$(openssl rand -hex 32)
```

生成強隨機 salt：

```bash
openssl rand -hex 32
# 輸出例如: 7f8a9b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0
```

## 📝 總結

這個認證機制提供了：

- ✅ **簡單**: 5 字元 session ID，易於分享
- ✅ **安全**: HMAC-SHA256 + secret salt
- ✅ **快速**: 無需資料庫，純計算驗證
- ✅ **Stateless**: 易於水平擴展
- ✅ **隱私**: Secret 不外洩，重開即失效

適合用於：
- 防止未授權的 API 呼叫
- 簡單的 session 管理
- 不需要長期持久化的場景
