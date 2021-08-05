from django import forms

from post.models import Post, Comment


class PostCreationForms(forms.ModelForm):
    picture = forms.ImageField()
    caption = forms.CharField()

    class Meta:
        model = Post
        fields = ['picture', 'caption']


class CommentCreationForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={'rows': 4, 'cols': 70}))

    class Meta:
        model = Comment
        fields = ['content']
