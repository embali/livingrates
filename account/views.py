from django.http import QueryDict, JsonResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
import random
import string

from .models import Account
from .forms import SignUpForm, SignInForm, ResetForm, UpdateForm


class Message(object):
    PASSWORDS_DONT_MATCH = 'Passwords do not match'
    CONFIRM_EMAIL = 'Please check and confirm your email'
    EMAIL_CONFIRMED = 'Email has been confirmed, sign in to proceed'
    UNABLE_CONFIRM_EMAIL = 'Unable to confirm email, try again later or ' \
                           'reset your password'
    INVALID_CREDENTIALS = 'Invalid credentials'
    EMAIL_NOT_CONFIRMED = 'User email is not confirmed'
    USER_UNAVAILABLE = 'User is not registered/active or banned'
    RESET_EMAIL = 'Check your email to reset password'
    RESET_EMAIL_SENT = 'Reset email have been already sent, if you won\'t ' \
                       'get it in next two hours, try again'
    PASSWORD_SENT = 'Temporary password has been sent to your email'
    RESET_UNABLE = 'Unable to reset password, try again later or contact ' \
                   'support'
    ACCOUNT_UPDATED = 'Account updated'
    EMAIL_UPDATED = 'Email successfully updated'
    UNABLE_UPDATE_EMAIL = 'Unable to update email'
    PASSWORD_CHANGED = 'Password has been changed successfully, please sign ' \
                       'in again'


class Status(object):
    AUTH = 'auth'
    DONE = 'done'
    VALIDATION = 'validation'
    PASSWORD = 'password'
    USER = 'user'
    UNAVAILABLE = 'unavailable'
    REDIRECT = 'redirect'


class SignUp(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        context = RequestContext(request, dict(
            signup_form=SignUpForm()))
        signup_modal = render_to_string(
            'account/partials/_signup_modal.html', context)

        return JsonResponse(dict(
            status=Status.DONE,
            signup_modal=signup_modal))

    def post(self, request):
        if request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        signup_form = SignUpForm(QueryDict(request.POST['signup_form']))

        if not signup_form.is_valid():
            context = RequestContext(request, dict(
                signup_form=signup_form))
            signup_modal = render_to_string(
                'account/partials/_signup_modal.html', context)

            return JsonResponse(dict(
                status=Status.VALIDATION,
                signup_modal=signup_modal))

        if signup_form.cleaned_data['password_'] != \
           signup_form.cleaned_data['confirmation']:
            context = RequestContext(request, dict(
                signup_form=signup_form,
                message=Message.PASSWORDS_DONT_MATCH))
            signup_modal = render_to_string(
                'account/partials/_signup_modal.html', context)

            return JsonResponse(dict(
                status=Status.PASSWORD,
                signup_modal=signup_modal))

        account = signup_form.save(commit=False)
        account.is_active = False
        account.set_full_name(signup_form.cleaned_data['full_name'])
        account.set_password(signup_form.cleaned_data['password_'])
        account.generate_confirmation()
        account.save()

        account.email_user(
            'LivingRates email confirmation',
            'Please follow this link to confirm your email:\n%s' %
            request.build_absolute_uri(reverse(
                'confirm_link', args=[account.email, account.confirmation, ])),
            settings.NOREPLY_EMAIL)

        context = RequestContext(request, dict(
            signup_form=signup_form,
            message=Message.CONFIRM_EMAIL))
        signup_modal = render_to_string(
            'account/partials/_signup_modal.html', context)

        return JsonResponse(dict(
            status=Status.DONE,
            signup_modal=signup_modal))


class Confirm(generic.View):
    def get(self, request, email, confirmation):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('web'))

        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return HttpResponseRedirect(reverse('confirm_fail'))

        if account.is_active or \
           account.confirmation != confirmation or \
           account.expiration < timezone.now():
            return HttpResponseRedirect(reverse('confirm_fail'))

        account.is_active = True
        account.save()

        return HttpResponseRedirect(reverse('confirm_success'))


class ConfirmStatus(generic.View):
    def get(self, request):
        if not request.user.is_authenticated():
            if request.path == reverse('confirm_success'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.EMAIL_CONFIRMED)))
            elif request.path == reverse('confirm_fail'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.UNABLE_CONFIRM_EMAIL)))

        return HttpResponseRedirect(reverse('web'))


class SignIn(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        context = RequestContext(request, dict(
            signin_form=SignInForm()))
        signin_modal = render_to_string('account/partials/_signin_modal.html',
                                        context)

        return JsonResponse(dict(
            status=Status.DONE,
            signin_modal=signin_modal))

    def post(self, request):
        if request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        signin_form = SignInForm(QueryDict(request.POST['signin_form']))

        if not signin_form.is_valid():
            context = RequestContext(request, dict(
                signin_form=signin_form))
            signin_modal = render_to_string(
                'account/partials/_signin_modal.html', context)

            return JsonResponse(dict(
                status=Status.VALIDATION,
                signin_modal=signin_modal))

        user = authenticate(email=signin_form.cleaned_data['email'],
                            password=signin_form.cleaned_data['password'])
        if user is None:
            context = RequestContext(request, dict(
                signin_form=signin_form,
                message=Message.INVALID_CREDENTIALS))
            signin_modal = render_to_string(
                'account/partials/_signin_modal.html', context)

            return JsonResponse(dict(
                status=Status.USER,
                signin_modal=signin_modal))
        elif not user.is_active:
            context = RequestContext(request, dict(
                signin_form=signin_form,
                message=Message.EMAIL_NOT_CONFIRMED))
            signin_modal = render_to_string(
                'account/partials/_signin_modal.html', context)

            return JsonResponse(dict(
                status=Status.USER,
                signin_modal=signin_modal))

        login(request, user)

        context = RequestContext(request, {})
        user_name = render_to_string('account/partials/_user_name.html',
                                     context)
        user_menu = render_to_string('account/partials/_user_menu.html',
                                     context)

        return JsonResponse(dict(
            status=Status.DONE,
            user_name=user_name,
            user_menu=user_menu))


class SignOut(generic.View):
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        context = RequestContext(request, {})
        signout_hidden = render_to_string(
            'account/partials/_signout_hidden.html', context)

        return JsonResponse(dict(
            status=Status.DONE,
            signout_hidden=signout_hidden))

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        logout(request)

        context = RequestContext(request, {})
        user_name = render_to_string('account/partials/_user_name.html',
                                     context)
        user_menu = render_to_string('account/partials/_user_menu.html',
                                     context)

        return JsonResponse(dict(
            status=Status.DONE,
            user_name=user_name,
            user_menu=user_menu))


class Reset(generic.View):
    def get(self, request, email=None, confirmation=None):
        if not email or not confirmation:
            if request.user.is_authenticated():
                return JsonResponse(dict(
                    status=Status.AUTH))

            context = RequestContext(request, dict(
                reset_form=ResetForm()))
            reset_modal = render_to_string(
                'account/partials/_reset_modal.html', context)

            return JsonResponse(dict(
                status=Status.DONE,
                reset_modal=reset_modal))
        else:
            if request.user.is_authenticated():
                HttpResponseRedirect(reverse('web'))

            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return HttpResponseRedirect(reverse('reset_fail'))

            if account.confirmation != confirmation or \
               account.expiration < timezone.now():
                return HttpResponseRedirect(reverse('reset_fail'))

            password = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(16))
            account.generate_confirmation()
            account.is_active = True
            account.set_password(password)
            account.save()

            account.email_user(
                'LivingRates temporary password',
                'Please use this temporary password to sign in: %s' % password,
                settings.NOREPLY_EMAIL)

            return HttpResponseRedirect(reverse('reset_success'))

    def post(self, request):
        def unavailable():
            context = RequestContext(request, dict(
                reset_form=reset_form,
                message=Message.USER_UNAVAILABLE))
            reset_modal = render_to_string(
                'account/partials/_reset_modal.html', context)

            return JsonResponse(dict(
                status=Status.UNAVAILABLE,
                reset_modal=reset_modal))

        if request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        reset_form = ResetForm(QueryDict(request.POST['reset_form']))

        if not reset_form.is_valid():
            context = RequestContext(request, dict(
                reset_form=reset_form))
            reset_modal = render_to_string(
                'account/partials/_reset_modal.html', context)

            return JsonResponse(dict(
                status=Status.VALIDATION,
                reset_modal=reset_modal))

        try:
            account = Account.objects.get(
                email=reset_form.cleaned_data['email'])
            if account.is_banned or account.is_staff or account.is_superuser:
                return unavailable()
        except Account.DoesNotExist:
            return unavailable()

        if account.mailed < timezone.now():
            account.generate_confirmation()
            account.update_mailed()
            account.save()

            account.email_user(
                'LivingRates password reset',
                'Please follow this link to reset your password:\n%s' %
                request.build_absolute_uri(reverse(
                    'reset_link',
                    args=[account.email, account.confirmation])),
                settings.NOREPLY_EMAIL)
            message = Message.RESET_EMAIL
        else:
            message = Message.RESET_EMAIL_SENT
        context = RequestContext(request, dict(
            reset_form=reset_form,
            message=message))
        reset_modal = render_to_string('account/partials/_reset_modal.html',
                                       context)

        return JsonResponse(dict(
            status=Status.DONE,
            reset_modal=reset_modal))


class ResetStatus(generic.View):
    def get(self, request):
        if not request.user.is_authenticated():
            if request.path == reverse('reset_success'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.PASSWORD_SENT)))
            elif request.path == reverse('reset_fail'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.RESET_UNABLE)))

        return HttpResponseRedirect(reverse('web'))


class Update(generic.View):
    def get(self, request, email=None, confirmation=None):
        if not email or not confirmation:
            if not request.user.is_authenticated():
                return JsonResponse(dict(
                    status=Status.AUTH))

            context = RequestContext(request, dict(
                update_form=UpdateForm(
                    initial={
                        'full_name': request.user.get_full_name(),
                        'email': request.user.email, })))
            update_modal = render_to_string(
                'account/partials/_update_modal.html', context)

            return JsonResponse(dict(
                status=Status.DONE,
                update_modal=update_modal))
        else:
            if not request.user.is_authenticated():
                HttpResponseRedirect(reverse('web'))

            account = request.user

            if account.new_email != email or \
               account.confirmation != confirmation or \
               account.expiration < timezone.now():
                return HttpResponseRedirect(reverse('update_fail'))

            account.generate_confirmation()
            account.email = account.new_email
            account.save()

            return HttpResponseRedirect(reverse('update_success'))

    def post(self, request):
        def unavailable():
            context = RequestContext(request, dict(
                update_form=update_form,
                message=Message.USER_UNAVAILABLE))
            update_modal = render_to_string(
                'account/partials/_update_modal.html', context)

            return JsonResponse(dict(
                status=Status.UNAVAILABLE,
                update_modal=update_modal))

        if not request.user.is_authenticated():
            return JsonResponse(dict(
                status=Status.AUTH))

        account = request.user
        old_email = account.email

        update_form = UpdateForm(QueryDict(request.POST['update_form']),
                                 instance=account)

        if not account.is_active or account.is_banned or account.is_staff or \
           account.is_superuser:
            return unavailable()

        if not update_form.is_valid():
            context = RequestContext(request, dict(
                update_form=update_form))
            update_modal = render_to_string(
                'account/partials/_update_modal.html', context)

            return JsonResponse(dict(
                status=Status.VALIDATION,
                update_modal=update_modal))

        check = account.check_password(update_form.cleaned_data['password_'])
        new = update_form.cleaned_data['new']
        confirmation = update_form.cleaned_data['confirmation']
        if not check or new != confirmation:
            context = RequestContext(request, dict(
                update_form=update_form,
                message=Message.PASSWORDS_DONT_MATCH))
            update_modal = render_to_string(
                'account/partials/_update_modal.html', context)

            return JsonResponse(dict(
                status=Status.PASSWORD,
                update_modal=update_modal))

        account = update_form.save(commit=False)
        account.set_full_name(update_form.cleaned_data['full_name'])
        account.email = old_email
        if old_email != update_form.cleaned_data['email']:
            account.new_email = update_form.cleaned_data['email']
            account.generate_confirmation()
            account.email_user(
                'LivingRates new email confirmation',
                'Please follow this link to confirm your new email:\n%s\n'
                'Note that you should be signed in while confirmation' %
                request.build_absolute_uri(reverse(
                    'update_link',
                    args=[account.new_email, account.confirmation, ])),
                settings.NOREPLY_EMAIL)
        account.save()

        if len(update_form.cleaned_data['new']):
            account.set_password(update_form.cleaned_data['new'])
            account.save()

            return JsonResponse(dict(
                status=Status.REDIRECT,
                url=reverse('update_password')))

        context = RequestContext(request, dict(
            update_form=update_form,
            message=Message.ACCOUNT_UPDATED))
        update_modal = render_to_string('account/partials/_update_modal.html',
                                        context)

        context = RequestContext(request, {})
        user_name = render_to_string('account/partials/_user_name.html',
                                     context)
        user_menu = render_to_string('account/partials/_user_menu.html',
                                     context)

        return JsonResponse(dict(
            status=Status.DONE,
            update_modal=update_modal,
            user_name=user_name,
            user_menu=user_menu))


class UpdateStatus(generic.View):
    def get(self, request):
        if request.user.is_authenticated():
            if request.path == reverse('update_success'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.EMAIL_UPDATED)))
            elif request.path == reverse('update_fail'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.UNABLE_UPDATE_EMAIL)))
        else:
            if request.path == reverse('update_password'):
                return render(request, "web/web.html", RequestContext(
                    request, dict(
                        status=Message.PASSWORD_CHANGED)))

        return HttpResponseRedirect(reverse('web'))
