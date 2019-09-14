from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 10
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return

            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)



    def test_can_start_a_list_and_retrieve_it_later(self):

        self.browser.get(self.live_server_url)


        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        time.sleep(2)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )


        inputbox.send_keys('购买孔雀毛')

        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1:购买孔雀毛')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀毛做蝇拍')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2:使用孔雀毛做蝇拍')
        self.wait_for_row_in_list_table('1:购买孔雀毛')


        # self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # 伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('购买孔雀毛')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:购买孔雀毛')

        # 伊迪丝清单的唯一url
        edith_list_url = self.browser.current_url
        print('***',edith_list_url)
        self.assertRegex(edith_list_url, '/lists/.+')


        # 新用户 弗朗西斯访问了网站
        ## 我们使用给一个新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀毛',page_text)
        self.assertNotIn('飞翔',page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('买牛奶')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:买牛奶')

        # 弗朗西斯获得他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买孔雀毛',page_text)
        self.assertIn('买牛奶',page_text)


    def test_layout_and_styling(self):

        # 伊迪丝访问主页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        # 她看到输入框完美的居中显示
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            # delta=10

        )












