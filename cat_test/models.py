from django.db import models
from django.contrib.auth.models import User
from item_banks.models import ItemBank, ItemBankQuestion, Threshold
from fractionqs.models import FractionWithConstant
from centres.models import UserItemBank, UserItemBankProbabilities
import random, math
from pyper import *
from numpy import array

class CatTest(models.Model):
    name = models.CharField(max_length=20)
    min_items = models.IntegerField(default=4)
    max_items = models.IntegerField(default=10)
    max_se = models.IntegerField(default=0.1)    
    
class UserCatTest(models.Model):
    user = models.ForeignKey(User)
    item_bank = models.ForeignKey(ItemBank)
    cat_test = models.ForeignKey(CatTest)
    ability = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)    
    stand_dev = models.FloatField(default=1)
    items = models.IntegerField(default=0)
    hardness = models.FloatField(default=0)
    right = models.IntegerField(default=0)
    threshold = models.FloatField(default=0)
    time_taken = models.IntegerField(default=0)
    
    def __unicode__(self):
      return u'Ability: %s Difficulty %s Stand_Err %s Items %s Hardness %s Right %s' % (self.ability, self.difficulty,self.stand_dev, self.items, self.hardness, self.right)        

    def endTest(self):
    #Reasons for ending
    #Max item reached
    #Min items reached and less than max standard error
      endNow = False    
      if self.items >= self.cat_test.min_items and self.stand_dev <= self.cat_test.max_se:    
        endNow = True
      elif self.items >= self.cat_test.max_items:
        endNow = True
      return(endNow)
      
    def nextQuestion(self):
      #1. Request next candidate. Set D=0, L=0, H=0, and R=0.
      #2. Find next item near difficulty, D.
      start_range = self.difficulty - self.stand_dev
      end_range = self.difficulty + self.stand_dev
      qrange = ItemBankQuestion.objects.filter(difficulty__range=(start_range,end_range),item_bank=self.item_bank)
      qrange = qrange.exclude(cattestitem__user_cat_test=self)
      if len(qrange) == 0:
        #If none in ideal range choose any
        #Could widen range first
        print "Widening range"
        qrange = ItemBankQuestion.objects.all()
        qrange = qrange.exclude(cattestitem__user_cat_test=self)
        if len(qrange) == 0:
          return(None)
      #Pick a random item
      q = random.choice(qrange)
      q.usage +=1
      q.save()
      #3. Set D at the actual calibration of that item.    
      self.difficulty = q.difficulty       
      self.save()    
      cti = CatTestItem(user_cat_test=self,item_bank_question=q)
      cti.save()      
      return(cti)
      
    def updateAbility(self,correct):    
    #4. Administer that item.
    #5. Obtain a response.
    #6. Score that response.
    #7. Count the items taken: L = L + 1
      self.items += 1
    #8. Add the difficulties used: H = H + D
      self.hardness += self.difficulty              
    #9. If response incorrect, update item difficulty: D = D - 2/L
      if correct == 0:
        self.difficulty -= 2.0/self.items
    #10. If response correct, update item difficulty: D = D + 2/L
    #11. If response correct, count right answers: R = R + 1
      if correct==1:
        self.right = self.right + 1      
        self.difficulty += 2.0/self.items
#12. If not ready to decide to pass/fail, Go to step 2.
#13. If ready to decide pass/fail, calculate wrong answers: W = L - R
      wrong = self.items - self.right
#14. Estimate measure: B = H/L + log(R/W)
      if wrong > 0 and self.right > 0:
        self.ability = float(self.hardness)/self.items + math.log(float(self.right)/wrong)
#15. Estimate standard error of the measure: S = L/(R*W)
      if self.right > 2 and wrong == 0:
        self.ability = 5
      if wrong > 2 and self.right == 0:
        self.ability = -5        
      if wrong > 0 and self.right > 0: 
        self.stand_dev = float(self.items) / (self.right*wrong)
#16. Compare B with pass/fail standard T.
#17. If (T - S) < B < (T + S), go to step 2.
#18. If (B - S) > T, then pass.
#19. If (B + S) < T, then fail.
#20. Go to step 1.
      self.save()      
      return(self)
      
    def simAbility(self):
      self.items += 1    
      #start R
      myR = R()
      #set responses so far
      cti = CatTestItem.objects.filter(user_cat_test=self)
      responses = cti.values_list('correct',flat=True)      
      myR['responses'] = array(responses)
      thr = Threshold.objects.filter(item_bank=self.item_bank)
      thrs = thr.values_list('ability',flat=True)      
      myR['grades'] = array(thrs)
      myR['m.theta'] = self.ability
      myR['s.theta'] = self.stand_dev
      #myR.run('source("C:/Users/User/BitNami DjangoStack projects/maths/rasch/rasch.R")')
      myR.run('source("C:/Users/cbwheadon/Documents/Django/maths/rasch/rasch.R")')
      self.ability = myR['thm']
      self.stand_dev = myR['ths']
      grade_probs = myR['probs']
	  
      #Update grade probabilities
      user_item_bank = UserItemBank.objects.filter(user=self.user,item_bank = self.item_bank)
      i = 0      
      for th in thr:
        prob = UserItemBankProbabilities.objects.get(threshold=th,user_item_bank=user_item_bank)
        if len(thr) > 1:
          prob.probability = grade_probs[i] * 100
        else:
          prob.probability = grade_probs * 100   
        i += 1
        prob.save()        
      del myR
      self.save()      
      return(self)
      
    def updateTime(self):
      cti = CatTestItem.objects.filter(user_cat_test=self)
      time_taken = cti.values_list('time_taken',flat=True)    
      self.time_taken = sum(time_taken)
      self.save()
      return(self)
      
class CatTestItem(models.Model):      
    user_cat_test = models.ForeignKey(UserCatTest)
    item_bank_question = models.ForeignKey(ItemBankQuestion)
    correct = models.IntegerField(default=0)
    skip = models.IntegerField(default=2)    
    time_taken = models.IntegerField(default=0)
    
class CatTestItemFractionAnswer(models.Model):
    cat_test_item = models.ForeignKey(CatTestItem)
    fraction = models.ForeignKey(FractionWithConstant)    