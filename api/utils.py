import os
from entry import dirname, cache
from flask import Response, jsonify

from PIL import Image, ImageFont, ImageDraw, ImageColor

# for serve_image
import io
import urllib.request
from werkzeug.wsgi import FileWrapper


fonts = {
    "Black-48": ImageFont.truetype(
        os.path.join(dirname, "fonts/Overpass-Black.ttf"), size=48
    ),
    "Bold-72": ImageFont.truetype(
        os.path.join(dirname, "fonts/Overpass-Bold.ttf"), size=72
    ),
    "SemiBold-64": ImageFont.truetype(
        os.path.join(dirname, "fonts/Overpass-SemiBold.ttf"), size=64
    ),
    "SemiBold-28": ImageFont.truetype(
        os.path.join(dirname, "fonts/Overpass-SemiBold.ttf"), size=28
    ),
    "Consolas-12": ImageFont.truetype(
        os.path.join(dirname, "fonts/Consolas.ttf"), size=12
    ),
}


def load_image(url: str, convert: str = None) -> Image:
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        },
    )
    path = io.BytesIO(urllib.request.urlopen(req).read())

    image = Image.open(path)

    if convert:
        return image.convert(convert)

    return image


def serve_image(pil_img: Image) -> Response:

    # stream image
    img_io = io.BytesIO()
    pil_img.save(img_io, "PNG", quality=70)
    img_io.seek(0)

    # use werkzeug filewrapper because
    # wsgi is not compatible with caching
    file_wrapper = FileWrapper(img_io)
    return Response(
        file_wrapper,
        mimetype="image/png",
        direct_passthrough=True,
    )


@cache.cached(timeout=86400, key_prefix="error_image")
def generate_error(
    title: str = "An error occured.",
    error: str = "An unknown error occured.",
    code: str = None,
) -> Image:

    mitsu = Image.open(os.path.join(dirname, "static/mitsu.png"))
    mitsu = mitsu.resize((628, 628), resample=Image.ANTIALIAS)

    image = Image.new(mitsu.mode, (1200, 628), ImageColor.getrgb("#5191F5"))
    image.paste(mitsu, (1200 - 628, 0))

    font = fonts["Bold-72"]
    font_sub = fonts["SemiBold-64"]
    font_con = fonts["Consolas-12"]

    padding = 65

    draw = ImageDraw.Draw(image)

    text_size_code = font_con.getsize(f"Code: {code}")
    draw.text((padding, 628 / 2 - 72), title, font=font)
    draw.text((padding, 628 / 2), error, font=font_sub)

    if code:
        draw.rounded_rectangle(
            (
                padding - 8,
                628 - text_size_code[1] - padding - 12,
                padding + text_size_code[0] + 8,
                628 - padding,
            ),
            radius=7,
            fill=ImageColor.getrgb("#FFFFFF"),
        )
        draw.text(
            (padding, 628 - text_size_code[1] - padding - 5),
            f"Code: {code}",
            font=font_con,
            fill=ImageColor.getrgb("#000000"),
        )

    return image


def throw_error(
    e=None, image=False, title="Unknown resource", error="Bad AniList id"
) -> Response:

    if not image:
        return jsonify({"error": {"title": title, "description": error, "code": e}})

    return serve_image(
        generate_error(
            title=title,
            error=error,
            code=e,
        )
    )