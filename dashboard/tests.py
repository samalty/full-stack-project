from django.test import TestCase
from .models import Project

# Create your tests here.

class ProjectTests(TestCase):
    def test_str(self):
        test_title = Project(project_title='Project 1')
        self.assertEqual(str(test_title), 'Project 1')