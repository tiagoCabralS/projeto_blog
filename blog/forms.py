from django import forms
from blog.models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title', 'text', 
        )
        
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2'
        )
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error('email', ValidationError('Já existe um usuário cadastrado com esse e-mail', code='invalid'))
        
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if not password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error('password', ValidationError(errors))
                
        return password1