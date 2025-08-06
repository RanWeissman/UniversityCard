# pip install Pillow
# pip install fastapi[all]

# uvicorn main:app --reload

from PIL import Image, ImageDraw, ImageFont
import threading
import time
import os


def round_card_edges(image: Image, corner_radius: float = 40):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, *image.size), radius=corner_radius, fill=255)

    rounded = Image.new("RGBA", image.size)
    rounded.paste(image, (0, 0), mask=mask)
    return rounded


def create_rounded_profile_photo(user_image: Image):
    # Open and resize image
    size = (225, 225)
    corner_radius = 20
    border_width = 5
    border_color = "orange"

    user_image = user_image.resize(size, Image.Resampling.LANCZOS)

    # Create mask with rounded corners
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=corner_radius, fill=255)

    # Apply the rounded mask
    rounded_img = Image.new("RGBA", size)
    rounded_img.paste(user_image, (0, 0), mask)

    # Add border/frame
    border_size = (size[0] + 2 * border_width, size[1] + 2 * border_width)
    framed = Image.new("RGBA", border_size, (0, 0, 0, 0))

    border_mask = Image.new("L", border_size, 0)
    draw = ImageDraw.Draw(border_mask)
    draw.rounded_rectangle(
        (0, 0, border_size[0], border_size[1]), radius=corner_radius + border_width, fill=255
    )
    draw.rounded_rectangle(
        (border_width, border_width, border_size[0] - border_width, border_size[1] - border_width),
        radius=corner_radius, fill=0)

    draw_framed = ImageDraw.Draw(framed)
    draw_framed.bitmap((0, 0), border_mask, fill=border_color)

    # Paste the rounded image into the framed one
    framed.paste(rounded_img, (border_width, border_width), rounded_img)

    return framed


def create_card(name: str, id_n: str, template_path: str, user_image: Image):
    template = Image.open(template_path).convert("RGBA")
    profile = create_rounded_profile_photo(user_image)
    template.paste(profile, (75, 225), profile)

    draw = ImageDraw.Draw(template)

    font_title = ImageFont.truetype("arialbd.ttf", size=50)
    draw.text((355, 150), "STUDENT CARD", font=font_title, fill="black")

    font = ImageFont.truetype("arial.ttf", size=32)
    draw.text((400, 240), name, font=font, fill="black")
    draw.text((400, 290), id_n, font=font, fill="black")
    draw.text((400, 340), "2025-2026", font=font, fill="black")

    template = round_card_edges(template, corner_radius=40)
    return template


def delete_file_later(path, delay=10):
    def delayed_delete():
        time.sleep(delay)
        try:
            os.remove(path)
            print(f"[INFO] Deleted temporary file: {path}")
        except Exception as e:
            print(f"[ERROR] Could not delete file: {path}. Reason: {e}")
    threading.Thread(target=delayed_delete).start()



# def main():
#     in_name = "Ran Weissman"
#     in_id = "312236466"
#     in_profile_path = "self_photo.jpeg"  # TODO: PNG OR JPEG
#     in_template_path = "template.png"
#     in_output_path = "business_card_output.png"
#
#     create_card(in_name, in_id, in_profile_path, in_template_path, in_output_path)
#
#
# if __name__ == "__main__":
#     main()
