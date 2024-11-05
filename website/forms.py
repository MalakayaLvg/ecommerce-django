from django import forms

from website.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content","rate"]

        label = {
            "content":"Saisissez votre commentaire"
        }
