from django.test import TestCase
from centres.models import Centre, Candidate, UserItemBank
from item_banks.models import ItemBank, Domain
import datetime
from django.contrib.auth.models import User
from django.test.client import Client
from functional_tests import ROOT

class TestCentre(TestCase):
    def test_create_and_save_centre(self):
        centre = Centre()
        centre.name = "Test School"
        centre.centre_id = "60114"
        centre.create_date = datetime.datetime(2012,03,04)
        centre.save()
        
        #check we can retrieve it
        all_objs = Centre.objects.all()
        self.assertEquals(len(all_objs),1) 
        my_obj = all_objs[0]
        self.assertEquals(my_obj.name, "Test School")
        self.assertEquals(my_obj.centre_id, "60114")
        self.assertEquals(my_obj.create_date, datetime.datetime(2012,03,04))
        
        #check it returns its own name
        self.assertEquals(unicode(my_obj),"60114 Test School")
        
    def test_create_and_save_candidate(self):
        centre = Centre()
        centre.name = "Test School"
        centre.centre_id = "60114"
        centre.create_date = datetime.datetime(2012,03,04)
        centre.save()
        
        #Create new user who belongs to centre
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.first_name = "John"
        user.last_name = "Lennon"
        user.save()
        
        u = User.objects.get(username__exact='john')
        self.assertEquals(u.first_name, "John")
        self.assertEquals(u.last_name, "Lennon")
        
        candidate = Candidate()
        candidate.gender = "M"
        candidate.dob = datetime.date(1969,05,01)
        candidate.centre = centre
        candidate.user = user
        candidate.save()
        
        #check we can retrieve it
        all_objs = Candidate.objects.all()
        self.assertEquals(len(all_objs),1) 
        my_obj = all_objs[0]
        self.assertEquals(my_obj.gender, "M")
        self.assertEquals(my_obj.dob, datetime.date(1969,05,01))
        self.assertEquals(unicode(my_obj.centre),"60114 Test School")
        self.assertEquals(unicode(my_obj.user.first_name),"John")
        self.assertEquals(unicode(my_obj),"John Lennon")

class TestUserItemBanksView(TestCase):
        def test_user_item_bank_view(self):
          user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
          user.first_name = "John"
          user.last_name = "Lennon"
          user.save()
          self.client = Client()
          response = self.client.get(ROOT + '/accounts/login/')
                    
          #Set up two item banks and associate with user
          user = User.objects.get(pk=1) 
          domain = Domain.objects.get(name="Number")
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Addition"
          item_bank.domain = domain
          item_bank.save()
          user_item_bank = UserItemBank()
          user_item_bank.user = user
          user_item_bank.item_bank = item_bank
          user_item_bank.save()
          
          item_bank = ItemBank()
          item_bank.name = "Fractions"
          item_bank.topic = "Subtraction"
          item_bank.domain = domain
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
        item_bank.create_date = datetime.datetime(2012,03,06)
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
        
class TestUserItemBank(TestCase):
    def test_user_item_bank_link(self):
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
        item_bank = ItemBank()
        item_bank.name = "Fractions"
        item_bank.topic = "Subtraction"
        item_bank.domain = domain
        item_bank.create_date = datetime.datetime(2012,03,06)
        item_bank.save()
        user_item_bank = UserItemBank()
        user_item_bank.user = user
        user_item_bank.item_bank = item_bank
        user_item_bank.save()
        uibs = UserItemBank.objects.all()[0]
        self.assertEqual(uibs.item_bank,item_bank)
        self.assertEqual(uibs.user,user)         
        item_banks = ItemBank.objects.filter(useritembank__user=user)
        self.assertEqual(len(item_banks),1)         