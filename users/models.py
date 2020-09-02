# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import datetime
date = datetime.datetime.now()

class User(AbstractUser):
    # add additional fields in here
    #username = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="Username")
    email = models.EmailField(max_length=25, unique=True, verbose_name="Email")

    def __str__(self):
        return self.first_name

    def get_first_name(self):
        return self.last_name

    def get_full_name(self):
        self.fullname = f'{self.first_name} {self.last_name}'
        return self.fullname

    def get_short_name(self):
        return self.first_name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_code = models.CharField(max_length=20, blank=True, unique=True, default=f'team{date.day}{date.month}{date.microsecond}', verbose_name="Code")
    team_name = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Name")
    team_desc = models.CharField(max_length=150, blank=True, verbose_name="Function")
    team_lead = models.ForeignKey(User, on_delete=models.PROTECT, default=1, blank=True, verbose_name="Team Lead")
    team_date_created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='team_author', verbose_name="Created by")
    team_date_updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='team_last_author', verbose_name="Created by")
    team_date_created = models.DateTimeField(blank=True, verbose_name="Date Created")
    team_date_updated = models.DateTimeField(blank=True, null=True, verbose_name="Last Update")

    def __str__(self):
        return f'Team {self.team_name}'

class Profile(models.Model):
    Support = 1
    Developer = 2
    Supervisor= 3
    Manager = 4
    Administrator = 5
    Male = 1
    Female = 2
    Other = 3
    Single = 1
    Married = 2
    Divorced = 3
    Separated = 4
    Widowed = 5


    GENDER_CHOICES = (
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other'),
    )

    MARITAL_STATUS_CHOICES = (
        (Single, 'Single'),
        (Married, 'Married'),
        (Divorced, 'Divorced'),
        (Separated, 'Separated'),
        (Widowed, 'Widowed'),
    )

    ROLE_CHOICES = (
        (Support, 'Support'),
        (Developer, 'Developer'),
        (Supervisor, 'Supervisor'),
        (Manager, 'Manager'),
        (Administrator, 'Administrator'),
    )

    date = datetime.datetime.now()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_code = models.CharField(max_length=30, default=f'{date.month}{date.day}{date.year}{date.microsecond}', verbose_name="User code")
    middle_name = models.CharField(max_length=30, blank=True, default='', verbose_name="Middle name")
    extension_name = models.CharField(max_length=5, blank=True, default='', verbose_name="Extension")
    nickname = models.CharField(max_length=25, blank=True, default='', verbose_name="Nickname")
    team = models.ForeignKey(Team, on_delete=models.PROTECT, blank=True, null=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS_CHOICES, default=1, verbose_name="Status")
    phone_number = models.CharField(max_length=25, blank=True, default='', verbose_name="Phone number")
    mobile_number = models.CharField(max_length=25, blank=True, default='', verbose_name="Mobile number")
    birth_date = models.DateField(max_length=25, blank=True, null=True, verbose_name="Date of birth")
    present_address = models.TextField(max_length=135, blank=True, default='', verbose_name="Present address")
    permanent_address = models.TextField(max_length=135, blank=True, default='', verbose_name="Permanent address")
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=1, verbose_name="Gender")
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    type = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    def get_profile_type(self):
        return dict(self.ROLE_CHOICES).get(self.type)

    def get_gender(self):
        return dict(self.GENDER_CHOICES).get(self.type)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
            return f'{self.nickname}\'s Profile'



