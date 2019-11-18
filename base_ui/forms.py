from django import forms
from django.contrib.flatpages.models import FlatPage
from .models import Post
from allauth.account.forms import SignupForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    date_of_birth = forms.DateField(required=False, label = "Date of birth (mm/dd/yyyy)")

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_date = self.cleaned_data['date_of_birth']
        user.save()
        return user


class PostForm(forms.ModelForm):
    content_html = forms.CharField(widget=CKEditorUploadingWidget(), label="Content")
    class Meta:
        model = Post
        fields = ('title', 'content_html')




# class PostCommentCustomForm()