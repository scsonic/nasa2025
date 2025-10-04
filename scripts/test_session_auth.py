#!/usr/bin/env python3
"""
測試 Session 認證機制
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_generate_session():
    """測試生成 session"""
    print("=" * 60)
    print("測試 1: 生成 Session")
    print("=" * 60)
    
    response = requests.post(f"{BASE_URL}/api/session/generate")
    data = response.json()
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if data['status'] == 'success':
        session_id = data['session_id']
        secret = data['secret']
        print(f"\n✅ Session ID: {session_id}")
        print(f"✅ Secret: {secret}")
        print(f"✅ Session ID 長度: {len(session_id)} (應該是 5)")
        print(f"✅ Secret 長度: {len(secret)} (應該是 10)")
        return session_id, secret
    else:
        print("❌ 生成失敗")
        return None, None

def test_valid_session(session_id, secret):
    """測試有效的 session"""
    print("\n" + "=" * 60)
    print("測試 2: 使用有效的 Session 和 Secret")
    print("=" * 60)
    
    # 建立測試圖片
    import io
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {
        'file': ('test.png', img_bytes, 'image/png')
    }
    
    data = {
        'prompt': 'test prompt',
        'session_id': session_id,
        'secret': secret
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/edit", files=files, data=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 認證成功！")
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ 請求失敗: {response.text}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def test_invalid_secret(session_id):
    """測試無效的 secret"""
    print("\n" + "=" * 60)
    print("測試 3: 使用錯誤的 Secret")
    print("=" * 60)
    
    import io
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {
        'file': ('test.png', img_bytes, 'image/png')
    }
    
    data = {
        'prompt': 'test prompt',
        'session_id': session_id,
        'secret': 'wrongsecret'  # 錯誤的 secret
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/edit", files=files, data=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ 正確拒絕了無效的 secret！")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ 應該返回 403，但返回了 {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def test_invalid_session_id():
    """測試無效的 session ID"""
    print("\n" + "=" * 60)
    print("測試 4: 使用錯誤的 Session ID")
    print("=" * 60)
    
    import io
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    files = {
        'file': ('test.png', img_bytes, 'image/png')
    }
    
    data = {
        'prompt': 'test prompt',
        'session_id': 'XXXXX',  # 錯誤的 session ID
        'secret': '1234567890'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/edit", files=files, data=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ 正確拒絕了無效的 session ID！")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ 應該返回 403，但返回了 {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def test_multiple_sessions():
    """測試生成多個不同的 session"""
    print("\n" + "=" * 60)
    print("測試 5: 生成多個 Session（驗證唯一性）")
    print("=" * 60)
    
    sessions = []
    for i in range(3):
        response = requests.post(f"{BASE_URL}/api/session/generate")
        data = response.json()
        if data['status'] == 'success':
            sessions.append((data['session_id'], data['secret']))
            print(f"Session {i+1}: {data['session_id']} / {data['secret']}")
    
    # 檢查是否都不同
    session_ids = [s[0] for s in sessions]
    secrets = [s[1] for s in sessions]
    
    if len(set(session_ids)) == len(session_ids):
        print("✅ 所有 Session ID 都是唯一的")
    else:
        print("❌ 發現重複的 Session ID")
    
    if len(set(secrets)) == len(secrets):
        print("✅ 所有 Secret 都是唯一的")
    else:
        print("❌ 發現重複的 Secret")

def main():
    print("\n🍌 Nano Banana - Session 認證測試\n")
    
    try:
        # 測試 1: 生成 session
        session_id, secret = test_generate_session()
        
        if session_id and secret:
            # 測試 2: 有效的認證
            test_valid_session(session_id, secret)
            
            # 測試 3: 無效的 secret
            test_invalid_secret(session_id)
            
            # 測試 4: 無效的 session ID
            test_invalid_session_id()
            
            # 測試 5: 多個 session
            test_multiple_sessions()
        
        print("\n" + "=" * 60)
        print("✅ 所有測試完成")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 無法連接到服務器")
        print("請確認服務器正在運行: python app.py")
    except Exception as e:
        print(f"\n❌ 測試失敗: {e}")

if __name__ == "__main__":
    main()
