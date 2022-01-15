from django.shortcuts import render
from .models import ImageFile
from django.utils import timezone


def index(request):
    saved = False
    if request.method == "POST":
        img_file = request.FILES["img_file"]
        i = ImageFile(img_file=img_file, img_date=timezone.now())
        valid, error_message = i.validate()

        if valid:
            saved = True
            i.save()
            img_url = i.img_file.url
            print(img_url)
            thumb_img = "/" + i.get_thumbnail(200)
            details = i.get_image_details()
            pk = i.pk
            format = i.get_image_format()
            return render(
                request,
                "image/index.html",
                {
                    "saved": saved,
                    "img_url": img_url,
                    "thumb_img": thumb_img,
                    "details": details,
                    "pk": pk,
                    "format": format,
                },
            )
        else:
            return render(
                request,
                "image/index.html",
                {"error_message": error_message, "saved": saved},
            )
    else:
        return render(request, "image/index.html", {"saved": saved})


def reshape(request):
    if request.method == "POST":
        print(request.POST)
        width = int(request.POST["w"])
        height = int(request.POST["h"])
        pk = int(request.POST["pk"])
        image = ImageFile.objects.get(pk=pk)
        file_dir = "/" + image.reshape_image(width, height)
        thumb_dir = "/" + image.get_thumbnail(200)
        return render(
            request,
            "image/reshape.html",
            {"file_dir": file_dir, "thumb_dir": thumb_dir},
        )
    else:
        return render(request, "image/index.html")


def resize(request):
    if request.method == "POST":
        print(request.POST)
        size = int(request.POST["size"])
        pk = int(request.POST["pk"])
        image = ImageFile.objects.get(pk=pk)
        file_dir, err_text, reached_size = image.resize_image(size)
        if err_text == "":
            error = False
        else:
            error = True
        err_text = err_text.split("\n")
        file_dir = "/" + file_dir
        thumb_dir = "/" + image.get_thumbnail(200)
        return render(
            request,
            "image/resize.html",
            {
                "file_dir": file_dir,
                "thumb_dir": thumb_dir,
                "error": error,
                "err_text": err_text,
                "reached_size": reached_size,
            },
        )
    else:
        return render(request, "image/index.html")


def reformat(request):
    if request.method == "POST":
        pk = int(request.POST["pk"])
        image = ImageFile.objects.get(pk=pk)
        format = image.get_image_format()
        if format == "PNG":
            file_dir = "/" + image.png_to_jpg()
            converted_format = "JPG"
        else:
            file_dir = "/" + image.jpg_to_png()
            converted_format = "PNG"
        return render(
            request,
            "image/reformat.html",
            {"file_dir": file_dir, "converted_format": converted_format},
        )
    else:
        return render(request, "image/index.html")
