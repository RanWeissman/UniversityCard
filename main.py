
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import uuid
import os
from pathlib import Path
import uvicorn


# Import your card creation function
from card_generator import create_card  # Replace with your actual import

app = FastAPI()


os.makedirs("static", exist_ok=True)

# Mount static folder for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure folders exist
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

    ext = ".png" if file.content_type == "image/png" else ".jpg"
    image_filename = f"{uuid.uuid4()}{ext}"
    image_path = f"uploads/{image_filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    card_filename = f"card_{uuid.uuid4()}.png"
    output_path = f"static/cards/{card_filename}"
    template_path = "template.png"  # Adjust this path as needed

    create_card(name, id_number, image_path, template_path, output_path)

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



