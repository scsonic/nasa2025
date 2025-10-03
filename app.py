"""
簡化版 Nano Banana API - 單一 FastAPI 服務
整合圖像上傳、處理和存取功能
"""

import os
import uuid
import base64
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

from google import genai
from google.genai import types

# 載入環境變數
load_dotenv()

# 初始化 FastAPI
app = FastAPI(
    title="Nano Banana API",
    description="圖像編輯與生成 API，使用 Google Gemini 2.5 Flash",
    version="1.0.0"
)

# CORS 設定（如果需要從網頁前端呼叫）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 建立必要的目錄
BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
RESULT_DIR = BASE_DIR / "result"
STATIC_DIR = BASE_DIR / "static"
INPUT_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# 掛載靜態檔案目錄
app.mount("/images", StaticFiles(directory=str(RESULT_DIR)), name="images")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

# 讀取環境變數
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("請設定 GOOGLE_API_KEY 環境變數")


class ImageEditRequest(BaseModel):
    """圖像編輯請求"""
    prompt: str
    image_url: Optional[str] = None


def generate_nano_banana(image_path: str, user_prompt: str, base_url: str = "http://localhost:8000") -> dict:
    """
    使用 Gemini 2.5 Flash 處理圖像

    Args:
        image_path: 本地圖像路徑
        user_prompt: 使用者的編輯指令
        base_url: 服務的基礎 URL

    Returns:
        dict: 包含狀態和結果圖像 URL 的字典
    """
    try:
        # 檢查檔案是否存在
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "message": f"圖片不存在: {image_path}"
            }

        # 讀取並轉換圖片為 Base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # 初始化 Gemini 客戶端
        client = genai.Client(
            vertexai=False,
            api_key=GOOGLE_API_KEY
        )

        # 準備圖片和提示
        image_part = types.Part.from_bytes(
            data=base64.b64decode(encoded_string),
            mime_type="image/jpeg",
        )

        contents = [
            types.Content(
                role="user",
                parts=[image_part, types.Part.from_text(text=user_prompt)]
            ),
        ]

        # 設定生成參數
        config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            max_output_tokens=32768,
            response_modalities=["TEXT", "IMAGE"],
        )

        # 呼叫 Gemini API
        image_urls = []
        text_output = []

        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash-image-preview",
            contents=contents,
            config=config
        ):
            # 收集文字輸出
            if getattr(chunk, "text", None):
                text_output.append(chunk.text)

            # 處理生成的圖片
            for candidate in getattr(chunk, "candidates", []) or []:
                parts = getattr(candidate, "content", None) and candidate.content.parts or []
                for part in parts:
                    if getattr(part, "inline_data", None):
                        # 生成唯一檔名
                        image_filename = f"{uuid.uuid4()}.jpg"
                        image_filepath = RESULT_DIR / image_filename

                        # 儲存圖片
                        with open(image_filepath, "wb") as f:
                            f.write(part.inline_data.data)

                        # 產生 URL
                        image_url = f"{base_url}/images/{image_filename}"
                        image_urls.append(image_url)

        if image_urls:
            return {
                "status": "success",
                "image_urls": image_urls,
                "text": "".join(text_output) if text_output else None
            }
        else:
            return {
                "status": "error",
                "message": "未生成圖片",
                "text": "".join(text_output) if text_output else None
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"處理失敗: {str(e)}"
        }


@app.get("/")
def root():
    """Demo 網站首頁"""
    from fastapi.responses import FileResponse
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    上傳圖片到伺服器

    Returns:
        dict: 包含上傳圖片路徑的字典
    """
    try:
        # 產生唯一檔名
        file_extension = os.path.splitext(file.filename)[1] or ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = INPUT_DIR / unique_filename

        # 儲存檔案
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "status": "success",
            "file_path": str(file_path),
            "filename": unique_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上傳失敗: {str(e)}")
    finally:
        file.file.close()


@app.post("/api/edit")
async def edit_image(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    """
    上傳圖片並直接編輯

    Args:
        file: 要編輯的圖片檔案
        prompt: 編輯指令

    Returns:
        dict: 包含編輯結果的字典
    """
    try:
        # 先上傳圖片
        file_extension = os.path.splitext(file.filename)[1] or ".jpg"
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = INPUT_DIR / unique_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 取得當前請求的 base URL
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        # 處理圖片
        result = generate_nano_banana(
            image_path=str(file_path),
            user_prompt=prompt,
            base_url=base_url
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"編輯失敗: {str(e)}")
    finally:
        file.file.close()


@app.post("/api/edit-from-path")
async def edit_from_path(
    file_path: str = Form(...),
    prompt: str = Form(...)
):
    """
    從已上傳的圖片路徑進行編輯

    Args:
        file_path: 已上傳圖片的路徑
        prompt: 編輯指令

    Returns:
        dict: 包含編輯結果的字典
    """
    try:
        # 取得當前請求的 base URL
        base_url = os.getenv("BASE_URL", "http://localhost:8000")

        # 處理圖片
        result = generate_nano_banana(
            image_path=file_path,
            user_prompt=prompt,
            base_url=base_url
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"編輯失敗: {str(e)}")


@app.get("/health")
def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "api_key_set": bool(GOOGLE_API_KEY)
    }


if __name__ == "__main__":
    # 本地開發用
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
