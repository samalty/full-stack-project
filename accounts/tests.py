from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post
from . import views
from .forms import EditProfileForm, UserRegistrationForm, UserLoginForm
from .models import UserProfile

# To run tests enter 'python3 manage.py test accounts' in the terminal

class AccountsViewsTests(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username='Test',
                                        email='test@domain.com',
                                        password='Testing')
        
        self.post = Post.objects.create(user=self.user,
                                        title='Test post',
                                        content='This is a test blog post.',
                                        tag='Test',
                                        slug='test-post')
        self.post.save()
        
    def tearDown(self):
        pass
    
    def test_index_page(self):
        
        response = self.client.get('/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'index.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Welcome')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_login_page(self):
        
        response = self.client.get('/accounts/login/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'login.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Login below to see how your project is progressing')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_profile_page(self):
        
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/accounts/{0}/'.format(self.user.pk))
        
        """ Tests instance of user has been created """
        self.assertEqual(User.objects.count(), 1)
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'profile.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'test@domain.com')
        self.assertNotContains(response, 'This should not be on the page')
        
    def test_edit_profile_page(self):
        
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/accounts/{0}/edit/'.format(self.user.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'edit_profile.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Edit your profile below')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_update_image_page(self):
        
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/accounts/{0}/update_image/'.format(self.user.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'update_image.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Update your profile image below')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_display_profile_page(self):
        
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/accounts/{0}/author/'.format(self.post.slug))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'display_profile.html')
        
        """ Tests page contains correct html """
        self.assertNotContains(response, 'This should not be on the page')

class UserProfileModelTests(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username='Test',
                                        email='test@domain.com',
                                        password='Testing')
                                        
        self.client.login(username='Test', password='Testing')
        
        self.profile = UserProfile(user=self.user,
                              bio='This is a test bio.',
                              location='Coventry, UK',
                              website='https://www.test.com')
        
    def tearDown(self):
        pass
    
    def test_user_profile_model(self):
        
        """ Tests project instance is being stored in database """
        self.assertTrue(isinstance(self.profile, UserProfile))
        
        """ Tests project fields are logged correctly """
        self.assertEqual(self.profile.bio, 'This is a test bio.')
        self.assertEqual(self.profile.location, 'Coventry, UK')
        
        """ Tests default image for new users """
        self.assertEqual(str(self.profile.image), 'profile_img/anon.png')
    
    def test_profile_function_for_new_users(self):
                                 
        profile_exists = UserProfile.objects.filter(user=self.user).exists()
        
        """ Test to ensure profile instances are automatically created for new users """
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertTrue(profile_exists)

class AccountsFormsTests(TestCase):
    
    def test_user_registration_form_valid(self):
        
        form = UserRegistrationForm({'username': 'Test',
                                     'email': 'email@test.com',
                                     'password1': 'testing',
                                     'password2': 'testing'})
        
        """ Tests valid user registration form entry is recognised """
        self.assertTrue(form.is_valid())
    
    def test_user_registration_form_invalid(self):
        
        form = UserRegistrationForm({'username': 'Test',
                                     'email': 'emailtest.com',
                                     'password1': 'testing1',
                                     'password2': 'testing2'})
        
        """ Tests invalid user registration form entry is recognised """
        self.assertFalse(form.is_valid())
        
        """ Tests invalid field entries result in error messages """
        self.assertEqual(form.errors['email'], [u'Enter a valid email address.'])
        self.assertEqual(form.errors['password2'], [u'Passwords do not match'])
    
    def test_user_registration_form_missing_input(self):
        
        form = UserRegistrationForm({'username': '',
                                     'email': 'emailtest.com',
                                     'password1': 'testing1',
                                     'password2': ''})
        
        """ Tests registration form entry with missing input is recognised """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
        self.assertEqual(form.errors['password2'], [u'This field is required.'])

    def test_user_login_form_valid(self):
        
        form = UserLoginForm({'username': 'Test',
                              'password': 'Testing'})
        
        """ Tests valid user login form entry is recognised """
        self.assertTrue(form.is_valid())

    def test_user_login_form_missing_input(self):
        
        form = UserLoginForm({'username': '',
                              'password': ''})
        
        """ Tests invalid user registration form entry is recognised """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
        self.assertEqual(form.errors['password'], [u'This field is required.'])

    def test_edit_profile_form_valid(self):
        
        form = EditProfileForm({'bio':'This is a test bio', 
                                'location':'Coventry, UK', 
                                'website':'www.test.com'})
                                
        """ Tests user profile can be updated using form """
        self.assertTrue(form.is_valid())