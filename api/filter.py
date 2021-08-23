from entry import app, cache, client
from .utils import load_image, serve_image, throw_error, fonts
from PIL import Image, ImageFilter, ImageColor, ImageDraw

import urllib.request


@app.route("/filter/<mode>/<id>")
@cache.cached(timeout=86400)
def adult(mode, id):
    if mode not in ["media", "cover", "banner"]:
        return throw_error(title="Unknown mode", error="Please specify either `media`, `cover` or `banner`")

    if mode in ["cover", "banner"]:

        if "ANIME" in id.upper():
            id = id.replace("ANIME-", "")
            id = int(id)
            type = "ANIME"
        elif "MANGA" in id.upper():
            id = id.replace("MANGA-", "")
            type = int(id)
            mode = "MANGA"
        else:
            return (
                "Unknown Resource.<br>"
                "Bad AniList media id<br>"
                "Expected `MANGA` or `ANIME`"
            )

        result = client.get(id, content_type=type.lower())
        url = getattr(result, mode)
        if mode == "cover":
            url = url.large

        try:
            img = load_image(url)
        except urllib.error.HTTPError as e:
            return throw_error(e.code)
        except Exception as e:
            return throw_error(title="Unhandled exception", error=str(e), e=result)

        return serve_image(img.filter(ImageFilter.GaussianBlur(5)))

    elif mode == "media":
        if not isinstance(id, int):
            if not id.isdecimal():
                return (
                    "Unknown Resource.<br>" "Bad AniList media id<br>" "Expected `int`"
                )

            id = int(id)

        try:
            img = load_image(f"https://img.anili.st/{mode}/{id}")
        except urllib.error.HTTPError as e:
            return throw_error(e.code)
        except Exception as e:
            return throw_error(title="Unhandled exception", error=str(e))

        img_blur = img.filter(ImageFilter.GaussianBlur(15))
        img_blur = Image.alpha_composite(
            img_blur, Image.new(img.mode, img.size, ImageColor.getrgb("#FFFFFF50"))
        )

        img_size_2 = (img.size[0] * 2, img.size[1] * 2)
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

        mask = mask.resize(img.size, resample=Image.ANTIALIAS)

        img.paste(img_blur, mask=mask)

        draw = ImageDraw.Draw(img)

        padding = 55
        label = "ADULT"

        font = fonts["Black-48"]
        size = font.getsize(label)

        draw.rounded_rectangle(
            (
                img.size[0] - padding - size[0] - 8,
                padding,
                img.size[0] - padding + 8,
                padding + 48 + 8,
            ),
            radius=7,
            fill=ImageColor.getrgb("#EC294B"),
        )
        draw.text((img.size[0] - padding - size[0], padding - 3), label, font=font)

        return serve_image(img)
