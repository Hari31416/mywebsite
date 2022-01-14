from django import forms
from .models import ImageFile


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageFile
        fields = ("img_name", "img_file")
        widgets = {
            "img_file": forms.FileInput(
                attrs={
                    "class": "form-control-file",
                    "id": "img_file",
                    "name": "img_file",
                    "type": "file",
                    "accept": "image/*",
                }
            )
        }
