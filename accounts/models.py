from typing import Any, Optional
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "CustomUser":
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not password:
            raise ValueError(_('A password must be provided'))
            
        email = self.normalize_email(email)
        base_username = email.split('@')[0]

        # Optimize unique username generation:
        # Retrieve all usernames that start with the base_username in one query.
        existing_usernames = set(
            self.model.objects.filter(username__startswith=base_username)
            .values_list('username', flat=True)
        )
        username = base_username
        counter = 1
        while username in existing_usernames:
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create the user instance with the generated unique username.
        user = self.model(email=email, username=username, **extra_fields)
        
        # Validate the password using Django's password validators.
        validate_password(password, user)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "CustomUser":
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', CustomUser.UserRole.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
            
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    # Removed redundant "name" field. The combination of first_name and last_name is used instead.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & password are required by default.

    objects = CustomUserManager()

    class UserRole(models.TextChoices):
        CUSTOMER = 'CUSTOMER', _('Customer')
        AGENT = 'AGENT', _('Agent')
        ADMIN = 'ADMIN', _('Admin')
    
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user account is active.')
    )
    
    # Rely on AbstractUser for:
    # - first_name
    # - last_name
    # - username (which is unique and already indexed)
    # - date_joined and last_login

    def __str__(self) -> str:
        return self.email

    @property
    def is_customer(self) -> bool:
        """Return True if the user's role is CUSTOMER."""
        return self.role == self.UserRole.CUSTOMER
    
    @property
    def is_agent(self) -> bool:
        """Return True if the user's role is AGENT."""
        return self.role == self.UserRole.AGENT
    
    @property
    def full_name(self) -> str:
        """
        Return the full name of the user, falling back to email if first_name and last_name are not provided.
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            # The unique 'username' field is automatically indexed.
        ]
