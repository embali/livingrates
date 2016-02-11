from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
import random
import string
from django.conf import settings
import sys


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=255, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Use for successful email confirmation.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    middle_name = models.CharField(_('middle name'), max_length=255,
                                   blank=True)
    confirmation = models.CharField(_('confirmation'), max_length=128,
                                    blank=True)
    is_banned = models.BooleanField(
        _('banned'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as banned. '
            'Select this instead of deleting accounts.'
        ),
    )
    expiration = models.DateTimeField(_('expiration'), default=timezone.now)
    new_email = models.EmailField(_('new email address'), blank=True)
    mailed = models.DateTimeField(_('mailed'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s %s' % (self.first_name, self.middle_name,
                                  self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        if settings.DEBUG:
            print(self.email, subject, message, '\n', file=sys.stderr)

        send_mail(subject, message, from_email, [self.email, ], **kwargs)

    def update_mailed(self):
        self.mailed = timezone.now() + timedelta(hours=2)

    def generate_confirmation(self):
        """
        Generate confirmation code and its expiration timestamp
        """
        self.confirmation = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(128))
        self.expiration = timezone.now() + timedelta(hours=24)

    def set_full_name(self, full_name):
        """
        Parse full name into first, middle and last
        """
        names = [name.strip() for name in full_name.strip().split()]
        if len(names) > 2:
            self.first_name = names[0]
            self.middle_name = ' '.join(names[1:-1])
            self.last_name = names[-1]
        elif len(names) == 2:
            self.first_name = names[0]
            self.middle_name = ''
            self.last_name = names[-1]
        elif len(names) == 1:
            self.first_name = names[0]
            self.middle_name = ''
            self.last_name = ''
        else:
            self.first_name = ''
            self.middle_name = ''
            self.last_name = ''

    def get_any_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.email.split('@')[0]
