from django.shortcuts import render
from django.http import HttpResponse
from language.models import Text

# Create your views here.


def index(request):
    no_text = False
    text = ""
    error = False
    try:
        text = request.POST["text"]
    except:
        no_text = True

    if text.strip() == "":
        no_text = True

    if no_text:
        text = "Please enter some text."
        language = "No text entered yet!"
        languages = "No text entered yet!"
        error = True
        my_dict = {
            "language": language,
            "text": text,
            "languages": languages,
            "error": error,
        }
        return render(request, "language/index.html", my_dict)
    else:
        t = Text(text=text)

        try:
            languages = t.get_all_languages()
            language = languages[0][0]
        except IndexError:
            language = "No language found!"
            languages = [("No language found!", 100)]

        my_dict = {
            "language": language,
            "text": text,
            "languages": languages,
            "error": error,
        }
        return render(request, "language/index.html", my_dict)
