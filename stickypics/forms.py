from django import forms
from upload_validator import FileTypeValidator

from stickypics.models import Stickypic, Comment


class StickypicModelForm(forms.ModelForm):

    image=forms.ImageField(
        label='',help_text="JPEG,PNG,JPG will accepted",required=False,
        validators=[FileTypeValidator(
            allowed_types=['image/jpeg','image/png','image/jpg']
        )]
    )
    description=forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control'
    }))
    source=forms.URLField(widget=forms.URLInput(attrs={
        'class':'form-control'
    }))
    class Meta:

        model=Stickypic
        fields=[
            'image',
            'description',
            'source',
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