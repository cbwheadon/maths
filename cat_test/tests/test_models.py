from django.test import TestCase
from django.test.client import Client
from functional_tests import ROOT
from cat_test.models import CatTest, CatTestItem, UserCatTest
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Domain, ItemBankQuestion
from centres.models import UserItemBank
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
      item_bank.create_date = datetime.datetime(2012,03,06)
      item_bank.save()
      user_item_bank = UserItemBank()
      user_item_bank.user = user
      user_item_bank.item_bank = item_bank
      user_item_bank.save()
      user_cat_test = UserCatTest()
      user_cat_test.user = user
      user_cat_test.item_bank = item_bank
      user_cat_test.cat_test = cat_test
      user_cat_test.save()
      uct = UserCatTest.objects.all()[0]
      self.assertEquals(uct.user,user)
      self.assertEquals(uct.item_bank,item_bank)
      self.assertEquals(uct.cat_test,cat_test)
      
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
      item_bank.create_date = datetime.datetime(2012,03,06)
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
      user_cat_test.stand_err = 0.1
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,True)
      user_cat_test.items = 5
      user_cat_test.stand_err = 2
      user_cat_test.save()
      end_test = user_cat_test.endTest()
      self.assertEquals(end_test,False)
      user_cat_test.items = 2
      user_cat_test.stand_err = 0.1
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
      item_bank.create_date = datetime.datetime(2012,03,06)
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
      item_bank.create_date = datetime.datetime(2012,03,06)
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
      #Second question right
      user_cat_test.nextQuestion()
      user_cat_test.updateAbility(1)
      self.assertEquals(user_cat_test.right,2)
      self.assertEquals(user_cat_test.items,2)
      self.assertEquals(user_cat_test.difficulty,1)
      self.assertEquals(user_cat_test.hardness,0)      
      self.assertEquals(user_cat_test.ability,0)
      #Third question wrong
      user_cat_test.nextQuestion()
      user_cat_test.updateAbility(0)
      self.assertEquals(user_cat_test.right,2)
      self.assertEquals(user_cat_test.items,3)
      self.assertEquals(user_cat_test.difficulty, - 2.0/3.0)
      self.assertEquals(user_cat_test.hardness,0)      
      self.assertEquals(user_cat_test.ability,math.log(2))
      
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
      item_bank.create_date = datetime.datetime(2012,03,06)
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
      cat_test_item.save()
      cat_test_item = CatTestItem.objects.all()[0]
      self.assertEquals(cat_test_item.user_cat_test,user_cat_test)
      self.assertEquals(cat_test_item.item_bank_question,ibq)
      