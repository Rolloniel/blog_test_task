from django.core.mail import send_mail
from django.conf import settings


def send_comment_notification(instance, created):
    if created:
        comment = instance
        post_title = comment.content_object.title
        post_author = comment.content_object.author
        site_name = comment.site.name
        email_to = [post_author.email]
        email_from = settings.DEFAULT_FROM_EMAIL
        email_subject = "Your post was commented by another user!"
        email_message = "Hello from {site_name}!\n\nYou're receiving this e-mail because user" \
                        " {comment_user} has commented your post {post_title}.\n\nRegards,\n {site_name} administration".format(
            site_name=site_name,
            comment_user=comment.user.username,
            post_title=post_title)
        send_mail(email_subject, email_message, email_from, email_to, fail_silently=False)