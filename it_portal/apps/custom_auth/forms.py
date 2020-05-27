from django import forms
from allauth.account.forms import LoginForm, perform_login, app_settings

class MyCustomLoginForm(LoginForm):

    error_messages = {
        'account_inactive':
        ("В настоящее время этот аккаунт неактивен."),

        'email_password_mismatch':
        ("Неверный e-mail или пароль."),

        'username_password_mismatch':
        ("Неверный логин или пароль."),
    }

    def login(self, request, redirect_url=None):
        ret = perform_login(request, self.user,
                            email_verification=app_settings.EMAIL_VERIFICATION,
                            redirect_url=redirect_url)
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)

        request.session['remember'] = remember

        return ret

class MyCustomSignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ('First name')}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ('Last name')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.save()
