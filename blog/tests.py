from django.test import TestCase, Client
from .models import Post
from .forms import BlogPostForm
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.urls import reverse
from django.http import HttpRequest
from . import views


# To run tests enter 'python3 manage.py test blog' in the terminal

class BlogViewsTests(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username='Test',
                                             email='test@domain.com',
                                             password='Testing')
        
        self.client.login(username='Test', password='Testing')
        
        self.post = Post.objects.create(user=self.user,
                                        title='Test post',
                                        content='This is a test blog post.',
                                        tag='Test',
                                        slug='test-post')
        self.post.save()
    
    def tearDown(self):
        pass
    
    def test_get_posts_page(self):
        
        response = self.client.get('/blog/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'blogposts.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Contribute to the conversation')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_post_detail_page(self):
        
        response = self.client.get('/blog/{0}/'.format(self.post.slug))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'postdetail.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Published on')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_create_or_edit_post_page(self):
        
        response = self.client.get('/blog//new/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'blogpostform.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Add a post below')
        self.assertNotContains(response, 'This should not be on the page')

class PostModelTests(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user(username='Test',
                                             email='test@domain.com',
                                             password='Testing')
        
        self.client.login(username='Test', password='Testing')
        
        self.post = Post(user=self.user,
                         title='Test Post',
                         content='This is a test post.')
        self.post.save()
        
    def tearDown(self):
        pass

    def test_post_model(self):
        

        """ Tests project instance is being stored in database """
        self.assertTrue(isinstance(self.post, Post))
        
        """ Tests project fields are logged correctly """
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        
        """ Tests default settings for views """
        self.assertEqual(self.post.views, 0)
        
        """ Tests model's create_slug function works """
        self.assertEqual(str(self.post.slug), 'test-post')

class BlogPostFormTests(TestCase):
    
    def test_blog_post_form_invalid(self):
        
        form = BlogPostForm({'title': '',
                             'content': ''})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], [u'This field is required.'])
        self.assertEqual(form.errors['content'], [u'This field is required.'])
    
    def test_blog_post_form_valid(self):
        
        form = BlogPostForm({'title': 'Test Post',
                             'content': 'This is a test post.'})
        
        """ Tests form can be submitted having filled all necessary fields """
        self.assertTrue(form.is_valid())