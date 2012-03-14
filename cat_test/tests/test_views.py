from django.test import TestCase
from functional_tests import ROOT
from django.contrib.auth.models import User
from item_banks.models import ItemBank, Domain, ItemBankQuestion
from centres.models import UserItemBank
from cat_test.models import CatTest

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
          response = self.client.post('/start/', {'item_bank_id': item_bank.id, 'cat_test_id':cat_test.id})
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
          

        def test_start_test_wout_login_view(self):
          response = self.client.get('/start/')
          self.assertEqual(response.status_code, 302)          