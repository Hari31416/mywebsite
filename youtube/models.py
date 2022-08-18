from django.db import models
import pytube
import os
import random
import string

# Create your models here.
class YoutubeAudio(models.Model):

    youtube_url = models.URLField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    files = None
    thumb_url = None
    details = {}
    download_url = None

    def _get_length(self, time):
        """takes a time in seconds and returns a string of the form mm:ss"""
        minutes = time // 60 % 60
        seconds = time % 60
        return f"{minutes}:{seconds}"

    def validate(self):
        """returns True if the url is valid, False otherwise"""
        error_text = ""
        error = True
        yt = None
        try:
            yt = pytube.YouTube(self.youtube_url)
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
            error_text = "The video is longer than half an hour. Are you sure this is a song? Please choose a shorter video."
            return error, error_text

        return error, error_text

    def get_details(self):
        """takes a url and returns details about the song/video"""

        yt = pytube.YouTube(self.youtube_url)
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

        duration = self._get_length(yt.length)
        thumbnail = yt.thumbnail_url
        watch_url = yt.watch_url

        self.details = {
            "title": title,
            "artist": artist,
            "album": album,
            "duration": duration,
            "thumbnail": thumbnail,
            "watch_url": watch_url,
            "is_song": is_song,
        }
        return self.details

    def get_audio_files(self):
        yt = pytube.YouTube(self.youtube_url)
        audio_details = []
        files = yt.streams.filter(only_audio=True).order_by("abr")
        for file in files:
            id = file.itag
            file_size = round(file.filesize_approx / (1024 ** 2), 1)
            quality = file.abr
            audio_details.append((id, file_size, quality))
        self.files = files
        return audio_details, files

    def download_audio(self, id):
        if not self.files:
            self.get_audio_files()

        file = self.files.get_by_itag(id)
        name = file.default_filename
        ran_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
        file_name = str(ran_str) + "_" + name
        file_path = os.path.join("media", "youtube")
        file.download(output_path=file_path, filename=file_name)
        original_file = os.path.join(file_path, file_name)

        for extension in [".mp4", ".mkv", ".avi", ".webm"]:
            if original_file.endswith(extension):
                print("Found file ending with: " + extension)
                new_file = original_file.replace(extension, ".mp3")
                os.rename(original_file, new_file)
                self.download_url = new_file
                return new_file
        print("NOT FOUND!")
        self.download_url = original_file
        return self.download_url
