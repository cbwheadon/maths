from django.db import models
from fractionqs.models import FractionBankQuestion
import datetime

class ItemBankTemplate(models.Model):
  name = models.CharField(max_length=20)

class QuestionType(models.Model):
  name = models.CharField(max_length=20)
 
class Domain(models.Model):
  name = models.CharField(max_length=200)
  create_date = models.DateField(default=datetime.date.today)  

  def __unicode__(self):
    return self.name  

class ItemBank(models.Model):
  name = models.CharField(max_length=200)
  domain = models.ForeignKey(Domain)  
  topic = models.CharField(max_length=200)
  template = models.ForeignKey(ItemBankTemplate)
  question_type = models.ForeignKey(QuestionType)  
  create_date = models.DateField(default=datetime.date.today)
 
  def __unicode__(self):
    return self.name  
    
  def fill(self,bank,typ):
    if typ == "fractions":
      fbqs = FractionBankQuestion.objects.filter(fraction_question_bank=bank)
      #Link item bank and question bank
      for fbq in fbqs:
        ibq = ItemBankQuestion()
        ibq.item_bank = self
        ibq.usage = 0
        ibq.difficulty = 0
        ibq.sd_difficulty = 0
        ibq.discrimination = 1
        ibq.save()
        ibfb = ItemBankFractionQuestion()
        ibfb.item_bank_question = ibq
        ibfb.fraction_bank_question = fbq
        ibfb.save()
    
class ItemBankQuestion(models.Model):
  item_bank = models.ForeignKey(ItemBank)
  usage = models.IntegerField(default=0)
  difficulty = models.IntegerField(default=0)
  sd_difficulty = models.IntegerField(default=0)
  discrimination = models.IntegerField(default=1)
  
class ItemBankFractionQuestion(models.Model):
  item_bank_question = models.ForeignKey(ItemBankQuestion)
  fraction_bank_question = models.ForeignKey(FractionBankQuestion)  