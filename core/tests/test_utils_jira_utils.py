from django.test import Client
from django.test.testcases import SimpleTestCase, TestCase
from django.urls import reverse


class TestUrls(TestCase):
    client = Client()
    user = {
        'username': 'apon@strativ.se',
        # 'password': 'Apon1234'
        'password': 'pbkdf2_sha256$150000$7i0Mi8EjeSNx$BjjrSnMefRKvJJEkvBFJIGC6yqVMTpfWbdihm2zWd/A='
    }

    def test_get_issue_project_by_key(self):
        login = self.client.login(username=self.user.get('username'), password=self.user.get('password'))
        print('login response - {}'.format(str(login)))
        response = self.client.get(reverse('core:logged_jira_hour'))
        print(response)
        self.assertEquals(response.status_code, 200)

    def test_append_jql_param(self):
        self.assertEquals(1, 1)
