import io

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
THUMBNAIL_SIZE = (128, 128)

app = FastAPI(title="Thumbnail Forge")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/thumbnails", responses={200: {"content": {"image/png": {}}}})
async def create_thumbnail(file: UploadFile = File(...)) -> Response:
    raw = await file.read(MAX_UPLOAD_BYTES + 1)
    if not raw:
        raise HTTPException(status_code=400, detail="empty upload")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="upload larger than 10 MiB")
    try:
        with Image.open(io.BytesIO(raw)) as image:
            thumbnail = ImageOps.fit(ImageOps.exif_transpose(image).convert("RGBA"), THUMBNAIL_SIZE)
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError) as exc:
        raise HTTPException(status_code=415, detail=f"not a supported image: {exc}") from exc
    out = io.BytesIO()
    thumbnail.save(out, format="PNG", optimize=True)
    return Response(content=out.getvalue(), media_type="image/png")
