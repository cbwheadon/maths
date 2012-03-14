from functional_tests import FunctionalTest, ROOT
from selenium.webdriver.common.keys import Keys

class TestLogIn(FunctionalTest):

    def test_no_log_in_to_welcome(self):
      # Gertrude opens her web browser, and goes straight to the welcome page
      self.browser.get(ROOT + '/welcome/')
      #Should be redirected to login page
      body = self.browser.find_element_by_tag_name('body')
      self.assertIn('Username', body.text)  