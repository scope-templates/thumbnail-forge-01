# Thumbnail Forge

Thumbnail Forge, an image thumbnail service. Post an image, get a 128x128 PNG back, centre-cropped to a square.

## Run locally

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

```sh
curl localhost:8000/health
curl -F file=@photo.jpg localhost:8000/thumbnails -o thumb.png
```

## Container image

```sh
docker build -t thumbnail-forge .
docker run --rm -p 8000:8000 thumbnail-forge
```

The image is built in two stages (dependencies into a virtualenv, then a slim runtime), runs as a non-root user,
exposes 8000 and listens on `PORT` when that is set, for example `-e PORT=9000 -p 9000:9000`.

## Routes

| Method | Path          | Description                                                                                   |
| ------ | ------------- | --------------------------------------------------------------------------------------------- |
| GET    | `/health`     | `{"ok": true}`                                                                                |
| POST   | `/thumbnails` | multipart field `file`; returns `image/png` 128x128. 400 empty, 413 over 10 MiB, 415 not an image |

## Environment

| Variable | Default | Purpose     |
| -------- | ------- | ----------- |
| `PORT`   | `8000`  | listen port |
