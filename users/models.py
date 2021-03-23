from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager
from rest_framework_api_key.models import AbstractAPIKey, BaseAPIKeyManager


class Organization(models.Model):
    name = models.CharField(max_length=128)
    subdomain_prefix = models.CharField(max_length=100, null=True, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        

class Company(models.Model):
    name = models.CharField(max_length=55)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name='organization_companies')

    def __str__(self):
        return self.name


class OrganizationAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    
    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Organization API key"
        verbose_name_plural = "Organization API keys"
    

class GeneralModel(models.Model):
    organizations = models.ManyToManyField(Organization)
    # need to update how permissioning is done for different groups to account
    # for the change from a single ManyToOne User-Org relationship to ManyToMany
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='%(app_label)s_company_%(class)s')

    class Meta:
        abstract = True


class OrganizationAPIKeyManager(BaseAPIKeyManager):
    def get_usable_keys(self):
        return super().get_usable_keys().filter(organization__active=True)


class UserManager(BaseUserManager):

    use_in_migrations = True
    
    #groups, organization, guest_organizations,
    def _create_user(self, email, password, **extra_fields):
        print('CREATING USER!!!')
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields,
            #groups=Group.objects.get(id=groups),
            #organization=Organization.objects.get(id=organization),
            #guest_organizations=guest_organizations,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        print('sdfsfdsf @@@@@@@')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, GeneralModel):
    groups = models.ManyToManyField(Group)#, on_delete=models.CASCADE)
    # Organizations relation is already set in the GeneralModel Abstract
    #organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name='users')
    guest_organizations = models.ManyToManyField(Organization, blank=True, related_name='guest_organizations_user')
    name = models.CharField(max_length=128, null=True)
    username = None
    email = models.EmailField(verbose_name='email field', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='date joined', auto_now=True)    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class TeamModel(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name






class Invite(GeneralModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender_invite')
    receiver = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, related_name='organization_invite')
    groups = models.ManyToManyField(Group)


    # OAuth library for social/etc AUth providers: https://python-social-auth.readthedocs.io/en/latest/installing.html
    # https://django-allauth.readthedocs.io/en/latest/overview.html