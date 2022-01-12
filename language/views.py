from django.shortcuts import render
from django.http import HttpResponse
from language.models import Text

# Create your views here.


def index(request):
    no_text = False
    text = ""
    try:
        text = request.POST["text"]
    except:
        no_text = True

    if text == "":
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
        language = t.get_language()
        languages = t.get_all_languages()
        error = False
        my_dict = {
            "language": language,
            "text": text,
            "languages": languages,
            "error": error,
        }
        return render(request, "language/index.html", my_dict)


def help(request):
    my_dict = {"insert_me": "Hello! What can I do for you?"}
    return render(request, "language/help.html", my_dict)
