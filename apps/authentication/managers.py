from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import  ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
 

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    Handles user creation and email validation.
    """
    def email_validator(self,email):
        """
        Validate that the provided email is correct.
        Raises a ValueError if the email is invalid.
        """
        try :
            validate_email(email)
        except ValidationError :
            raise ValueError(_('please enter valid email address'))
        
    def create_user(self,email,first_name,last_name,password,**extra_fields):
        """
        Create and save a regular user with the given email, name, and password.
        """
        if email : 
            email = self.normalize_email(email)
            self.email_validator(email)
        else :
            raise ValueError('an email address is required')    
        if  not first_name :
            raise ValueError('first name is required')
        if  not last_name :
            raise ValueError('last name is required')
        user = self.model(
            email  = email , first_name  = first_name, last_name = last_name  ,**extra_fields
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    def create_superuser(self,email,first_name,last_name,password,**extra_fields):
        """
        Create and save a superuser  with all permissions.
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True :
            raise ValueError(_('is_staff must be true for admin user'))
        if extra_fields.get('is_superuser') is not True :
            raise ValueError(_('is_superuser must be true for admin user'))
        
        user = self.create_user(
            email , first_name , last_name , password, **extra_fields
        )
        user.save(using= self._db)
        return user
        
        
        
            
            
                
        
        
    
