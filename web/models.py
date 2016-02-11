from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from account.models import Account


class Address(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    address = models.TextField(_('address'), unique=True, db_index=True)
    latitude = models.FloatField(_('latitude'), null=True, db_index=True)
    longitude = models.FloatField(_('longitude'), null=True, db_index=True)

    class Meta:
        verbose_name_plural = _('addresses')

    def __str__(self):
        return self.address


class Rate(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=False)
    account = models.ForeignKey(Account)
    address = models.ForeignKey(Address)
    apartment = models.CharField(_('apartment'), max_length=32, blank=True)
    title = models.CharField(_('title'), max_length=255, blank=True)
    text = models.TextField(_('text'), blank=True)

    def __str__(self):
        return "%s - %s" % (self.account, self.address)


class Photo(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=False)
    rate = models.ForeignKey(Rate)
    image = models.ImageField(_('image'), max_length=255)

    def __str__(self):
        return self.rate


class Category(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Variety(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    category = models.ForeignKey(Category)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name_plural = _('varieties')

    def __str__(self):
        return self.name


class Grade(models.Model):
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=False)
    rate = models.ForeignKey(Rate)
    variety = models.ForeignKey(Variety)
    value = models.FloatField(_('value'), null=True)

    def __str__(self):
        return self.rate
