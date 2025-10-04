"""
測試 GCS 連線和上傳功能
"""

import os
from google.cloud import storage
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_gcs_connection():
    """測試 GCS 連線"""
    print("🔍 測試 GCS 連線...")
    
    bucket_name = os.getenv("GCS_BUCKET_NAME", "team-bubu")
    
    try:
        # 初始化 client
        client = storage.Client()
        print(f"✅ GCS client 初始化成功")
        
        # 檢查 bucket
        bucket = client.bucket(bucket_name)
        if bucket.exists():
            print(f"✅ Bucket '{bucket_name}' 存在")
        else:
            print(f"❌ Bucket '{bucket_name}' 不存在")
            return False
        
        # 列出一些檔案
        blobs = list(client.list_blobs(bucket_name, max_results=5))
        print(f"📁 找到 {len(blobs)} 個檔案（最多顯示 5 個）:")
        for blob in blobs:
            print(f"   - {blob.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 連線失敗: {e}")
        return False

def test_upload():
    """測試上傳功能"""
    print("\n📤 測試上傳功能...")
    
    bucket_name = os.getenv("GCS_BUCKET_NAME", "team-bubu")
    
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # 建立測試檔案
        test_content = b"This is a test file from FastAPI"
        test_filename = "test_upload.txt"
        
        # 上傳到 result 資料夾
        blob = bucket.blob(f"result/{test_filename}")
        blob.upload_from_string(test_content, content_type="text/plain")
        
        # 產生公開 URL
        public_url = f"https://storage.googleapis.com/{bucket_name}/result/{test_filename}"
        
        print(f"✅ 上傳成功!")
        print(f"📍 URL: {public_url}")
        
        # 測試是否可以公開存取
        import requests
        response = requests.head(public_url)
        if response.status_code == 200:
            print(f"✅ 檔案可以公開存取 (HTTP {response.status_code})")
        else:
            print(f"⚠️  檔案無法公開存取 (HTTP {response.status_code})")
        
        return True
        
    except Exception as e:
        print(f"❌ 上傳失敗: {e}")
        return False

def main():
    print("=" * 60)
    print("🍌 Nano Banana - GCS 測試")
    print("=" * 60)
    
    # 檢查環境變數
    use_gcs = os.getenv("USE_GCS", "false")
    bucket_name = os.getenv("GCS_BUCKET_NAME", "team-bubu")
    
    print(f"\n⚙️  環境設定:")
    print(f"   USE_GCS: {use_gcs}")
    print(f"   GCS_BUCKET_NAME: {bucket_name}")
    print()
    
    # 執行測試
    connection_ok = test_gcs_connection()
    
    if connection_ok:
        upload_ok = test_upload()
        
        if upload_ok:
            print("\n" + "=" * 60)
            print("🎉 所有測試通過！GCS 已準備就緒。")
            print("=" * 60)
            print("\n現在可以啟動 FastAPI 服務：")
            print("  python app.py")
        else:
            print("\n⚠️  上傳測試失敗")
    else:
        print("\n⚠️  連線測試失敗")
        print("\n請確認：")
        print("1. 已執行: gcloud auth application-default login")
        print("2. .env 中的 GCS_BUCKET_NAME 正確")
        print("3. 有權限存取該 bucket")

if __name__ == "__main__":
    main()
