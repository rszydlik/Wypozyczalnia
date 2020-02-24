from django import forms
from django.contrib.auth.models import User

from wypozyczalnia_app.models import Book, Friend, Library


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['btitle', 'bauthor', 'bdescription']


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['name', 'email', 'phone']


class LendForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ('borrower',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        userid = self.user.pk
        super(LendForm, self).__init__(*args, **kwargs)
        self.fields['borrower'].queryset = self.fields['borrower'].queryset.filter(relates=userid)


class Login(forms.Form):
    login_form = forms.CharField(label='Login', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class AddUserForm(forms.ModelForm):
    password_conf = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password_conf', 'first_name', 'last_name', 'email')
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean_password_conf(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password_conf")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Hasła się różnią',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="Podaj nowe hasło", widget=forms.PasswordInput, max_length=128)
    confirm_password = forms.CharField(label="Potwierdź hasło", widget=forms.PasswordInput, max_length=128)

    def clean_password_conf(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Hasła się różnią',
            )
        return password2
