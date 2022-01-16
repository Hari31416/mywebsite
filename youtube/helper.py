import pytube
import os


def validate(url):
    """returns True if the url is valid, False otherwise"""
    error_text = ""
    error = True
    yt = None
    try:
        yt = pytube.YouTube(url)
        error = False
    except pytube.exceptions.RegexMatchError:
        error_text = "Invalid Youtube URL"
        return error, error_text
    except pytube.exceptions.VideoUnavailable:
        error_text = "Video Unavailable"
        return error, error_text

    length = yt.length
    if length > 60 * 30:
        error = True
        error_text = (
            "The video is longer than half an hour. Are you sure this is a song? :)"
        )
        return error, error_text

    return error, error_text


def get_length(time):
    """takes a time in seconds and returns a string of the form mm:ss"""
    minutes = time // 60 % 60
    seconds = time % 60
    return f"{minutes}:{seconds}"


def get_details(url):
    """takes a url and returns details about the song/video"""

    yt = pytube.YouTube(url)
    details = yt.metadata.metadata
    is_song = False
    if details:
        details = details[0]
        if "Song" in details.keys():
            is_song = True

        try:
            title = details["Song"]
        except KeyError:
            title = yt.title

        try:
            artist = details["Artist"]
        except KeyError:
            artist = yt.author

        try:
            album = details["Album"]
        except KeyError:
            album = "Unknown"
    else:
        title = yt.title
        artist = yt.author
        album = "Unknown"

    duration = get_length(yt.length)
    thumbnail = yt.thumbnail_url
    watch_url = yt.watch_url

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "duration": duration,
        "thumbnail": thumbnail,
        "watch_url": watch_url,
        "is_song": is_song,
    }


def get_audio_files(url):
    yt = pytube.YouTube(url)
    audio_details = []
    files = yt.streams.filter(only_audio=True).order_by("abr")
    for file in files:
        id = file.itag
        file_size = round(file.filesize_approx / (1024 ** 2), 1)
        quality = file.abr
        audio_details.append((id, file_size, quality))
    return audio_details, files


def download_audio(files, id):
    file = files.get_by_itag(id)
    name = file.default_filename
    file_path = os.path.join("media", "youtube")
    file.download(file_path)
    file_to_open = os.path.join(file_path, name)

    if file_to_open.endswith(".mp4"):
        try:
            os.rename(file_to_open, file_to_open.replace(".mp4", ".mp3"))
        except FileExistsError:
            pass
        return file_to_open.replace(".mp4", ".mp3")

    elif file_to_open.endswith(".webm"):
        try:
            os.rename(file_to_open, file_to_open.replace(".webm", ".mp3"))
        except FileExistsError:
            pass
        return file_to_open.replace(".webm", ".mp3")
    else:
        return file_to_open
