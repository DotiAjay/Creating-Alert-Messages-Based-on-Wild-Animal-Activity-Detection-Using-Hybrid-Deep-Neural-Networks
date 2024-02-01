from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    gender= models.CharField(max_length=30)
    address= models.CharField(max_length=30)


class predict_animal_activity_detection(models.Model):

    Fid= models.CharField(max_length=3000)
    Forest_Name= models.CharField(max_length=3000)
    Location= models.CharField(max_length=3000)
    Animal= models.CharField(max_length=3000)
    Height_cm= models.CharField(max_length=3000)
    Weight_kg= models.CharField(max_length=3000)
    Color= models.CharField(max_length=3000)
    Diet= models.CharField(max_length=3000)
    Habitat= models.CharField(max_length=3000)
    Predators= models.CharField(max_length=3000)
    Countries_Found= models.CharField(max_length=3000)
    Conservation_Status= models.CharField(max_length=3000)
    Family= models.CharField(max_length=3000)
    Social_Structure= models.CharField(max_length=3000)
    Alert_Message_Date= models.CharField(max_length=3000)
    Prediction= models.CharField(max_length=3000)

class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



