from django import forms

from .models import Tweet


class TweetForm(forms.ModelForm):
    """
    ツイートフォーム
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tweet
        fields = {"content"}
        widgets = {
            "content": forms.Textarea,
            "description": forms.Textarea(attrs={"rows": 6, "cols": 15}),
        }
        labels = {"content": "内容"}
        error_messages = {
            "content": {"required": "入力が必須です．", "max_length": "文字数は，255文字以下です．"}
        }
