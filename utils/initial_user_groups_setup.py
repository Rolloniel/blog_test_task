from django.contrib.auth.models import Group, Permission

DEFAULT_PERMISSIONS = {
    "admin": [[permission.codename for permission in Permission.objects.all()]], # All permissions for the admin
    "editor": ["no_moderation_required"]
}


if __name__ == "__main__":

    for group, permissions in DEFAULT_PERMISSIONS.items():
        group_object = Group.objects.get_or_create(name=group)[0]

        for permission in permissions:
            group_object.permissions.add(Permission.objects.get(codename=permission))