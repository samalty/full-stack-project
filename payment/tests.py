from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from dashboard.models import Project
from .models import Order, OrderLineItem
from .forms import PaymentForm, OrderForm
from django.contrib.auth.models import User
import datetime
import os
from django.utils import timezone
from . import views

# To run tests enter 'python3 manage.py test payment' in the terminal

class PaymentViewsTests(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username='Test',
                                             email='test@domain.com',
                                             password='Testing')
        
        self.client.login(username='Test', password='Testing')
        
        self.project = Project.objects.create(project_title='Test Project',
                                              description='This is a test project.',
                                              client=self.user,
                                              fee=750.00,
                                              deadline=datetime.date.today()+datetime.timedelta(days=10))
        self.project.save()
    
    def tearDown(self):
        pass

    def test_confirm_page(self):
        
        response = self.client.get('/payment/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'confirm.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Thank you for your custom')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_checkout_page(self):
        
        response = self.client.get('/payment/checkout/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'checkout.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Payment Details')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_receipt_page(self):
        
        response = self.client.get('/payment/receipt/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'receipt.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Your payment has been successfully processed')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_confirm_payment_function(self):
        
        response = self.client.get('/payment/confirm/{0}/'.format(self.project.id))
        
        """ Tests calling on function results in redirect """
        self.assertEqual(response.status_code, 302)

class OrderModelTests(TestCase):
    
    def test_order_model(self):
        
        user = User.objects.create_user(username='Test',
                                        email='test@domain.com',
                                        password='Testing')
        self.client.login(username='Test', password='Testing')
        
        order = Order(company_name='Test Co',
                      date=datetime.date.today(),
                      town_or_city='Testerton',
                      street_address1='7 Test Close',
                      county='Testshire',
                      postcode='TE5T 1NG')
        
        """ Tests order instance is being stored in database """
        self.assertTrue(isinstance(order, Order))
        
        """ Tests order fields are logged correctly """
        self.assertEqual(order.company_name, 'Test Co')
        self.assertEqual(order.town_or_city, 'Testerton')
        
        """ Tests default settings for date field """
        self.assertEqual(order.date, datetime.date.today())
        
    def test_order_line_item_model(self):
        
        user = User.objects.create_user(username='Test',
                                        email='test@domain.com',
                                        password='Testing')
        self.client.login(username='Test', password='Testing')
        
        test_project = Project.objects.create(project_title='Test Project',
                                              description='This is a test project.',
                                              client=user,
                                              fee=750.00,
                                              deadline=datetime.date.today()+datetime.timedelta(days=10))
                                         
        test_order = Order(company_name='Test Co',
                           date=datetime.date.today(),
                           town_or_city='Testerton',
                           street_address1='7 Test Close',
                           county='Testshire',
                           postcode='TE5T 1NG')
        
        orderlineitem = OrderLineItem(order=test_order,
                                      project=test_project)
        
        """ Tests orderlineitem instance is being stored in database """
        self.assertTrue(isinstance(orderlineitem, OrderLineItem))
        
        """ Tests string returned by orderlineitem is correct """
        self.assertEqual(str(orderlineitem), 'Test Project-750.0')

class PaymentOrderFormTests(TestCase):
    
    def test_payment_form_invalid(self):
        
        form = PaymentForm({'credit_card_number': '4242424242424242',
                            'cvv': '',
                            'expiry_month': '10',
                            'expiry_year': '2020'})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['stripe_id'], [u'This field is required.'])
    
    def test_payment_form_valid(self):
        
        form = PaymentForm({'credit_card_number': '4242424242424242',
                            'cvv': '111',
                            'expiry_month': '10',
                            'expiry_year': '2020',
                            'stripe_id': os.getenv('STRIPE_SECRET')})
        
        """ Tests form submits when all necessary fields are completed """
        #self.assertTrue(form.is_valid())
    
    def test_order_form_invalid(self):
        
        form = OrderForm({'company_name': '',
                          'town_or_city': 'Testerton',
                          'street_address1': '',
                          'county': 'Testshire',
                          'country': 'UK',
                          'postcode': ''})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['company_name'], [u'This field is required.'])
        self.assertEqual(form.errors['street_address1'], [u'This field is required.'])
        self.assertEqual(form.errors['postcode'], [u'This field is required.'])
    
    def test_order_form_valid(self):
        
        form = OrderForm({'company_name': 'Test Co',
                          'town_or_city': 'Testerton',
                          'street_address1': '7 Test Close',
                          'county': 'Testshire',
                          'country': 'UK',
                          'postcode': 'TE5T 1NG'})
        
        """ Tests form submits when all necessary fields are completed """
        self.assertTrue(form.is_valid())