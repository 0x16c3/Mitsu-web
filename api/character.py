from entry import app, cache, client
from .utils import load_image, serve_image, throw_error, fonts
from PIL import Image, ImageFilter, ImageColor, ImageDraw

import urllib.request


@app.route("/character/<int:id>")
@cache.cached(timeout=86400)
def character(id: int):
    result = client.get_character(id)

    if not result:
        return throw_error(500)

    try:
        media = client.get(
            result.media[0]["id"], content_type=result.media[0]["type"].lower()
        )

        img_character = load_image(result.image.large, "RGBA")
        img_cover = load_image(media.banner, "RGBA")

    except urllib.error.HTTPError as e:
        return throw_error(e.code)
    except Exception as e:
        return throw_error(title="Unhandled exception", error=str(e), e=result)

    image = Image.new("RGBA", (1200, 628))

    ratio = 628 / img_cover.size[1]
    img_cover = img_cover.resize(
        (round(img_cover.size[0] * ratio), round(img_cover.size[1] * ratio)),
        resample=Image.ANTIALIAS,
    )
    img_cover = img_cover.filter(ImageFilter.GaussianBlur(15))
    img_cover = Image.alpha_composite(
        img_cover, Image.new("RGBA", img_cover.size, ImageColor.getrgb("#00000070"))
    )
    image.paste(img_cover, (392 - round(img_cover.size[0] / 2), 0))

    ratio = 473 / img_character.size[0]
    img_character = img_character.resize(
        (round(img_character.size[0] * ratio), round(img_character.size[1] * ratio)),
        resample=Image.ANTIALIAS,
    )

    img_size_2 = (image.size[0] * 2, image.size[1] * 2)
    mask = Image.new("L", img_size_2, 0)
    draw = ImageDraw.Draw(mask)
    poly_edge = (783, 727)
    draw.polygon(
        (
            (poly_edge[0] * 2, 0),
            (img_size_2[0], 0),
            img_size_2,
            (poly_edge[1] * 2, img_size_2[1]),
        ),
        fill=255,
    )
    mask = mask.resize(image.size, resample=Image.ANTIALIAS)
    black = Image.new(
        "RGBA",
        (image.size[0], image.size[1]),
        ImageColor.getrgb("#000000"),
    )
    black.paste(img_character, (image.size[0] - img_character.size[0], 0))
    image.paste(black, mask=mask)

    """
    ---
    """

    padding = round(image.size[1] / 2) - round(72 * 2 / 2 + 14)
    font = fonts["Bold-72"]
    font_reg = fonts["SemiBold-28"]

    draw = ImageDraw.Draw(image)

    image_blur = Image.new("RGBA", (1200, 628))
    draw_blur = ImageDraw.Draw(image_blur)

    draw_list = [draw_blur, draw]

    for c in draw_list:

        blur = c == draw_blur

        if hasattr(result.name, "first"):
            c.text(
                (60, padding),
                result.name.first,
                font=font,
                fill=ImageColor.getrgb("black") if blur else ImageColor.getrgb("white"),
            )
        if hasattr(result.name, "last"):
            c.text(
                (60, padding + 72),
                result.name.last,
                font=font,
                fill=ImageColor.getrgb("black") if blur else ImageColor.getrgb("white"),
            )

        c.text(
            (60, padding + 72 * 2 + 12),
            str(result.favorites) + " Favorites",
            font=font_reg,
            fill=ImageColor.getrgb("black") if blur else ImageColor.getrgb("#FFAEBC"),
        )

        if blur:
            image_blur = image_blur.filter(ImageFilter.GaussianBlur(10))
            image = Image.alpha_composite(image, image_blur)

            # reset draw obj after alpha composite
            draw_list[1] = ImageDraw.Draw(image)

    return serve_image(image)