from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    '''
    Manager for user model
    '''
    def _create_user(self, email, password, **extra_fields):
        '''
        Create and save a user with the given email, and password.
        '''
        if not email:
            raise ValueError(ValidationErrors.MissingFields.missingEmail)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                ValidationErrors.SuperUserPermissions.superuserIsNotStaff)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                ValidationErrors.SuperUserPermissions.superuserIsNotSuperuser)

        return self._create_user(email, password, **extra_fields)

    def getByUser(self, user, throw=False):
        return None

    def getSearchUser(self, q=None):
        if q:
            resultset = self.filter(
                Q(email__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        else:
            return None

        return resultset

    def search(self, user, q=None, office_id=None, all=False):
        if q:
            resultset = self.getSearchUser(q=q)

            if office_id:
                if user.isOfficeOrAccountAdmin(office_id):
                    if not all:
                        resultset = resultset.exclude(id__in=OfficeUser.objects.filter(
                            office__id=office_id).values_list('user__id', flat=True))
                else:
                    return None
        else:
            return self.all()

        return resultset


class BlogManager(models.Manager):
    '''
    '''
    pass


class CommentManager(models.Manager):
    '''
    '''
    pass


class LikeManager(models.Manager):
    '''
    '''
    pass
