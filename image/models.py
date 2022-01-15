from django.db import models
from PIL import Image
import os

# Create your models here.
class ImageFile(models.Model):
    img_file = models.ImageField(upload_to="images")
    img_date = models.DateTimeField(auto_now_add=True)
    formats = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        # "gif": "GIF",
        # "bmp": "BMP",
    }
    thumb_file = ""
    resized_file = ""
    reshape_file = ""

    def get_image_format(self):
        return self.formats[self.img_file.name.split(".")[-1]]

    def get_img_name(self):
        return self.img_file.name.split("/")[-1].split(".")[0]

    def change_path_format(self):
        """
        Changes the path format to be compatible with django
        """
        path = self.img_file.url.strip("/")
        path = path.replace("/", "\\")
        return path

    def validate(self):
        """
        Validates image for file size and file type
        """
        valid = True
        error_message = ""
        if self.img_file.size / (1024 * 1024) > 5:
            error_message += "File size should be less than 5 MB\n"
            valid = False
        if self.img_file.name.split(".")[-1] not in self.formats.keys():
            error_message += "File format should be one of the following: "
            for format in self.formats.keys():
                error_message += format + ", "
            error_message = error_message[:-2]
            valid = False
        return valid, error_message

    def __str__(self):
        return self.img_file.name

    def get_image_details(self):
        """
        Returns details about the image
        """
        img = Image.open(self.img_file)
        height = self.img_file.height
        width = self.img_file.width
        format = self.formats[self.img_file.name.split(".")[-1]]
        size = round(self.img_file.size / (1024), 2)
        try:
            dpi = img.info["dpi"][0]
        except KeyError:
            dpi = "Not available"
        return {
            "height": f"{height} pixels",
            "width": f"{width} pixels",
            "format": format,
            "size": f"{size} KB",
            "dpi": dpi,
        }

    def get_thumbnail(self, height=200):
        """
        Returns thumbnail of the image
        Keeps the aspect ratio unchanged
        """
        img = Image.open(self.img_file)
        ratio = self.img_file.width / self.img_file.height
        width = int(ratio * height)
        img = img.resize((width, height), Image.ANTIALIAS)
        thumb_dir = os.path.join("media", "images", "thumb")
        file_dir = os.path.join(thumb_dir, self.img_file.name.split("/")[1])
        img.save(file_dir)
        self.thumb_file = file_dir.replace("\\", "/")
        return self.thumb_file

    def reshape_image(self, w, h):
        img = Image.open(self.img_file)
        img = img.resize((w, h), Image.ANTIALIAS)
        reshaped_img = os.path.join("media", "images", "reshape")
        file_dir = os.path.join(reshaped_img, self.img_file.name.split("/")[1])
        img.save(file_dir)

        return file_dir.replace("\\", "/")

    def jpg_to_png(self):
        jpg = Image.open(self.img_file)
        img_name = self.get_img_name()
        converted_img = os.path.join("media", "images", "converted", img_name)
        file_path = f"{converted_img}.png"
        jpg.save(file_path, "PNG")
        return file_path.replace("\\", "/")

    def png_to_jpg(self):
        png = Image.open(self.img_file)
        png.load()
        img_name = self.get_img_name()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3])  # 3 is the alpha channel
        converted_img = os.path.join("media", "images", "converted", img_name)
        file_path = f"{converted_img}.jpg"
        background.save(file_path, "JPEG")
        return file_path.replace("\\", "/")

    def resize_png_image(self, size):
        img = self.png_to_jpg()
        print(f"IMAGE: {img}")
        return self.resize_jpg_image(size=size, file_path=img)

    def resize_jpg_image(self, size, file_path=None):
        """
        Resizes the image to the given size (Kb)
        """
        error = ""
        # Desired size of the image
        FINAL_SIZE = size
        # Original image directory
        if file_path is None:
            file = self.change_path_format()
            original_file = self.img_file.url
        else:
            file = file_path
            original_file = file

        # Resized image directory
        resized_img = os.path.join("media", "images", "resize")
        resize_image = os.path.join(resized_img, self.get_img_name())
        resize_image = f"{resize_image}.jpg"
        iter = 1
        print(f"{iter} iteration")

        # Original image size
        original_size = os.path.getsize(file) / 1024
        print(file)
        print(f"Original size: {original_size} KB")
        # Setting the image quality based on the ratio of the original image size
        # and the desired size
        fold = original_size / FINAL_SIZE
        quality = int(100 / fold)

        # Resizing the image
        o_img = Image.open(file)
        o_img.save(resize_image, quality=quality)
        print(resize_image)
        current_size = os.path.getsize(resize_image) / 1024
        print(f"{FINAL_SIZE} KB -> {current_size} KB")

        # Defining the prevoius size to be used in while loop
        previous_size = current_size

        # Starting the loop and keep running till the desired size is reached
        while current_size > FINAL_SIZE:
            iter += 1
            print(f"{iter} iteration")

            # reducing the quality of the image
            quality = quality - 2
            c_image = Image.open(resize_image)
            c_image.save(resize_image, quality=quality)
            current_size = os.path.getsize(resize_image) / 1024

            # Checking if the image size is decreasing or not
            difference = previous_size - current_size
            if difference < 1:
                error += "Image size is not decreasing. Because the quality of the image has reached very low.\n"
                print(f"{FINAL_SIZE} KB -> {current_size} KB")
                print("No more difference")
                break

            previous_size = current_size

            if current_size <= FINAL_SIZE:
                print(f"{FINAL_SIZE} KB -> {current_size} KB")
                print("Done!")
                break

            # making sure that the quality is at least 5
            if quality < 5:
                error += (
                    "Quality has reached very low value (less than 5%). Aborting!\n"
                )
                error += "You should consider reshaping the image first."
                print(f"{FINAL_SIZE} KB -> {current_size} KB")
                print("Aborting! Quality has reached very low value (less than 5%).")
                print("You should consider reshaping the image first.")
                break

            print(f"{FINAL_SIZE} KB -> {current_size} KB")
        return resize_image.replace("\\", "/"), error, round(current_size, 2)

    def resize_image(self, size, file_path=None):
        """
        Resizes the image to the given size (Kb)
        """
        if self.img_file.name.endswith(".png"):
            return self.resize_png_image(size)
        else:
            return self.resize_jpg_image(size, file_path=None)
