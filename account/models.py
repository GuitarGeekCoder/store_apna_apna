from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.contrib.auth.hashers import make_password
class City(models.Model):
    name = models.CharField(max_length=500)

    class Meta:
        db_table="city"
        app_label="account"  

    def __str__(self):
        return self.name
      
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Override groups and user_permissions to avoid conflicts with related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Avoid conflict with the default 'user_set'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Avoid conflict with the default 'user_set'
        blank=True
    )
    city = models.ForeignKey(City,on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar_images/", blank=True, null=True)
    address = models.TextField(blank=True,null=True)
    class Meta:
        db_table = 'user'
        app_label = 'account'
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        # If the password is being set, make sure it's hashed
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt')):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

def fetch_user(user_id):
    try:
        return User.objects.filter(pk=user_id,is_active=True).first()
    except Exception as e:
        print("Exception in fetching user:",str(e))
        return None