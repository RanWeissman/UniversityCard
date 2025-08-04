
from io import BytesIO
import os
from pathlib import Path
import uuid

from card_generator import create_card, delete_file_later  # Replace with your actual import
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import uvicorn

app = FastAPI()

os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

Path("static/cards").mkdir(parents=True, exist_ok=True)
Path("uploads").mkdir(parents=True, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
def generate_card(
    request: Request,
    name: str = Form(...),
    id_number: str = Form(...),
    file: UploadFile = File(...)
):
    if file.content_type not in ["image/png", "image/jpeg"]:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": "Only PNG and JPEG files are allowed."
        })

    # ext = ".png" if file.content_type == "image/png" else ".jpg"
    # image_filename = f"{uuid.uuid4()}{ext}"
    # image_path = f"uploads/{image_filename}"
    # with open(image_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)
    #
    # output_path = f"static/cards/{card_filename}"
    # template_path = "template.png"  # Adjust this path as needed

    file_bytes = file.file.read()
    user_image = Image.open(BytesIO(file_bytes)).convert("RGBA")
    template_path = "template.png"

    card_image = create_card(name, id_number, template_path, user_image)
    card_filename = f"card_{uuid.uuid4()}.png"
    card_image.save(f"static/cards/{card_filename}")
    delete_file_later(f"static/cards/{card_filename}", delay=5)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "card_url": f"/static/cards/{card_filename}"
    })


if __name__ == "__main__":
    uvicorn.run(
        "main:app",       # module:attribute
        host="127.0.0.1",  # or "0.0.0.0" to listen on all interfaces
        port=8000,
        reload=True       # set to False in production
    )
