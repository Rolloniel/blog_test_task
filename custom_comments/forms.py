from django import forms
from django_comments.forms import CommentForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import CustomComment


class CustomCommentForm(CommentForm):
    comment = forms.CharField(widget=CKEditorUploadingWidget(), label="Comment")

    def get_comment_create_data(self, site_id):
        # Use the data of the superclass, and add in the title field
        data = super().get_comment_create_data()
        data['comment'] = self.cleaned_data['comment']
        return data

    # class Meta:
    #     model = CustomCommentField
    #     fields = ('comment')