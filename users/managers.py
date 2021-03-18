from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def get_author_queryset(self):
        return super().get_queryset().filter(is_author=True)

    def _create_user(
            self, email, name, profile_picture=None, password=None,
            is_author=False, is_staff=False, is_active=True
    ):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.set_password(password)  # change password to hash
        user.profile_picture = profile_picture
        user.is_author = is_author
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, name, profile_picture=None, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.set_password(password)
        user.profile_picture = profile_picture
        user.admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
