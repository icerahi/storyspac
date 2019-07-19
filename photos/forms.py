from django import forms
from upload_validator import FileTypeValidator

from .models import Photo,Comment
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea

class PhotoModelForm(forms.ModelForm):
    caption=forms.CharField(widget=EmojiPickerTextInput)

    image = forms.ImageField(
        label='', help_text="JPEG,PNG,JPG will accepted", required=True,
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg', 'image/png', 'image/jpg']
        )],
    )



    class Meta:
        model=Photo
        fields=[
            'image',
            'caption'
        ]


class CommentModelForm(forms.ModelForm):
    comment=forms.CharField(label='',widget=forms.TextInput(
        attrs={
            'placeholder':'Comment',
            'class':'form-control',
        }
    ))
    class Meta:
        model=Comment
        fields=('comment',)