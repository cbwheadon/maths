from django.test import TestCase
from functional_tests import ROOT
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Domain, ItemBankQuestion
from centres.models import UserItemBank
from cat_test.models import CatTest, UserCatTest
from fractionqs.models import FractionQuestionBank, Oper

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
          user_cat_test = UserCatTest.objects.get(user=user)
          self.assertEquals(user_cat_test.items,0)
        
        def test_start_test_wout_login_view(self):
          response = self.client.get('/start/')
          self.assertEqual(response.status_code, 302)

class TestCatQuestionView(TestCase):
        def test_question_view_w_login(self):
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
          item_bank.template = "fractions.html"
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
                
        def test_question_view_wout_login(self):
          response = self.client.get('/question/')
          self.assertEqual(response.status_code, 302)
          
        def test_question_view_post(self):
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.save()
          self.client.login(username='john', password='johnpassword')
          response = self.client.post('/question/',follow=True)
          print response.redirect_chain 
          self.assertEqual(response.status_code, 200)

class TestCatFeedbackView(TestCase):
          def test_question_view_wout_login(self):
            response = self.client.get('/feedback/')
            self.assertEqual(response.status_code, 302)
            
          def test_question_view_w_login(self):
            user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
            user.save()
            self.client.login(username='john', password='johnpassword')
            response = self.client.get('/feedback/')
            self.assertEqual(response.status_code, 200)    
            self.assertTemplateUsed(response, 'feedback.html')
        