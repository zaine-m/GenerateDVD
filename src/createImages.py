from PIL import Image, ImageDraw, ImageFont
import textwrap

class CreateImages:
    def __init__(self, basePath, banner, title, username, description, vidNum, minutes):
        self.basePath = basePath
        self.banner = Image.open(str(banner))
        self.banner = self.banner.resize((720, 120))
        self.title = title
        self.username = username
        self.description = textwrap.shorten(description, width=50, placeholder="...")
        self.vidNum = vidNum
        self.minutes = minutes

    def createBackground(self):
        # Create a new image with RGB mode
        image = Image.new("RGB", (720, 405), "white")
        # image = Image.new("RGB", (2000, 1125), "white")
        image.paste(self.banner, (0, 0))

        # Draw a red rectangle on the image
        draw = ImageDraw.Draw(image)

        width, height = 162, 72
        gradient = Image.new("RGB", (width, height))
        pixels = gradient.load()

        topColour = (50, 50, 50)
        bottomColour = (0, 0, 0)

        for y in range(height):
            t = y / (height - 1)

            r = int(topColour[0] * (1 - t) + bottomColour[0] * t)
            g = int(topColour[1] * (1 - t) + bottomColour[1] * t)
            b = int(topColour[2] * (1 - t) + bottomColour[2] * t)

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
        image.paste(gradient, (222, 288), mask)
        image.paste(gradient, (428, 288), mask)

        font = ImageFont.truetype("Roboto\\Roboto-SemiBold.ttf", 54)
        draw.text((225, 126), self.title, fill='#000000', font=font)

        font = ImageFont.truetype("Roboto\\Roboto-Regular.ttf", 23)
        draw.text((225, 198), f"{self.username}", fill='#000000', font=font)
        draw.text((225+(draw.textlength(f"{self.username}", font=font)), 198), f" • {self.vidNum} videos • {self.minutes} minutes", fill='#444444', font=font)
        draw.text((225, 234), self.description, fill="#444444", font=font)

        # Save the image
        bckgndPath = (self.basePath / "HomePage" / "Background.jpg")
        bckgndPath.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(bckgndPath))

    def createChapterBackground(self):
        image = Image.new("RGB", (720, 405), "white")

        image.paste(self.banner, (0, 0))
        bckgndPath = (self.basePath / "HomePage" / "ChapterBackground.jpg")
        bckgndPath.parent.mkdir(parents=True, exist_ok=True)
        image.save(str(bckgndPath))


# draw.rectangle([(0, 0), (2000, 332)], fill="black")
# draw.ellipse([(50, 400), (550, 900)], fill="black")