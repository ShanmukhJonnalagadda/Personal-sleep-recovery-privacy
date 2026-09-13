"""Generate the LinkedIn-ready system architecture PNG using Pillow."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "system-architecture.png"
WIDTH, HEIGHT = 1080, 1350


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for candidate in [name, f"/usr/share/fonts/truetype/dejavu/{name}",
                      "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
                      "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def rounded_box(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str = "#2c4259") -> None:
    draw.rounded_rectangle(xy, radius=24, fill=fill, outline=outline, width=2)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = "#66f2cb") -> None:
    draw.line([start, end], fill=color, width=5)
    x, y = end
    if end[1] >= start[1]:
        points = [(x, y), (x - 10, y - 16), (x + 10, y - 16)]
    else:
        points = [(x, y), (x - 10, y + 16), (x + 10, y + 16)]
    draw.polygon(points, fill=color)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#081423")
    draw = ImageDraw.Draw(image)

    draw.text((72, 68), "SYSTEM ARCHITECTURE", fill="#66f2cb", font=font(22, True))
    draw.text((72, 112), "Personal Sleep & Recovery", fill="#ffffff", font=font(44, True))
    draw.text((72, 166), "Analytics Dashboard", fill="#ffffff", font=font(44, True))
    draw.text((72, 225), "Automated wearable-data pipeline from acquisition to secure visualization", fill="#a9b7c8", font=font(20))

    boxes = [
        (292, 410, "WHOOP API", "Sleep • Recovery • Strain • HRV • RHR • Workouts", "#15263a", "01"),
        (500, 646, "Python Data Pipeline", "Retrieve • Clean • Transform • Convert time zones", "#15263a", "02"),
        (748, 894, "Supabase / PostgreSQL", "Persistent physiological records and user preferences", "#15263a", "03"),
        (996, 1152, "Streamlit Analytics Dashboard", "Interactive trends, filters and personalized insights", "#00c891", "04"),
    ]

    for top, bottom, title, subtitle, fill, number in boxes:
        rounded_box(draw, (170, top, 910, bottom), fill, "#2c4259" if fill != "#00c891" else "#66f2cb")
        cy = (top + bottom) // 2
        draw.ellipse((205, cy - 36, 277, cy + 36), fill="#0b2030" if fill != "#00c891" else "#063e31")
        draw.text((241, cy), number, anchor="mm", fill="#66f2cb", font=font(22, True))
        title_color = "#ffffff" if fill != "#00c891" else "#06251d"
        sub_color = "#a9b7c8" if fill != "#00c891" else "#0b3d31"
        draw.text((315, top + 38), title, fill=title_color, font=font(29, True))
        draw.text((315, top + 83), subtitle, fill=sub_color, font=font(17))

    arrow(draw, (540, 410), (540, 490))
    arrow(draw, (540, 646), (540, 724))
    arrow(draw, (540, 894), (540, 972))

    rounded_box(draw, (730, 418, 1010, 493), "#0d1b2b", "#4d6b88")
    draw.text((753, 434), "GitHub Actions", fill="#ffffff", font=font(18, True))
    draw.text((753, 464), "Scheduled every 6 hours", fill="#a9b7c8", font=font(15))
    draw.line([(730, 480), (650, 520)], fill="#66f2cb", width=3)
    draw.polygon([(650, 520), (660, 505), (667, 518)], fill="#66f2cb")
    rounded_box(draw, (72, 423, 390, 485), "#0d1b2b", "#4d6b88")
    draw.text((90, 442), "Journal export / CSV import", fill="#a9b7c8", font=font(17))
    arrow(draw, (320, 485), (320, 498))

    rounded_box(draw, (289, 1193, 791, 1265), "#15263a", "#4d6b88")
    draw.text((540, 1212), "Google OAuth • Authorized users only", anchor="ma", fill="#ffffff", font=font(18, True))
    draw.text((540, 1241), "Controlled access to the deployed dashboard", anchor="ma", fill="#a9b7c8", font=font(15))
    arrow(draw, (540, 1193), (540, 1158), "#8ab8ff")

    draw.text((540, 1312), "API INTEGRATION  •  CLOUD STORAGE  •  AUTOMATION  •  VISUALIZATION", anchor="mm", fill="#73859a", font=font(15))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, optimize=True)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
