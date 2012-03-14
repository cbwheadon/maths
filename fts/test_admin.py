from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys
from maths.item_banks.models import Domain
import datetime

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
      self.assertIn('60114 Test Centre', body.text)  