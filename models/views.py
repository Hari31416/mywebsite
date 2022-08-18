from django.shortcuts import render
from .models import ImageFile

# Create your views here.


def index(request):
    return render(request, "models/index.html")


def food_vision(request):
    saved = False
    if request.method == "POST":
        img_file = request.FILES["img_file"]
        i = ImageFile(img_file=img_file)
        valid, error_message = i.validate()
        if valid:
            i.save()
            saved = True
            img_url = i.img_file.url
            img = i.preprocess_image()
            preds, classes = i.predict(5)

            results = list(
                map(
                    lambda x: (" ".join(x[0].split("_")).title(), round(x[1] * 100, 2)),
                    zip(classes, preds),
                )
            )
            print(results)
            return render(
                request,
                "models/food_vision.html",
                {
                    "img_url": img_url,
                    "saved": saved,
                    "image": img,
                    "results": results,
                },
            )
        else:
            return render(
                request,
                "models/food_vision.html",
                {"error_message": error_message, "saved": saved},
            )
    else:
        return render(request, "models/food_vision.html", {"saved": saved})
