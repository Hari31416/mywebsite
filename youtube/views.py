from django.shortcuts import render
from .models import YoutubeAudio

# Create your views here.
def index(request):
    link_provided = True
    if request.method == "POST":
        url = request.POST["url"]
        youtube_file = YoutubeAudio(youtube_url=url)
        error, error_text = youtube_file.validate()
        if error:
            return render(
                request,
                "youtube/index.html",
                {"error_text": error_text, "link_provided": link_provided},
            )
        else:
            youtube_file.save()
            pk = youtube_file.pk
            details = youtube_file.get_details()
            is_song = details.pop("is_song")
            thumb_url = details.pop("thumbnail")
            watch_url = details.pop("watch_url")
            audio_details, _ = youtube_file.get_audio_files()
            return render(
                request,
                "youtube/index.html",
                {
                    "details": details,
                    "link_provided": link_provided,
                    "is_song": is_song,
                    "thumb_url": thumb_url,
                    "watch_url": watch_url,
                    "audio_details": audio_details,
                    "pk": pk,
                },
            )
    else:
        link_provided = False
        return render(request, "youtube/index.html", {"link_provided": link_provided})


def download(request):
    if request.method == "POST":
        pk = request.POST["pk"]
        id = int(request.POST["id"])
        youtube_file = YoutubeAudio.objects.get(pk=pk)
        path = "/" + youtube_file.download_audio(id)
    return render(
        request,
        "youtube/download.html",
        {
            "id": id,
            "path": path,
        },
    )
