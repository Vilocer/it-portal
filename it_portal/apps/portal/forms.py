from django import forms
from .models import ArticleLike, Comment
from apps.user.models import ProfileSubscriber

class LikeForm(forms.Form):
	class Meta:
		model = ArticleLike
		fields = {}

class commentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = { 'content', 'image' }
