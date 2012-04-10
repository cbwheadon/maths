from django.db import models
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Threshold
import datetime

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
  time_taken_str = models.CharField(max_length=8,default='00:00:00')  
  ability = models.FloatField(default=0)
  ability_stand_dev = models.FloatField(default=1)
  grade = models.IntegerField(default=0)    
  
  def update(self,user_cat_test):
    self.tests += 1
    self.questions += user_cat_test.items
    self.correct += user_cat_test.right
    self.time_taken += user_cat_test.time_taken
    self.ability = user_cat_test.ability
    self.ability_stand_dev = user_cat_test.stand_dev     
    user_cat_test.updateTime()
    self.time_taken += user_cat_test.time_taken
    self.time_taken_str = str(datetime.timedelta(seconds=self.time_taken))
    self.save()
    return(self)
    
  def probabilities(self):
    #Return grade thresholds  
    threshes = Threshold.objects.filter(item_bank=self.item_bank)
    #For each threshold initialise UserItemBankProbabilities
    for thresh in threshes:
      prob = UserItemBankProbabilities()
      prob.user_item_bank = self
      prob.threshold = thresh
      prob.probability = thresh.init_prob
      prob.save()      
    return(self)    

class UserItemBankProbabilities(models.Model):
    user_item_bank = models.ForeignKey(UserItemBank)
    threshold = models.ForeignKey(Threshold)
    probability = models.FloatField()      