from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category,Product
from unittest import skip
from django.test import Client       # we can simulate a client 
from django.urls import reverse
# Create your tests here.
from store.views import all_products ,category_list
from django.http import HttpRequest



##### Testing Views


#testing homepage 
#we simulate a client which try to access our homepage using the Client Class


class TestViewResponses(TestCase):
	def setUp(self):
		self.c=Client()
		User.objects.create(username='admin')
		Category.objects.create(name='django', slug='django')
		Product.objects.create(category_id=1, title='django beginners', created_by_id=1,slug='django-beginners', price='20.00', image='django')

	def test_homepage_url(self):
		response=self.c.get('/')
		self.assertEqual(response.status_code,200)
	def test_product_detail_url(self):
		response=self.c.get(reverse('store:product_detail',args=['django-beginners']))

		self.assertEqual(response.status_code,200)
	def test_product_detail_url_bad(self):
		response=self.c.get(reverse('store:product_detail',args=['node-beginners']))
		self.assertNotEqual(response.status_code,200)


	def test_category_detail_url(self):
		response=self.c.get(reverse('store:category_list',args=['django']))

		self.assertEqual(response.status_code,200)
	def test_category_detail_url_bad(self):
		response=self.c.get(reverse('store:category_list',args=['rango']))
		self.assertNotEqual(response.status_code,200)


	def test_homepage_html(self):
		request=HttpRequest()
		response=all_products(request)
		html=response.content.decode('utf8')
		self.assertIn('<title>Home</title>',html)
		self.assertEqual(response.status_code,200)


	def test_categorylist_html(self):
		request=HttpRequest()
		response=category_list(request,'django')
		html=response.content.decode('utf8')
		self.assertEqual(response.status_code,200)