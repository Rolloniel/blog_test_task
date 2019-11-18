from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group, AbstractUser, Permission, ContentType
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


import lxml.html



DEFAULT_USER_PERMISSIONS = ["add_emailconfirmation", "view_emailconfirmation", "add_socialaccount",
                            "change_socialaccount", "view_socialaccount", "add_post", "change_post", "delete_post",
                            "view_post"]


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of birth")


class Post(models.Model):

    STATE_CHOICES = [
        ('NP', 'Not published'),
        ('P', 'Published')
    ]

    title = models.CharField("Title", max_length=90, default='')

    author = models.ForeignKey("User", related_name="posts", verbose_name="Author", on_delete=models.CASCADE, default=1)

    content_html = RichTextUploadingField(blank=True, verbose_name="Content")

    created = models.DateTimeField("Created", default=timezone.now,
                                   editable=False)  # when first revision was created
    updated = models.DateTimeField("Updated", null=True, blank=True,
                                   editable=False)  # when last revision was created (even if not published)
    published = models.DateTimeField("Published", null=True, blank=True)  # when last published

    state = models.CharField("State", max_length=90, choices=STATE_CHOICES, default=STATE_CHOICES[0][0])

    view_count = models.IntegerField("View count", default=0, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    @property
    def is_published(self):
        return self.state == 'P'

    @property
    def is_future_published(self):
        return self.is_published and self.published is not None and self.published > timezone.now()

    @property
    def teaser_text(self):
        text = lxml.html.fromstring(self.content_html).text_content()
        if len(text) < 400:
            return text
        else:
            return text[:400]

    def save(self, **kwargs):
        self.updated_at = timezone.now()

        if self.is_published and self.published is None:
            self.published = timezone.now()

        self.full_clean()
        super(Post, self).save(**kwargs)

    class Meta:
        permissions = [('no_moderation_required', 'Can post without premoderation')]

        ordering = ("-published",)
        get_latest_by = "published"
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def inc_views(self):
        self.view_count += 1
        self.save()


# class PostComment(models.Model):
#     post = models.ForeignKey('Post', verbose_name="Post", on_delete=models.CASCADE, default=1)
#
#     comment_html = models.CharField(max_length=500, verbose_name="Comment HTML")
#
#     author = models.ForeignKey("User", verbose_name="Author", on_delete=models.CASCADE, default=1)
#
#     created = models.DateTimeField("Created", default=timezone.now,
#                                    editable=False)
#     updated = models.DateTimeField("Updated", null=True, blank=True,
#                                    editable=False)
#
#     def __str__(self):
#         return "{} by {}".format(self.created.date(), self.author.username)
#
#     class Meta:
#         verbose_name = "Comment"
#         verbose_name_plural = "Comments"



@receiver(post_save, sender=User)
def set_default_user_group(sender, instance, created, **kwargs):
    """ Adds a fresh registered user to "user" group, creates this group if needed """
    if created:
        instance.groups.add(Group.objects.get_or_create(name='user')[0])
        instance.save()


@receiver(post_save, sender=Group)
def set_default_group_permissions(sender, instance, created, **kwargs):
    """ Adds list of default permissions to created group """
    if created:
        for permission in DEFAULT_USER_PERMISSIONS:
            print("PING!", instance)
            instance.permissions.add(Permission.objects.get(codename=permission))
