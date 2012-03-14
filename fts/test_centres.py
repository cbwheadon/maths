from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys
from item_banks.models import ItemBank, Domain
from centres.models import UserItemBank
from django.contrib.auth.models import User

class TestAdmin(FunctionalTest):

    def test_log_in_to_admin(self):
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
      return(self)
          
    def test_can_create_new_centre_via_admin_site(self):
      print("test_can_create_new_centre_via_admin_site")    
      #Admin logs in
      self.test_log_in_to_admin()
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
      print body.text
      
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
      print body.text
      
      #Set up two item banks and associate with user
      user = User.objects.get(username="JRotten") 
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