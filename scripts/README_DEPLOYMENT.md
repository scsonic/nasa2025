# 部署說明

## 快速部署步驟

### 1. 設定啟動腳本權限

```bash
chmod +x start.sh
```

### 2. 測試啟動腳本

```bash
./start.sh
```

按 `Ctrl+C` 停止測試。

### 3. 安裝 systemd 服務

```bash
# 複製 service 文件到 systemd 目錄
sudo cp scripts/bubu.service /etc/systemd/system/

# 重新載入 systemd
sudo systemctl daemon-reload

# 啟用服務（開機自動啟動）
sudo systemctl enable bubu

# 啟動服務
sudo systemctl start bubu
```

### 4. 管理服務

```bash
# 查看服務狀態
sudo systemctl status bubu

# 停止服務
sudo systemctl stop bubu

# 重啟服務
sudo systemctl restart bubu

# 查看日誌
sudo journalctl -u bubu -f

# 查看最近 100 行日誌
sudo journalctl -u bubu -n 100
```

## 配置說明

### Workers 數量建議

- **2 核 CPU**: 1-2 workers
- **4 核 CPU**: 3 workers (當前設定)
- **8 核 CPU**: 6-7 workers
- **16 核 CPU**: 12-14 workers

公式: `workers = (CPU 核心數 × 2) - 1` 或 `CPU 核心數 - 1`

### 修改 Workers 數量

編輯 `start.sh`:

```bash
WORKERS=3  # 改成你想要的數量
```

### 修改部署路徑

當前配置路徑為 `/var/www/html/nasa2025`。

如需修改，請編輯 `scripts/bubu.service`:

```ini
WorkingDirectory=/your/actual/path
Environment="PATH=/your/actual/path/venv/bin:..."
ExecStart=/your/actual/path/start.sh
```

### 修改運行用戶

預設使用 `www-data` 用戶，如需修改請編輯 `scripts/bubu.service`:

```ini
User=your_username
Group=your_groupname
```

## 環境變數

確保 `.env` 文件存在且包含必要的配置:

```bash
# 複製範例文件
cp .env.example .env

# 編輯環境變數
nano .env
```

## 防火牆設定

如果使用防火牆，請開放 8000 端口:

```bash
# UFW
sudo ufw allow 8000/tcp

# firewalld
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

## Nginx 反向代理 (可選)

如果想使用 Nginx 作為反向代理:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 故障排除

### 服務無法啟動

```bash
# 查看詳細錯誤
sudo journalctl -u bubu -n 50 --no-pager

# 檢查權限
ls -la /var/www/html/nasa2025/
ls -la /var/www/html/nasa2025/start.sh

# 手動測試啟動
cd /var/www/html/nasa2025
./start.sh
```

### 端口被占用

```bash
# 查看誰在使用 8000 端口
sudo lsof -i :8000

# 或使用 netstat
sudo netstat -tlnp | grep 8000
```

### 修改端口

編輯 `start.sh`:

```bash
PORT=8080  # 改成其他端口
```

## 性能監控

```bash
# 查看資源使用
htop

# 查看 Python 進程
ps aux | grep uvicorn

# 查看連接數
ss -s
```
