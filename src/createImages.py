from PIL import Image, ImageDraw, ImageFont
import textwrap

class CreateImages:
    def __init__(self, basePath, banner, title, username, description, vidNum, minutes):
        self.basePath = basePath
        self.banner = Image.open(str(banner))
        self.banner = self.banner.resize((2000, 332))
        self.title = title
        self.username = username
        self.description = textwrap.shorten(description, width=50, placeholder="...")
        self.vidNum = vidNum
        self.minutes = minutes

    def createBackground(self):
        # Create a new image with RGB mode
        image = Image.new("RGB", (2000, 1125), "white")
        image.paste(self.banner, (0, 0))

        # Draw a red rectangle on the image
        draw = ImageDraw.Draw(image)

        # Gradient rectangle dimensions
        x1, y1 = 675, 800
        width, height = 450, 200

        # Create gradient
        gradient = Image.new("RGB", (width, height))
        pixels = gradient.load()

        top = (50, 50, 50)
        bottom = (0, 0, 0)

        for y in range(height):
            t = y / (height - 1)

            r = int(top[0] * (1 - t) + bottom[0] * t)
            g = int(top[1] * (1 - t) + bottom[1] * t)
            b = int(top[2] * (1 - t) + bottom[2] * t)

            for x in range(width):
                pixels[x, y] = (r, g, b)

        # Create rounded mask
        mask = Image.new("L", (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)

        mask_draw.rounded_rectangle(
            [(0, 0), (width, height)],
            fill=255,
            radius=100
        )

        # Paste gradient onto your main image
        image.paste(gradient, (x1, y1), mask)
        image.paste(gradient, (x1+550, y1), mask)

        font = ImageFont.truetype("C:\\Users\\Lenovo\\Videos\\toDVD\\DvdWriter\\Roboto\\Roboto-SemiBold.ttf", 150)
        draw.text((625, 350), self.title, fill='#000000', font=font)

        font = ImageFont.truetype("C:\\Users\\Lenovo\\Videos\\toDVD\\DvdWriter\\Roboto\\Roboto-Regular.ttf", 63)
        draw.text((625, 550), f"{self.username}", fill='#000000', font=font)
        draw.text((625+(draw.textsize(f"{self.username}", font=font)), 550), f" • {self.vidNum} videos • {self.minutes} minutes", fill='#444444', font=font)
        draw.text((625, 650), self.description, fill="#444444", font=font)

        # Save the image
        bckgndPath = (self.basePath / "HomePage" / "Background.jpg")
        bckgndPath.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(bckgndPath))

    def createChapterBackground(self):
        image = Image.new("RGB", (2000, 1125), "white")

        image.paste(self.banner, (0, 0))
        bckgndPath = (self.basePath / "HomePage" / "ChapterBackground.jpg")
        bckgndPath.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(bckgndPath))


# draw.rectangle([(0, 0), (2000, 332)], fill="black")
# draw.ellipse([(50, 400), (550, 900)], fill="black")