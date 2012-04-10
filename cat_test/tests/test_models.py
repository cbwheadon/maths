from django.test import TestCase
from django.test.client import Client
from functional_tests import ROOT
from cat_test.models import CatTest, CatTestItem, UserCatTest, CatTestItemFractionAnswer
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Domain, ItemBankQuestion, QuestionType, ItemBankTemplate, Threshold, Grade
from centres.models import UserItemBank, UserItemBankProbabilities
from fractionqs.models import FractionWithConstant
import datetime, math

class TestCatTest(TestCase):
    def test_create_and_save_cat(self):
      #check it returns its own name
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.min_items = 5
      cat_test.max_items = 10
      cat_test.max_se = 2
      cat_test.save()
      ct = CatTest.objects.get(name="short")
      self.assertEquals(ct.name,"short")
      self.assertEquals(ct.min_items,5)
      self.assertEquals(ct.max_items,10)
      self.assertEquals(ct.max_se,2)

class TestUserCatTest(TestCase):
    def test_create_and_save(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.time_taken = 12      
      user_cat_test.save()
      uct = UserCatTest.objects.all()[0]
      self.assertEquals(uct.user,user)
      self.assertEquals(uct.item_bank,item_bank)
      self.assertEquals(uct.cat_test,cat_test)
      self.assertEquals(uct.time_taken,12)
      
    def test_endTest(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.max_items = 10
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.items = 10
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,True)
      user_cat_test.items = 9
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,False)
      user_cat_test.items = 5
      user_cat_test.stand_dev = 0.1
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,True)
      user_cat_test.items = 5
      user_cat_test.stand_dev = 2
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,False)
      user_cat_test.items = 2
      user_cat_test.stand_dev = 0.1
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,False)
      
    def test_nextQuestion(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.max_items = 10
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      q = user_cat_test.nextQuestion()
      #One item in bank, one taken      
      self.assertEquals(isinstance(q, CatTestItem),True)
      q = user_cat_test.nextQuestion()
      #One item in bank, try to take another, should return None
      self.assertEquals(isinstance(q, CatTestItem),False)
      #Add more questions and see if they are repeated    
      for i in range(1,11):
        ibq = ItemBankQuestion()
        ibq.item_bank = item_bank
        ibq.save()
      for i in range(1,11):
        q = user_cat_test.nextQuestion() 
        print q.item_bank_question.id
      #Add a question of perfect difficulty and see if it is chosen amongst others        
      for i in range(1,11):
        ibq = ItemBankQuestion()
        ibq.item_bank = item_bank
        ibq.save()
      user_cat_test.difficulty = 2
      user_cat_test.stand_err = 0.1
      hibq = ItemBankQuestion()
      hibq.item_bank = item_bank
      hibq.difficulty = 2
      hibq.save()
      q = user_cat_test.nextQuestion()       
      self.assertEquals(q.item_bank_question,hibq)
      #Make ability different to all questions and make sure one is chosen
      user_cat_test.difficulty = 2
      user_cat_test.stand_err = 0.1
      q = user_cat_test.nextQuestion()       
      self.assertEquals(isinstance(q, CatTestItem),True)
      
    def test_updateAbility(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.max_items = 10
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      #First question right
      test_pattern = [1,1,0]
      test_ability = [0,0,math.log(2)]
      test_difficulty = [2,1,-2.0/3.0]
      test_stand_err = [2,2,1.5]
      test_items = [1,2,3]
      test_hardness = [0,0,0]
      test_right = [1,2,2]
      #Make three questions
      for i in range(1,4):
        ibq = ItemBankQuestion()
        ibq.item_bank = item_bank
        ibq.save()
      #Find first question
      user_cat_test.nextQuestion()
      user_cat_test.updateAbility(1)
      self.assertEquals(user_cat_test.right,1)
      self.assertEquals(user_cat_test.items,1)
      self.assertEquals(user_cat_test.difficulty,2)
      self.assertEquals(user_cat_test.hardness,0)      
      self.assertEquals(user_cat_test.ability,0)
      self.assertEquals(user_cat_test.stand_dev,1)
      #Second question right
      user_cat_test.nextQuestion()
      user_cat_test.updateAbility(1)
      self.assertEquals(user_cat_test.right,2)
      self.assertEquals(user_cat_test.items,2)
      self.assertEquals(user_cat_test.difficulty,1)
      self.assertEquals(user_cat_test.hardness,0)      
      self.assertEquals(user_cat_test.ability,0)
      self.assertEquals(user_cat_test.stand_dev,1)
      #Third question wrong
      user_cat_test.nextQuestion()
      user_cat_test.updateAbility(0)
      self.assertEquals(user_cat_test.right,2)
      self.assertEquals(user_cat_test.items,3)
      self.assertEquals(user_cat_test.difficulty, - 2.0/3.0)
      self.assertEquals(user_cat_test.hardness,0)      
      self.assertEquals(user_cat_test.ability,math.log(2))
      self.assertEquals(user_cat_test.stand_dev,1.5)
            
    def test_simAbility(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.max_items = 10
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      grd = Grade.objects.get(name="A")
      thresh = Threshold()
      thresh.grade = grd
      thresh.item_bank = item_bank
      thresh.ability = -1      
      thresh.save()
      user_item_bank.probabilities()      
      probs = UserItemBankProbabilities.objects.filter(user_item_bank=user_item_bank)
      self.assertEquals(len(probs),1)
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      #Make three questions
      for i in range(1,4):
        ibq = ItemBankQuestion()
        ibq.item_bank = item_bank
        ibq.save()
      #Find first question
      user_cat_test.nextQuestion()      
      user_cat_test.simAbility()
      self.assertEquals(round(user_cat_test.ability,3),-0.337)
      self.assertEquals(round(user_cat_test.stand_dev,3),0.885)
      probs = UserItemBankProbabilities.objects.filter(user_item_bank=user_item_bank)[0]
      self.assertEquals(round(probs.probability,0),77.0)	  

      user_cat_test.nextQuestion()      
      user_cat_test.simAbility()
      self.assertEquals(round(user_cat_test.ability,3),-0.813)
      self.assertEquals(round(user_cat_test.stand_dev,3),0.829)      
      
class TestCatTestItem(TestCase):
    def test_create_and_save(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      cat_test_item = CatTestItem()
      cat_test_item.user_cat_test = user_cat_test
      cat_test_item.item_bank_question = ibq
      cat_test_item.time_taken = 12
      ibq.usage +=1
      ibq.save()      
      cat_test_item.save()
      cat_test_item = CatTestItem.objects.all()[0]
      self.assertEquals(cat_test_item.user_cat_test,user_cat_test)
      self.assertEquals(cat_test_item.item_bank_question,ibq)
      self.assertEquals(cat_test_item.time_taken,12)
      self.assertEquals(cat_test_item.item_bank_question.usage,1)
      
class TestCatTestItemAnswer(TestCase):
    def test_create_and_save(self):
      cat_test = CatTest()
      cat_test.name = "short"
      cat_test.save()
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.save()
      domain = Domain()
      domain.name = "Number"
      domain.create_date = datetime.datetime(2012,03,06)
      domain.save()
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      ibq = ItemBankQuestion()
      ibq.item_bank = item_bank
      ibq.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      cat_test_item = CatTestItem()
      cat_test_item.user_cat_test = user_cat_test
      cat_test_item.item_bank_question = ibq
      cat_test_item.time_taken = 12
      cat_test_item.save()
      answer = FractionWithConstant()
      answer.const = 1
      answer.denom = 2
      answer.num = 3
      answer.save()
      ctifa = CatTestItemFractionAnswer()
      ctifa.cat_test_item = cat_test_item
      ctifa.fraction = answer
      ctifa.save()
      ctifa = CatTestItemFractionAnswer.objects.filter(cat_test_item = cat_test_item)[0]
      self.assertEquals(ctifa.fraction,answer)