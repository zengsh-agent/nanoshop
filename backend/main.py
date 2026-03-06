import os
import io
import base64
import uuid
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

app = FastAPI(title="NanoShop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo (use Redis in production)
sessions: Dict[str, Dict] = {}

# Allowed image formats
ALLOWED_FORMATS = {"jpg", "jpeg", "png", "webp", "bmp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_DIM = 2048


def validate_image(file: UploadFile) -> bool:
    """Validate image format."""
    ext = file.filename.split(".")[-1].lower()
    return ext in ALLOWED_FORMATS


def process_image(image: Image.Image) -> Image.Image:
    """Resize large images while maintaining aspect ratio."""
    if max(image.size) > MAX_IMAGE_DIM:
        ratio = MAX_IMAGE_DIM / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def apply_operation(image: Image.Image, operation: Dict) -> Image.Image:
    """Apply a single operation to the image."""
    op_type = operation.get("type")
    value = operation.get("value", 1.0)

    if op_type == "brightness":
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(value)
    elif op_type == "contrast":
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(value)
    elif op_type == "saturation":
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(value)
    elif op_type == "sharpness":
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(value)
    elif op_type == "blur":
        radius = int(value * 10)
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    elif op_type == "sharpen":
        return image.filter(ImageFilter.SHARPEN)
    elif op_type == "rotate":
        return image.rotate(value, expand=True)
    elif op_type == "flip_horizontal":
        return ImageOps.mirror(image)
    elif op_type == "flip_vertical":
        return ImageOps.flip(image)
    elif op_type == "grayscale":
        return ImageOps.grayscale(image).convert("RGB")
    elif op_type == "invert":
        return ImageOps.invert(image)
    elif op_type == "solarize":
        return ImageOps.solarize(image, threshold=int(value * 256))
    elif op_type == "equalize":
        return ImageOps.equalize(image)
    elif op_type == "autocontrast":
        return ImageOps.autocontrast(image)
    elif op_type == "sepia":
        # Apply sepia filter
        img_array = np.array(image).astype(np.float32)
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        sepia = np.dot(img_array[..., :3], sepia_matrix.T)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        if image.mode == "RGBA":
            sepia = np.dstack([sepia, img_array[..., 3]])
        return Image.fromarray(sepia)
    elif op_type == "vintage":
        # Vintage effect: slight blur + sepia + reduced saturation
        img = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(0.8)
        return apply_operation(img, {"type": "sepia", "value": 0.5})
    elif op_type == "noir":
        # Noir effect: high contrast grayscale
        img = ImageOps.grayscale(image)
        img = ImageOps.autocontrast(img)
        return img.convert("RGB")
    elif op_type == "vivid":
        # Vivid: increased saturation and contrast
        img = ImageEnhance.Color(image).enhance(1.5)
        return ImageEnhance.Contrast(img).enhance(1.2)
    else:
        return image


def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL Image to base64 string."""
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode()


def base64_to_image(b64_str: str) -> Image.Image:
    """Convert base64 string to PIL Image."""
    img_data = base64.b64decode(b64_str)
    return Image.open(io.BytesIO(img_data))


def get_ai_suggestion(session: Dict, user_message: str) -> Dict:
    """Get AI suggestion for image editing (simple keyword-based)."""
    text_lower = user_message.lower()
    operations = []

    # Simple keyword matching
    if any(word in text_lower for word in ["bright", "lighter", "lighten"]):
        operations.append({"type": "brightness", "value": 1.3})
    elif any(word in text_lower for word in ["dark", "darker", "dim"]):
        operations.append({"type": "brightness", "value": 0.7})

    if any(word in text_lower for word in ["contrast", "pop", "dynamic"]):
        operations.append({"type": "contrast", "value": 1.3})

    if any(word in text_lower for word in ["saturate", "colorful", "vibrant", "color", "warm"]):
        operations.append({"type": "saturation", "value": 1.5})

    if any(word in text_lower for word in ["desaturate", "less color", "muted"]):
        operations.append({"type": "saturation", "value": 0.5})

    if any(word in text_lower for word in ["blur", "soft", "smooth", "dreamy"]):
        operations.append({"type": "blur", "value": 0.4})

    if any(word in text_lower for word in ["sharp", "crisp", "clear", "detail"]):
        operations.append({"type": "sharpen", "value": 1.0})

    if any(word in text_lower for word in ["rotate", "turn", "spin"]):
        operations.append({"type": "rotate", "value": 90})

    if any(word in text_lower for word in ["flip", "mirror"]):
        if "horizontal" in text_lower:
            operations.append({"type": "flip_horizontal", "value": 1})
        else:
            operations.append({"type": "flip_vertical", "value": 1})

    if any(word in text_lower for word in ["black white", "grayscale", "bw", "monochrome", "b&w"]):
        operations.append({"type": "grayscale", "value": 1})

    if any(word in text_lower for word in ["sepia", "old", "retro"]):
        operations.append({"type": "vintage", "value": 1})

    if any(word in text_lower for word in ["noir", "dramatic", "dark mood", "film"]):
        operations.append({"type": "noir", "value": 1})

    if any(word in text_lower for word in ["vivid", "bright", "enhance", "boost"]):
        operations.append({"type": "vivid", "value": 1})

    if any(word in text_lower for word in ["auto", "improve", "fix", "enhance"]):
        operations.append({"type": "autocontrast", "value": 1})
        operations.append({"type": "saturation", "value": 1.1})

    # Default: auto-enhance if no specific operation detected
    if not operations:
        operations.append({"type": "autocontrast", "value": 1})

    # Generate response message
    op_names = [op["type"] for op in operations]
    message = f"I suggest applying: {', '.join(op_names)}. "
    message += "These adjustments should help achieve the effect you're looking for. Click on an operation to apply it!"

    return {
        "success": True,
        "message": message,
        "suggested_operations": operations
    }


@app.get("/")
async def root():
    return {"message": "NanoShop API is running", "version": "1.0.0"}


@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload and process an image."""
    if not validate_image(file):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format. Allowed: {', '.join(ALLOWED_FORMATS)}"
        )

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB.")

    try:
        image = Image.open(io.BytesIO(contents))
        image = process_image(image)

        session_id = str(uuid.uuid4())
        original_b64 = image_to_base64(image)

        sessions[session_id] = {
            "original": original_b64,
            "current": original_b64,
            "operations": [],
            "conversation": [],
            "created_at": datetime.now().isoformat()
        }

        return {
            "success": True,
            "session_id": session_id,
            "image": original_b64,
            "message": "Image uploaded successfully! Tell me how you'd like to edit it."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/api/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...)
):
    """Chat with AI about image editing."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    # Add user message to conversation
    session["conversation"].append({"role": "user", "content": message, "timestamp": datetime.now().isoformat()})

    # Get AI suggestion (simple keyword-based)
    ai_result = get_ai_suggestion(session, message)

    # Add AI response to conversation
    session["conversation"].append({
        "role": "assistant",
        "content": ai_result["message"],
        "timestamp": datetime.now().isoformat()
    })

    return {
        "success": True,
        "message": ai_result["message"],
        "suggested_operations": ai_result.get("suggested_operations", [])
    }


@app.post("/api/apply")
async def apply_operation_endpoint(
    session_id: str = Form(...),
    operation: str = Form(...),
    value: float = Form(1.0)
):
    """Apply an operation to the image."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    current_image = base64_to_image(session["current"])

    # Apply operation
    op_dict = {"type": operation, "value": value}
    new_image = apply_operation(current_image, op_dict)

    # Update session
    session["current"] = image_to_base64(new_image)
    session["operations"].append(op_dict)

    return {
        "success": True,
        "image": session["current"],
        "operation": operation,
        "message": f"Applied {operation}!"
    }


@app.post("/api/preview")
async def preview_operation(
    session_id: str = Form(...),
    operation: str = Form(...),
    value: float = Form(1.0)
):
    """Preview an operation without applying."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    current_image = base64_to_image(session["current"])

    # Apply operation for preview
    op_dict = {"type": operation, "value": value}
    preview_image = apply_operation(current_image, op_dict)

    return {
        "success": True,
        "preview": image_to_base64(preview_image)
    }


@app.post("/api/undo")
async def undo_operation(session_id: str = Form(...)):
    """Undo the last operation."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    if not session["operations"]:
        return {"success": False, "message": "No operations to undo"}

    # Remove last operation
    session["operations"].pop()

    # Replay remaining operations on original
    original = base64_to_image(session["original"])
    current = original

    for op in session["operations"]:
        current = apply_operation(current, op)

    session["current"] = image_to_base64(current)

    return {
        "success": True,
        "image": session["current"],
        "message": "Undone last operation"
    }


@app.post("/api/reset")
async def reset_image(session_id: str = Form(...)):
    """Reset image to original."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    session["current"] = session["original"]
    session["operations"] = []

    return {
        "success": True,
        "image": session["current"],
        "message": "Image reset to original"
    }


@app.get("/api/image/{session_id}")
async def get_image(session_id: str):
    """Get current image state."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    return {
        "success": True,
        "image": session["current"],
        "original": session["original"],
        "operations": session["operations"]
    }


@app.post("/api/export")
async def export_image(
    session_id: str = Form(...),
    format: str = Form("png")
):
    """Export the edited image."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]
    image = base64_to_image(session["current"])

    # Validate format
    format = format.lower()
    if format not in ["png", "jpg", "jpeg", "webp"]:
        format = "png"

    output = io.BytesIO()
    if format in ["jpg", "jpeg"]:
        image.save(output, format="JPEG", quality=95)
    else:
        image.save(output, format=format.upper())

    output.seek(0)

    return StreamingResponse(
        output,
        media_type=f"image/{format}",
        headers={"Content-Disposition": f"attachment; filename=nanoshop_export.{format}"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
