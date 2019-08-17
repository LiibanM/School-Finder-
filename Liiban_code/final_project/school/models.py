from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class mapData(models.Model):
    URN = models.IntegerField(primary_key=True)
    LA = models.CharField(max_length=128, null=True)
    EstablishmentName = models.CharField(max_length=128, null=True)
    TypeOfEstablishment  = models.CharField(max_length=128, null=True)
    PhaseOfEducation = models.CharField(max_length=128, null=True)
    OfficialSixthForm = models.CharField(max_length=128, null=True)
    Gender = models.CharField(max_length=128, null=True)
    AdmissionsPolicy = models.CharField(max_length=128, null=True)
    NumberOfPupils = models.CharField(max_length=128, null=True)
    NumberOfBoys = models.CharField(max_length=128, null=True)
    NumberOfGirls = models.CharField(max_length=128, null=True)
    Street = models.CharField(max_length=128, null=True)
    Locality= models.CharField(max_length=128, null=True)
    Town = models.CharField(max_length=128, null=True)
    County = models.CharField(max_length=128, null=True)
    Postcode = models.CharField(max_length=128, null=True)
    SchoolWebsite = models.CharField(max_length=128, null=True)
    TelephoneNum = models.CharField(max_length=128, null=True)
    HeadTitle = models.CharField(max_length=128, null=True)
    HeadFirstName = models.CharField(max_length=128, null=True)
    HeadLastName = models.CharField(max_length=128, null=True)
    OfstedRating = models.CharField(max_length=128, null=True)
    Longitude = models.FloatField(max_length=128, null=True)
    Latitude = models.FloatField(max_length=128, null=True)

    def __str__(self):
        return self.EstablishmentName


class schoolPerformance(models.Model):
    URN = models.IntegerField(primary_key=True)
    EstablishmentName = models.CharField(max_length=128, null=True)
    Gcse_average_low = models.CharField(max_length=128, null=True)
    Gcse_average_high = models.CharField(max_length=128, null=True)
    Average_Ebacc = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.EstablishmentName

#relationalship link of one to one, each user has 1 name but many schools in lists
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #this only allows the user to selectt either male or female
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    list = models.ManyToManyField(mapData,related_name="lists")
    dob = models.DateField(null=True,blank=True)
    def __str__(self):
        return self.user.username


#This ensures that whenever a user is created, a userprofile is also created.
def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile= UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)
