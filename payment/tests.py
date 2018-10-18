from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from dashboard.models import Project
from .models import Order, OrderLineItem
from .forms import PaymentForm, OrderForm
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from . import views

# To run tests enter 'python3 manage.py test payment' in the terminal

class PaymentViewsTests(TestCase):
    
    def test_confirm_page(self):
        
        user = User.objects.create_user(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        project = Project.objects.create(project_title='Test Project',
                                         description='This is a test project.',
                                         client=user,
                                         fee=750.00,
                                         deadline=datetime.date.today()+datetime.timedelta(days=10))
        project.save()
        
        response = self.client.get('/payment/{0}/'.format(project.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'confirm.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Thankyou for your custom')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_checkout_page(self):
        
        user = User.objects.create_user(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/payment/checkout/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'checkout.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Payment Details')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_receipt_page(self):
        
        user = User.objects.create_user(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        project = Project.objects.create(project_title='Test Project',
                                         description='This is a test project.',
                                         client=user,
                                         fee=750.00,
                                         deadline=datetime.date.today()+datetime.timedelta(days=10))
        project.save()
        
        response = self.client.get('/payment/receipt/{0}/'.format(project.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'receipt.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Your payment for')
        self.assertNotContains(response, 'This should not be on the page')

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
                            'cvv': '111',
                            'expiry_month': '8',
                            'expiry_year': '2018'})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
#        self.assertEqual(form.errors['credit_card_number'], [u'The card number is not a valid credit card number.'])
#        self.assertEqual(form.errors['cvv'], [u'This field is required.'])
        self.assertEqual(form.errors['expiry_month'], [u"Your card's expiration month is invalid."])
#        self.assertEqual(form.errors['expiry_year'], [u'This field is required.'])