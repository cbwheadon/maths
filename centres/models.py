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
  accuracy = models.FloatField(default=0)
  time_taken = models.IntegerField(default=0)
  accuracy_time = models.FloatField(default=0)
  in_a_row = models.IntegerField(default=0)
  most_in_a_row = models.IntegerField(default=0)
  quickest = models.IntegerField(default=0)
  ability = models.FloatField(default=0)
  highest_ability = models.FloatField(default=0)
  grade = models.IntegerField(default=0)	
  highest_grade = models.IntegerField(default=0)
  
  def update(self,cat_test_item):
    record_list = []
    self.questions += 1
    self.correct += cat_test_item.correct
    self.accuracy = float(self.correct) / float(self.questions) 
    self.time_taken += cat_test_item.time
    if self.time_taken > 0:	  
      self.accuracy_time = float(self.correct) / float(self.time_taken)
    if cat_test_item.correct == 1:
      self.in_a_row +=1	
    else:
      self.in_a_row = 0	
    if self.in_a_row > self.most_in_a_row:
      self.most_in_a_row = self.in_a_row
      record_list.append('Most in a row!')
    if cat_test_item.correct == 1:
      if cat_test_item.time < self.quickest or self.quickest == 0:
        self.quickest = cat_test_item.time
        record_list.append('Quickest ever!')
    self.save()		  
    return(record_list)  