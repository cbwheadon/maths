from django.db import models
from django.contrib.auth.models import User
from item_banks.models import ItemBank

# Create your models here.
class Centre(models.Model):
  name =  models.CharField(max_length=255)
  centre_id = models.CharField(max_length=5)
  create_date = models.DateTimeField()
  
  def __unicode__(self):
    return self.centre_id + " " + self.name  

class Candidate(models.Model):
  gender =  models.CharField(max_length=1)
  dob = models.DateField()
  centre = models.ForeignKey(Centre)
  user = models.OneToOneField(User)   
    
  def __unicode__(self):
    return self.user.first_name + " " + self.user.last_name
    
class UserItemBank(models.Model):
  user = models.ForeignKey(User)
  item_bank = models.ForeignKey(ItemBank)
  tests = models.IntegerField(default=0)    
  questions = models.IntegerField(default=0)
  correct = models.IntegerField(default=0)
  time_taken = models.IntegerField(default=0)
  ability = models.FloatField(default=0)
  ability_stand_err = models.FloatField(default=2)
  grade = models.IntegerField(default=0)    
  
  def update(self,user_cat_test):
    self.tests += 1
    self.questions += user_cat_test.items
    self.correct += user_cat_test.right
    self.time_taken += user_cat_test.time_taken
    self.ability = user_cat_test.ability
    self.ability_stand_err = user_cat_test.stand_err
    self.save()
    return(self)  