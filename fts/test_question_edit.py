from functional_tests import FunctionalTest, ROOT
from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys
from item_banks.models import ItemBank, Domain, QuestionType, ItemBankTemplate, ItemBankFractionQuestion
from cat_test.models import CatTestItem, UserCatTest
from centres.models import UserItemBank
from fractionqs.models import FractionQuestionBank, Oper
from django.contrib.auth.models import User

class TestQuestion(FunctionalTest):

    def test_can_edit_question_via_admin_site(self):
      #Set up an item bank and associate with user
      domain = Domain.objects.get(name="Number")
      item_bank = ItemBank()
      item_bank.name = "Fractions"
      item_bank.topic = "Addition"
      item_bank.domain = domain
      item_bank.template = ItemBankTemplate.objects.get(pk=1)
      item_bank.question_type = QuestionType.objects.get(pk=1)
      item_bank.save()
      
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
      
      #Admin logs in
      # Gertrude opens her web browser, and goes to the admin page
      self.browser.get(ROOT + '/admin/')

      # She sees the familiar 'Django administration' heading
      body = self.browser.find_element_by_tag_name('body')
      
      # She types in her username and passwords and hits return
      username_field = self.browser.find_element_by_name('username')
      username_field.send_keys('admin')

      password_field = self.browser.find_element_by_name('password')
      password_field.send_keys('adm1n')
      password_field.send_keys(Keys.RETURN)
      #print out what you see
      body = self.browser.find_element_by_tag_name('body')
      #She sees a hyperlink that says "Centres"
      links = self.browser.find_elements_by_link_text('Item bank questions')
      self.assertEquals(len(links), 1)
      #Clicks it
      links[0].click()
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('/', body.text)