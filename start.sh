#!/bin/bash

# Nano Banana API 啟動腳本
# 使用 uvicorn 以多 worker 模式運行

# 設定變數
APP_MODULE="app:app"
HOST="0.0.0.0"
PORT=8000
WORKERS=3  # 四核 CPU 建議使用 3 個 workers (留一核給系統)
LOG_LEVEL="info"

# 取得腳本所在目錄
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 檢查 .env 文件是否存在
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env 文件不存在，請確認環境變數設定"
    echo "可以參考 .env.example 創建 .env 文件"
fi

# 啟動 uvicorn
echo "🚀 啟動 Nano Banana API..."
echo "📍 工作目錄: $SCRIPT_DIR"
echo "🔧 Workers: $WORKERS"
echo "🌐 監聽地址: $HOST:$PORT"
echo "----------------------------------------"

exec uvicorn $APP_MODULE \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --log-level $LOG_LEVEL \
    --access-log \
    --proxy-headers \
    --forwarded-allow-ips='*'
