from django.test import TestCase
from functional_tests import ROOT
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Domain, ItemBankQuestion, QuestionType, ItemBankFractionQuestion, ItemBankTemplate, Grade, Threshold
from centres.models import UserItemBank
from cat_test.models import CatTest, UserCatTest, CatTestItem
from fractionqs.models import FractionQuestionBank, Oper
import math

class TestCatTestViews(TestCase):
        def test_start_test_view(self):
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.save()
          self.client.login(username='john', password='johnpassword')
          #create structures
          cat_test = CatTest()
          cat_test.name = "Short Test"
          cat_test.save()
          domain = Domain.objects.get(pk=1)
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
          response = self.client.get('/start/', {'item_bank_id': item_bank.id, 'cat_test_id':cat_test.id})
          #Test that page exists
          self.assertEqual(response.status_code, 200)
          #Test that is has been rendered with a template
          self.assertTemplateUsed(response, 'start_test.html')
          #Test that it displays item bank name and cat_test name
          self.assertIn('Fractions',response.content)
          self.assertIn('Addition',response.content)
          self.assertIn('Short Test',response.content)
          self.assertIn('4', response.content)
          self.assertIn('10', response.content)
        
        def test_start_old_cat_view(self):
          #test that if a user has done more than one test the right one is being updated           
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.save()
          self.client.login(username='john', password='johnpassword')
          #create structures
          cat_test = CatTest()
          cat_test.name = "Short Test"
          cat_test.save()
          domain = Domain.objects.get(pk=1)
          item_bank = ItemBank()
          item_bank.question_type = QuestionType.objects.get(pk=1)
          item_bank.name = "Fractions"
          item_bank.topic = "Addition"
          item_bank.domain = domain
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
          user_cat_test.items = 6
          user_cat_test.save()
          user_cat_test = UserCatTest()
          response = self.client.get('/start/', {'item_bank_id': item_bank.id, 'cat_test_id':cat_test.id})
          ucts = UserCatTest.objects.filter(user=user)
          self.assertEquals(len(ucts),2)
          ucts = ucts.order_by('-id')
          self.assertEquals(ucts[0].items,0)
        
        def test_start_test_wout_login_view(self):
          response = self.client.get('/start/')
          self.assertEqual(response.status_code, 302)

class TestCatQuestionView(TestCase):
        def test_question_view_w_login(self):
          #Test the post functionality of the question view         
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.save()
          self.client.login(username='john', password='johnpassword')
          
          #create structures
          cat_test = CatTest()
          cat_test.name = "Short Test"
          cat_test.save()
          domain = Domain.objects.get(pk=1)
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Addition"
          item_bank.domain = domain
          item_bank.template = ItemBankTemplate.objects.get(pk=1)
          item_bank.question_type = QuestionType.objects.get(pk=1)
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
          #Give the test some questions
          #Create fraction question bank
          fqb = FractionQuestionBank()
          oper = Oper.objects.get(pk=1)
          n = 20
          st = 0
          en = 10
          name = "Test Bank"
          negatives_allowed = True
          fqb.generate(name,st,en,negatives_allowed,oper,n)
          #Fill item bank from fraction question bank
          item_bank.fill(fqb,"fractions")      
          response = self.client.get('/question/')
          self.assertEqual(response.status_code, 200)
          #Test that is has been rendered with a template
          self.assertTemplateUsed(response, 'question.html')
          #Question needs to know how to display itself
          self.assertIn('Fractions',response.content)
          #Fractions pulls in a fractions template          
          self.assertIn('Fraction Question',response.content)
          #Increments question
          self.assertIn('Questions completed: 0',response.content)
          #Displays the correct sign for a fraction question
          self.assertIn('+',response.content)
          #Test item_bank usage has been incremented          
          cat_test_item = CatTestItem.objects.filter(user_cat_test=user_cat_test)
          self.assertEquals(len(cat_test_item),1)
          cat_test_item = cat_test_item.order_by('-id')[0]
          self.assertEquals(cat_test_item.item_bank_question.usage,1)
          #Correct answer to question
          ibfq = ItemBankFractionQuestion.objects.filter(item_bank_question=cat_test_item.item_bank_question)
          answer = ibfq[0].fraction_bank_question.question.answer
          #Test post triggers marking process
          response = self.client.post('/question/', {'const': answer.const, 'num': answer.num, 'denom': answer.denom, 'time': 12})
          user_cat_test = UserCatTest.objects.get(user=user)
          self.assertEqual(user_cat_test.items,1)
          self.assertEqual(round(user_cat_test.ability,2),0.28)
          self.assertEqual(round(user_cat_test.stand_dev,2),0.91)
          #Check that a response has now been saved to user_cat_test
          cti = CatTestItem.objects.filter(user_cat_test=user_cat_test)
          self.assertEqual(len(cti),1)
          #Check response has been saved to cti
          self.assertEqual(cti[0].correct,1)
          self.assertEqual(cti[0].time_taken,12)
          #Try another
          cat_test_item = user_cat_test.nextQuestion()
          cat_test_item = CatTestItem.objects.filter(user_cat_test=user_cat_test)
          cat_test_item = cat_test_item.order_by('-id')[0]
          ibfq = ItemBankFractionQuestion.objects.filter(item_bank_question=cat_test_item.item_bank_question)
          answer = ibfq[0].fraction_bank_question.question.answer
          #Test post triggers marking process
          response = self.client.post('/question/', {'const': answer.const, 'num': answer.num, 'denom': answer.denom, 'time': 22})
          user_cat_test = UserCatTest.objects.get(user=user)
          self.assertEqual(user_cat_test.items,2)
          self.assertEqual(round(user_cat_test.ability,2),0.75)
          self.assertEqual(round(user_cat_test.stand_dev,2),0.82)          
          #Check that a response has now been saved to user_cat_test
          cti = CatTestItem.objects.filter(user_cat_test=user_cat_test)
          cti = cti.order_by('-id')
          self.assertEqual(len(cti),2)
          #Check response has been saved to cti
          self.assertEqual(cti[0].correct,1)
          self.assertEqual(cti[0].time_taken,22)          
          #Try another
          cat_test_item = user_cat_test.nextQuestion()
          #Test post triggers marking process
          response = self.client.post('/question/', {'const': answer.const, 'num': answer.num, 'denom': answer.denom, 'time': 3})
          user_cat_test = UserCatTest.objects.get(user=user)
          self.assertEqual(user_cat_test.items,3)
          self.assertEqual(round(user_cat_test.ability,2),0.76)
          self.assertEqual(round(user_cat_test.stand_dev,2),0.71)          
          #Check that a response has now been saved to user_cat_test
          cti = CatTestItem.objects.filter(user_cat_test=user_cat_test)
          cti = cti.order_by('-id')
          self.assertEqual(len(cti),3)
          #Check response has been saved to cti
          self.assertEqual(cti[0].correct,0)
          self.assertEqual(cti[0].time_taken,3)                   
          
        def test_question_view_wout_login(self):
          response = self.client.get('/question/')
          self.assertEqual(response.status_code, 302)

class TestCatFeedbackView(TestCase):
          #def test_question_view_wout_login(self):
            #response = self.client.get('/feedback/')
            #self.assertEqual(response.status_code, 302)
            
          #def test_question_view_w_login(self):
            #user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            #user.save()
            #self.client.login(username='john', password='johnpassword')
            #response = self.client.get('/feedback/')
            #self.assertEqual(response.status_code, 200)    
            #self.assertTemplateUsed(response, 'feedback.html')
            
          def test_feedback(self):
            #Test the post functionality of the question view         
            user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user.save()
            self.client.login(username='john', password='johnpassword')
            
            #create structures
            cat_test = CatTest()
            cat_test.name = "Short Test"
            cat_test.save()
            domain = Domain.objects.get(pk=1)
            item_bank = ItemBank()
            item_bank.name = "Fractions"
            item_bank.topic = "Addition"
            item_bank.domain = domain
            item_bank.template = ItemBankTemplate.objects.get(pk=1)
            item_bank.question_type = QuestionType.objects.get(pk=1)
            item_bank.save()
            user_item_bank = UserItemBank()
            user_item_bank.user = user
            user_item_bank.item_bank = item_bank
            user_item_bank.save()
            #Create a threshold
            grd = Grade.objects.get(name="A")
            thresh = Threshold()
            thresh.grade = grd
            thresh.item_bank = item_bank
            thresh.ability = -1      
            thresh.save()
            
            user_item_bank.probabilities()
            user_cat_test = UserCatTest()
            user_cat_test.user = user
            user_cat_test.item_bank = item_bank
            user_cat_test.cat_test = cat_test
            user_cat_test.save()
            
            #Give the test some questions
            #Create fraction question bank
            fqb = FractionQuestionBank()
            oper = Oper.objects.get(pk=1)
            n = 20
            st = 0
            en = 10
            name = "Test Bank"
            negatives_allowed = True
            fqb.generate(name,st,en,negatives_allowed,oper,n)
            #Fill item bank from fraction question bank
            item_bank.fill(fqb,"fractions")
            user_cat_test = UserCatTest()
            user_cat_test.user = user
            user_cat_test.item_bank = item_bank
            user_cat_test.cat_test = cat_test
            user_cat_test.save()
            cat_test_item = user_cat_test.nextQuestion()
            #Correct answer to question
            ibfq = ItemBankFractionQuestion.objects.filter(item_bank_question=cat_test_item.item_bank_question)
            answer = ibfq[0].fraction_bank_question.question.answer
            #Test post triggers marking process
            response = self.client.post('/question/', {'const': answer.const+1, 'num': answer.num+1, 'denom': answer.denom+1, 'time': 12})
            print answer.const, answer.num, answer.denom
            response = self.client.get('/feedback/')
            #First question right
            #Should say right or wrong
            self.assertIn('Wrong!',response.content)
            #Should give user's answer
            self.assertIn(str(answer.const+1),response.content)
            #Should give user's answer
            self.assertIn(str(answer.num+1),response.content)
            #Should give user's answer
            self.assertIn(str(answer.denom+1),response.content)
            #Should give right answer
            self.assertIn(str(answer.const),response.content)
            self.assertIn(str(answer.num),response.content)
            self.assertIn(str(answer.denom),response.content)
            #Should show user's time
            self.assertIn('12',response.content)
            #Should show probabilities
            self.assertIn('%',response.content)            

class TestCatEnd(TestCase):
          def test_end_wout_login(self):
            response = self.client.get('/end/')
            self.assertEqual(response.status_code, 302)

          def test_end_w_login(self):
            user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user.save()
            self.client.login(username='john', password='johnpassword')
            response = self.client.get('/end/')
            self.assertEqual(response.status_code, 200)    
            self.assertTemplateUsed(response, 'end_test.html')

          def test_display_user_cat_test(self):
            #Test the post functionality of the question view         
            user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user.save()
            self.client.login(username='john', password='johnpassword')
            
            #create structures
            cat_test = CatTest()
            cat_test.name = "Short Test"
            cat_test.save()
            domain = Domain.objects.get(pk=1)
            item_bank = ItemBank()
            item_bank.name = "Fractions"
            item_bank.topic = "Addition"
            item_bank.domain = domain
            item_bank.template = ItemBankTemplate.objects.get(pk=1)
            item_bank.question_type = QuestionType.objects.get(pk=1)
            item_bank.save()
            user_item_bank = UserItemBank()
            user_item_bank.user = user
            user_item_bank.item_bank = item_bank
            user_item_bank.save()
			#Create a threshold
            grd = Grade.objects.get(name="A")
            thresh = Threshold()
            thresh.grade = grd
            thresh.item_bank = item_bank
            thresh.ability = -1
            thresh.init_prob =50			
            thresh.save()
            user_item_bank.probabilities()
            user_cat_test = UserCatTest()
            user_cat_test.user = user
            user_cat_test.item_bank = item_bank
            user_cat_test.cat_test = cat_test
            user_cat_test.save()
            response = self.client.get('/end/')
            self.assertIn('Ability: 0',response.content)
            user_item_bank = UserItemBank.objects.get(pk=1)
            self.assertEqual(user_item_bank.tests,1)
            #Should show probabilities
            self.assertIn('50%',response.content)