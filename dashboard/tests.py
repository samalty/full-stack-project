from django.test import TestCase, Client
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm, EditForm, ClientEditForm
import datetime
from django.utils import timezone
from django.urls import reverse
from django.http import HttpRequest
from . import views
from django.core.exceptions import ValidationError

# To run tests enter 'python3 manage.py test dashboard' in the terminal

class DashboardViewsTests(TestCase):

    def test_dashboard_page(self):
        
        user = User.objects.create_user(username='Test',
                                email='test@domain.com',
                                password='Testing')
        global user
        self.client.login(username='Test', password='Testing')
        
        response = self.client.get('/dashboard/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'user_dashboard.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'This is your dashboard')
        self.assertNotContains(response, 'This should not be on the page')

    def test_project_detail_page(self):
        
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
        
        response = self.client.get('/dashboard/{0}/'.format(project.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'project_detail.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'This is your project detail page')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_plan_project_page(self):
        
        user = User.objects.create_superuser(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        project = Project.objects.create(project_title='Test Project',
                                         description='This is a test project.',
                                         client=user,
                                         fee=750.00,
                                         deadline=datetime.date.today()+datetime.timedelta(days=10))
        project.save()
        
        response = self.client.get('/dashboard/plan_project/')
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'plan_project.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Just agreed on a new project with a client')
        self.assertNotContains(response, 'This should not be on the page')
    
    def test_edit_page(self):
        
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
        
        response = self.client.get('/dashboard/{0}/edit/'.format(project.pk))
        
        """ Tests response status code """
        self.assertEqual(response.status_code, 200)
        
        """ Tests correct template is used """
        self.assertTemplateUsed(response, 'edit.html')
        
        """ Tests page contains correct html """
        self.assertContains(response, 'Project plan still requires some fine tuning')
        self.assertNotContains(response, 'This should not be on the page')
        
class ProjectModelTests(TestCase):
    
    def test_project_model(self):
        
        user = User.objects.create_user(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        project = Project(project_title='Test Project',
                          description='This is a test project.',
                          client=user,
                          fee=750.00,
                          deadline=datetime.date.today()+datetime.timedelta(days=10))
        project.save()
        
        """ Tests project instance is being stored in database """
        self.assertTrue(isinstance(project, Project))
        
        """ Tests project fields are logged correctly """
        self.assertEqual(project.project_title, 'Test Project')
        self.assertEqual(project.description, 'This is a test project.')
        
        """ Tests default settings for approved, signed_off and paid fields """
        self.assertFalse(project.approved)
        self.assertFalse(project.signed_off)
        self.assertFalse(project.paid)
        
        """ Tests default settings for task1_status and project_status fields """
        self.assertEqual(project.task1_status, 'To Do')
        self.assertEqual(project.project_status, 'To Do')

    def test_deadline_seven_days_in_advance(self):
        
        time1 = timezone.now() + datetime.timedelta(days=3)
        new_project1 = Project(deadline=time1)
        
        time2 = timezone.now() + datetime.timedelta(days=10)
        new_project2 = Project(deadline=time2)
        
        """ Tests method to ensure deadlines aren't set within 10 days is functional """
        self.assertIs(new_project1.seven_days_advance(), False)
        self.assertIs(new_project2.seven_days_advance(), True)
    
#    def test_insufficient_notice_returns_validation_error(self):
        
        """ Tests that deadlines set within a week return validation error """
        #with self.assertRaises(ValidationError):
        #    deadline_validation_error(3)
        
#        self.assertRaises(ValidationError, deadline_validation_error, 3)
    
    def test_calculate_vat(self):
        
        new_project = Project(fee=840.00)
        
        """ Tests calculate vat function works """
        self.assertEqual(new_project.calculate_vat(), 168.00)
    
    def test_project_status_based_on_other_variables(self):
        
        project1 = Project(signed_off=False, task1_status='To Do')
        project2 = Project(signed_off=False, task1_status='Done')
        project3 = Project(signed_off=True)
        
        """ Tests project status is correct, based on status of other fields """
        self.assertEqual(project1.decide_project_status(), 'To Do')
        self.assertEqual(project2.decide_project_status(), 'Doing')
        self.assertEqual(project3.decide_project_status(), 'Done')

    def test_task_status_with_empty_task_field(self):
        
        project = Project(task2='Second task')
        
        """ Tests task status defaults to 'To Do' when corresponding task field is used """
        self.assertEqual(project.update_task_status(), 'To Do')
        self.assertFalse(project.task2_status == '')

class ProjectFormTests(TestCase):
    
    def test_project_form_invalid(self):
        
        form = ProjectForm({'project_title': 'Test Project',
                            'description': 'This is a test project'})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['client'], [u'This field is required.'])
        self.assertEqual(form.errors['fee'], [u'This field is required.'])
        self.assertEqual(form.errors['deadline'], [u'This field is required.'])
        self.assertEqual(form.errors['priority'], [u'This field is required.'])
        self.assertEqual(form.errors['task1'], [u'This field is required.'])
        self.assertEqual(form.errors['task1_status'], [u'This field is required.'])
    
    def test_project_form_valid(self):
    
        user = User.objects.create_user(username='Test',
                                 email='test@domain.com',
                                 password='Testing')
        self.client.login(username='Test', password='Testing')
        
        form = ProjectForm({'project_title': 'Test Project',
                            'description': 'This is a test project.',
                            'client': '1',
                            'fee': '750.00',
                            'deadline': '2018-12-12',
                            'priority': 'High',
                            'task1': 'First task',
                            'task1_status': 'To Do'})
        
        """ Tests form can be submitted having filled all necessary fields """
        self.assertTrue(form.is_valid())
    
    def test_edit_form_invalid(self):
        
        form = EditForm({'description': '',
                         'fee': '',
                         'deadline': '',
                         'priority': '',
                         'task1': ''})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], [u'This field is required.'])
        self.assertEqual(form.errors['fee'], [u'This field is required.'])
        self.assertEqual(form.errors['deadline'], [u'This field is required.'])
        self.assertEqual(form.errors['priority'], [u'This field is required.'])
        self.assertEqual(form.errors['task1'], [u'This field is required.'])
    
    def test_edit_form_valid(self):
        
        form = EditForm({'description': 'This is a test project',
                         'fee': '750.00',
                         'deadline': '2018-12-12',
                         'priority': 'High',
                         'task1': 'First task'})
        
        """ Tests form can be submitted having filled all necessary fields """
        self.assertTrue(form.is_valid())
    
    def test_client_edit_form_invalid(self):
        
        form = ClientEditForm({'description': '',
                               'deadline': '',
                               'task1': ''})
        
        """ Tests form can't be submitted without filling all necessary fields """
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['description'], [u'This field is required.'])
        self.assertEqual(form.errors['deadline'], [u'This field is required.'])
        self.assertEqual(form.errors['task1'], [u'This field is required.'])
    
    def test_client_edit_form_valid(self):
        
        form = ClientEditForm({'description': 'This is a test project',
                               'deadline': '2018-12-12',
                               'task1': 'First task'})
        
        """ Tests form can be submitted having filled all necessary fields """
        self.assertTrue(form.is_valid())