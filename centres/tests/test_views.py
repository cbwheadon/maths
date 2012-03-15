from django.test import TestCase
from centres.models import Centre, Candidate, UserItemBank
from item_banks.models import ItemBank, Domain, QuestionType
from cat_test.models import CatTest
import datetime
from django.contrib.auth.models import User
from django.test.client import Client
from functional_tests import ROOT

class TestUserItemBanksView(TestCase):
        def test_user_item_bank_view(self):
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.first_name = "John"
          user.last_name = "Lennon"
          user.save()
          self.client = Client()
          response = self.client.get(ROOT + '/accounts/login/')
          #Set up a default cat_test type
          cat_test = CatTest.objects.get(pk=1)
          
          #Set up two item banks and associate with user
          user = User.objects.get(pk=1) 
          domain = Domain.objects.get(name="Number")
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Addition"
          item_bank.domain = domain
          item_bank.question_type = QuestionType.objects.get(pk=1)
          item_bank.save()
          user_item_bank = UserItemBank()
          user_item_bank.user = user
          user_item_bank.item_bank = item_bank
          user_item_bank.save()
          
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Subtraction"
          item_bank.domain = domain
          item_bank.question_type = QuestionType.objects.get(pk=1)
          item_bank.save()
          user_item_bank = UserItemBank()
          user_item_bank.user = user
          user_item_bank.item_bank = item_bank
          user_item_bank.save()
          
          #log in
          response = self.client.post(ROOT + '/accounts/login/', {'username': 'john', 'password': 'johnpassword'})
          
          response = self.client.get(ROOT + '/welcome/')
          self.assertIn('Domain', response.content)
          self.assertIn('Fractions', response.content)
          self.assertIn('Addition', response.content)
          #Test user banks are there
          self.assertEqual(len(response.context['user_banks']), 2)  
          #Test there are links to start a test
          self.assertIn('/start/?item_bank_id=1&cat_test_id=1', response.content)
          
        def test_user_item_bank_link_with_start_view(self):  
          
          #Test that link goes to start with query string picked up
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.save()
          domain = Domain.objects.get(name="Number")
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Addition"
          item_bank.domain = domain
          item_bank.question_type = QuestionType.objects.get(pk=1)
          item_bank.save()
          user_item_bank = UserItemBank()
          user_item_bank.user = user
          user_item_bank.item_bank = item_bank
          user_item_bank.save()        
          self.client.login(username='john', password='johnpassword')
          response = self.client.get('/start/', {'item_bank_id': '1', 'cat_test_id': '1'})
          self.assertIn('Fractions',response.content)
          self.assertIn('Short Test',response.content)
          
        
class TestLogInView(TestCase):
        def test_log_in_page(self):
          #Create new user
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.first_name = "John"
          user.last_name = "Lennon"
          user.save()
          client = Client()
          response = client.get(ROOT + '/accounts/login/')
          # check the log in appears on the page
          self.assertIn('Username', response.content)
          #check user can log in
          response = client.post('/accounts/login/', {'username': 'john', 'password': 'johnpassword'})
          #check valid page
          self.assertEqual(response.status_code, 302)
          
class TestWelcomeNoLogin(TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/welcome/')
        self.assertEqual(response.status_code, 302)          

class TestWelcomeLogin(TestCase):
    def test__login_details(self):
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
        item_bank.save()
        user_item_bank = UserItemBank()
        user_item_bank.user = user
        user_item_bank.item_bank = item_bank
        user_item_bank.save()        
        client = Client()
        client.login(username='john', password='johnpassword')
        response = client.get('/welcome/')         
        self.assertEqual(response.templates[0].name, 'user_item_banks.html')
        n = len(UserItemBank.objects.filter(user=user))
        self.assertEqual(len(response.context['user_banks']), n)       