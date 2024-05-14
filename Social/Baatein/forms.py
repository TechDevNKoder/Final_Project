from django import forms
from .models import Talk, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TalkForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Enter Your Thoughts!",
            "class": "form-control",
            "rows": 4,
        }
    ),
        label="",
    )

    class Meta:
        model = Talk
        fields = ['body', 'image']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        error_messages={'required': 'Enter a valid Email'})  # Customize or remove the message
    Name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}),
        error_messages={'required': 'Enter Your Name'})  # Customize or remove the message

    class Meta:
        model = User
        fields = ('username', 'Name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['username'].error_messages = {
            'required': 'Enter Your Username'}

        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password cant be too similar to your other 					    personal information. < /li > <li > Your password must contain at least 8 characters. < /li > <li > Your password cant be a commonly used password.</li><li>Your password cant be entirely numeric. < /li > </ul >'
        self.fields['password1'].error_messages = {
            'required': 'Enter your password'}

        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        self.fields['password2'].error_messages = {
            'required': 'Confirm Your Password'}

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if username and password1 and not password2:
            msg = "This field is required when username and password are provided."
            self.add_error('password2', msg)

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        error_messages={'required': 'Enter a valid Email'}
    )

    name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}),
        error_messages={'required': 'Enter Your Name'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'name')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'User Name'})
        self.fields['username'].label = ''
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['readonly'] = True

        self.fields['email'].required = True
        self.fields['name'].initial = self.instance.first_name
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Name'})
        self.fields['name'].label = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(
            email=email).exclude(pk=self.instance.pk).first()
        if existing_user:
            raise forms.ValidationError(
                "This email is already in use by another account.")
        return email

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name']
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }
