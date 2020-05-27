from django import forms
from .models import ProfileSubscriber

class subscribeForm(forms.Form):
	def save(self, request, author):
		if ProfileSubscriber.objects.filter(user=request.user, author=author).count() == 0:
			Sub = ProfileSubscriber.objects.create(user=request.user, author=author)
			Sub.save()

	def delete(self, requst, author):
		Sub = ProfileSubscriber.objects.get(user=requst.user, author=author)
		Sub.delete()