from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys
from item_banks.models import ItemBank, Domain, QuestionType, ItemBankTemplate, ItemBankFractionQuestion, Grade, Threshold
from cat_test.models import CatTestItem, UserCatTest
from centres.models import UserItemBank
from fractionqs.models import FractionQuestionBank, Oper
from django.contrib.auth.models import User

class TestAdmin(FunctionalTest):

    #def test_log_in_to_admin(self):
      # Gertrude opens her web browser, and goes to the admin page
      #self.browser.get(ROOT + '/admin/')

      # She sees the familiar 'Django administration' heading
      #body = self.browser.find_element_by_tag_name('body')
      #self.assertIn('Django administration', body.text)
      
      # She types in her username and passwords and hits return
      #username_field = self.browser.find_element_by_name('username')
      #username_field.send_keys('admin')

      #password_field = self.browser.find_element_by_name('password')
      #password_field.send_keys('adm1n')
      #password_field.send_keys(Keys.RETURN)
      #print out what you see
      #body = self.browser.find_element_by_tag_name('body')
      #self.assertIn('Welcome', body.text)
      #return(self)
          
    def test_can_create_new_centre_via_admin_site(self):
      print("test_can_create_new_centre_via_admin_site")    
      #Admin logs in
      # Gertrude opens her web browser, and goes to the admin page
      self.browser.get(ROOT + '/admin/')

      # She sees the familiar 'Django administration' heading
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Django administration', body.text)
      
      # She types in her username and passwords and hits return
      username_field = self.browser.find_element_by_name('username')
      username_field.send_keys('admin')

      password_field = self.browser.find_element_by_name('password')
      password_field.send_keys('adm1n')
      password_field.send_keys(Keys.RETURN)
      #print out what you see
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Welcome', body.text)
      #She sees a hyperlink that says "Centres"
      links = self.browser.find_elements_by_link_text('Centres')
      self.assertEquals(len(links), 2)
      #Clicks it
      links[1].click()
      #Selects add link
      add_link = self.browser.find_elements_by_link_text('Add centre')
      add_link[0].click()
      #Fill in name, centre_id and create date and hit submit
      name_field = self.browser.find_element_by_name('name')
      name_field.send_keys('Test Centre')
      centre_id_field = self.browser.find_element_by_name('centre_id')
      centre_id_field.send_keys('60114') 
      date_field = self.browser.find_element_by_name('create_date_0')
      date_field.send_keys('2012-03-05')
      time_field = self.browser.find_element_by_name('create_date_1')
      time_field.send_keys('10:25:12')
      date_field.send_keys(Keys.RETURN)
      #Centre is saved and centre_id and name is displayed
      body = self.browser.find_element_by_tag_name('body')
      #returns to home page
      self.assertIn('60114 Test Centre', body.text)
      links = self.browser.find_elements_by_link_text('Home')
      links[0].click()
      #Clicks on user
      links = self.browser.find_elements_by_link_text('Users')
      links[0].click()
      
      #Clicks on Add user
      links = self.browser.find_elements_by_link_text('Add user')
      links[0].click()
      name_field = self.browser.find_element_by_name('username')
      name_field.send_keys('JRotten')
      name_field = self.browser.find_element_by_name('password1')
      name_field.send_keys('password')
      name_field = self.browser.find_element_by_name('password2')
      name_field.send_keys('password')
      name_field.send_keys(Keys.RETURN)
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('The user "JRotten" was added successfully', body.text)
      
      name_field = self.browser.find_element_by_name('first_name')
      name_field.send_keys('Johnny')
      name_field = self.browser.find_element_by_name('last_name')
      name_field.send_keys('Rotten')
      name_field.send_keys(Keys.RETURN)
      links = self.browser.find_elements_by_link_text('Home')
      links[0].click()
      
      #She sees a hyperlink that says "Candidates"
      links = self.browser.find_elements_by_link_text('Candidates')
      self.assertEquals(len(links), 1)
      #Clicks it
      links[0].click()
      #Selects add link
      body = self.browser.find_element_by_tag_name('body')
      
      add_link = self.browser.find_elements_by_link_text('Add candidate')
      add_link[0].click()
      #Fill in gender, dob, centre, user and hit submit
      name_field = self.browser.find_element_by_name('gender')
      name_field.send_keys('M')
      dob_field = self.browser.find_element_by_name('dob')
      dob_field.send_keys('1969-05-01')
      
      select = self.browser.find_elements_by_tag_name("select")
      allOptions = select[0].find_elements_by_tag_name("option")   
      for option in allOptions:
        print "Value is: " + option.get_attribute("value")
        option.click()
      
      allOptions = select[1].find_elements_by_tag_name("option")   
      for option in allOptions:
        print "Value is: " + option.get_attribute("value")
        option.click()
        
      dob_field.send_keys(Keys.RETURN)
      #Candidate is saved and name is displayed
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('The candidate "Johnny Rotten" was added successfully.', body.text)
      
      #Set up an item bank and associate with user
      user = User.objects.get(username="JRotten") 
      domain = Domain.objects.get(name="Number")
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
      
      #Set up thresholds
      #add threshold
      grd = Grade.objects.get(name="C")
      thresh = Threshold()
      thresh.grade = grd
      thresh.item_bank = item_bank
      thresh.ability = 0      
      thresh.save()
      #add user probabilities
      user_item_bank.probabilities()   
      
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
          
      #Candidate logs in and is directed to welcome page
      self.browser.get(ROOT + '/accounts/login/')
      name_field = self.browser.find_element_by_name('username')
      name_field.send_keys('JRotten')
      dob_field = self.browser.find_element_by_name('password')
      dob_field.send_keys('password')
      name_field.send_keys(Keys.RETURN)
      
      #Candidate should now see a list of available item banks grouped into domains
      #Number - Fractions - Addition - Questions Answered - Ability - Last Access - Time
      #Each should be associated with three actions:
      #Start - Review - Reset
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Welcome', body.text)
      self.assertIn('Number',  body.text)
      self.assertIn('Fractions',  body.text)
      self.assertIn('Addition',  body.text)
      self.assertIn('50%',  body.text)
      
      #Candidate clicks on link to start test
      links = self.browser.find_elements_by_link_text('Short Test')
      links[0].click()
      
      #Should see start test screen
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Fractions',body.text)
      self.assertIn('Addition',body.text)
      self.assertIn('Short Test',body.text)
      self.assertIn('4', body.text)
      
      #Clicks on link to start test
      links = self.browser.find_elements_by_link_text('Start the test')
      links[0].click()
      
      body = self.browser.find_element_by_tag_name('body')
      #Should be taken to first question
      self.assertIn('Work out', body.text)
      
      #Enters answer and hits submit
      const_field = self.browser.find_element_by_name('const')
      const_field.send_keys('9')

      num_field = self.browser.find_element_by_name('num')
      num_field.send_keys('7')

      denom_field = self.browser.find_element_by_name('denom')
      denom_field.send_keys('8')

      denom_field.send_keys(Keys.RETURN)
      
      #Should see feedback that answer is wrong
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Wrong!', body.text)
      self.assertIn('9', body.text)
      self.assertIn('7', body.text)
      self.assertIn('8', body.text)
      
      #Clicks next
      links = self.browser.find_elements_by_link_text('Next')
      links[0].click()
      
      #Get second item
      
      user_cat_test = UserCatTest.objects.filter(user=user)
      user_cat_test = user_cat_test.order_by('-id')[0]
      cat_test_item = CatTestItem.objects.filter(user_cat_test=user_cat_test)
      cat_test_item = cat_test_item.order_by('-id')[0]
      ibq = cat_test_item.item_bank_question
      
      ifq = ItemBankFractionQuestion.objects.get(item_bank_question=ibq)
      ans = ifq.fraction_bank_question.question.answer
      
      #Enters correct answer and hits submit
      const_field = self.browser.find_element_by_name('const')
      const_field.send_keys(ans.const)

      num_field = self.browser.find_element_by_name('num')
      num_field.send_keys(ans.num)

      denom_field = self.browser.find_element_by_name('denom')
      denom_field.send_keys(ans.denom)

      denom_field.send_keys(Keys.RETURN)
      
      #Should see correct
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Correct!', body.text)
            
      #Clicks next
      links = self.browser.find_elements_by_link_text('Next')
      links[0].click()
      
      #Question 3
      denom_field = self.browser.find_element_by_name('denom')
      denom_field.send_keys(Keys.RETURN)
      
      #Doesn't answer, clicks next
      links = self.browser.find_elements_by_link_text('Next')
      links[0].click()
      
      #Question 4
      denom_field = self.browser.find_element_by_name('denom')
      denom_field.send_keys(Keys.RETURN)
      
      #Doesn't answer, clicks next
      links = self.browser.find_elements_by_link_text('End')
      links[0].click()
      
      #Should see end
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('End', body.text)
      
      #Clicks end
      links = self.browser.find_elements_by_link_text('Return')
      links[0].click()
      
      #Should see performance on item bank updated
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('-2.318', body.text)
      self.assertIn('4', body.text)
      self.assertIn('2%', body.text)