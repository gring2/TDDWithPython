from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from lists.models import Item
# Create your tests here.


class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 +1 , 2)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        resp = self.client.get('/')
        html = resp.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(resp, 'home.html')

    def test_uses_home_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'home.html')

    def test_can_save_a_POST_request(self):
        resp = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        resp = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['location'], '/')

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        resp = self.client.get('/')
        self.assertIn('itemey 1', resp.content.decode())
        self.assertIn('itemey 2', resp.content.decode())