from django import forms

from articles.models import Article, Comment


class ArticleCreateForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control'
    }))

    comment_disable=forms.BooleanField(required=False,label="Disable Comment ",)
    class Meta:
        model=Article
        fields=('title','body','status','comment_disable',)


class ArticleEditForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control'
    }))

    class Meta:
        model=Article
        fields=('title','body','status','comment_disable',)


class CommentForm(forms.ModelForm):
    comment=forms.CharField(label="",widget=forms.Textarea(

        attrs=
        {"class":"form-control",
         "id":"comment",
         "placeholder":"Text going here!!!",
         "onfocus":"this.placeholder = ''",
         "onblue":"this.placeholder = 'Text going here!!!!'" ,
         "rows":"4",
         "cols":"50"
         }))

    class Meta:
        model=Comment
        fields=('comment',)