from django.db.models.signals import post_save
from django_comments.abstracts import CommentAbstractModel
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

import asyncio
from ckeditor_uploader.fields import RichTextUploadingField

from utils.email_utils import send_comment_notification


class CustomComment(CommentAbstractModel):
    comment = RichTextUploadingField(blank=True, verbose_name="Content")


@receiver(post_save, sender=CustomComment)
def send_email_notification_about_comment(sender, instance, created, **kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(None, send_comment_notification, instance, created)
