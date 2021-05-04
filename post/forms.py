from django import forms

from post.models import Post, Comment


class PostCreationForms(forms.ModelForm):
    picture = forms.ImageField()
    caption = forms.CharField()

    class Meta:
        model = Post
        fields = ['picture', 'caption']


class CommentCreationForm(forms.ModelForm):
    content = forms.Textarea()

    class Meta:
        model = Comment
        fields = ['content']
