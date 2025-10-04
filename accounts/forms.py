from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Tenant

User = get_user_model()


class UserLoginForm(forms.Form):
    """User login form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.role = self.cleaned_data['role']
        
        if commit:
            user.save()
        return user


class TenantRegistrationForm(forms.ModelForm):
    """Tenant registration form for organizers"""
    organizer_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter organizer email'
        })
    )
    organizer_first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter organizer first name'
        })
    )
    organizer_last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter organizer last name'
        })
    )
    organizer_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter organizer password'
        })
    )
    
    class Meta:
        model = Tenant
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter organization name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter URL-friendly name (e.g., techcorp-events)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter organization description',
                'rows': 3
            }),
        }
    
    def save(self, commit=True):
        tenant = super().save(commit=False)
        tenant.is_active = True
        
        if commit:
            tenant.save()
            
            # Create organizer user
            organizer_email = self.cleaned_data['organizer_email']
            organizer_first_name = self.cleaned_data['organizer_first_name']
            organizer_last_name = self.cleaned_data['organizer_last_name']
            organizer_password = self.cleaned_data['organizer_password']
            
            organizer = User.objects.create_user(
                username=f"{tenant.slug}_admin",
                email=organizer_email,
                first_name=organizer_first_name,
                last_name=organizer_last_name,
                password=organizer_password,
                role='admin',
                tenant=tenant
            )
        
        return tenant
