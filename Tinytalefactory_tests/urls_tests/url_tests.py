from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.core import mail


UserModel = get_user_model()


class UrlTests(TestCase):

    def setUp(self):

        self.user = {
            'username': 'testuser',
            'email': 'testemail@tinytalefactory.com',
            'password': 'testpassword321',
        }

    def _create_user(self):
        return UserModel.objects.create_user(**self.user)

    def test__signup_url__expect_response_code_200(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__signup_url__expect_template_used_to_be_signup_html(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test__login_url__expect_response_code_200(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__login_url__expect_template_used_to_be_login_html(self):
        url = reverse('account_login')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'account/login.html')

    def test__account_email_url_when_not_logged_in__expect_response_code_302_redirect_to_login(self):
        url = reverse('account_email')
        response = self.client.get(url)

        expected_url = reverse('account_login') + f'?next={reverse("account_email")}'

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test__account_password_reset_when_not_logged_in__expect_response_code_200_template_used_password_reset_html(self):
        url = reverse('account_reset_password')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'account/password_reset.html')
        self.assertEqual(response.status_code, 200)

    def test__account_password_reset_POST_correct_email_details__expect_response_code_302_redirect_send_email(self):

        url = reverse('account_reset_password')
        data = {'email': self.user['email']}

        emails_send_before = len(mail.outbox)

        response = self.client.post(url, data)

        emails_send_after = len(mail.outbox)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(emails_send_before + 1, emails_send_after)

    def test__account_password_reset_POST_wrong_email_details__expect_response_code_200_template_used_password_reset_html(self):

        url = reverse('account_reset_password')
        data = {'email': 'novalidemail.com'}

        response = self.client.post(url, data)
        a = 1
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_reset.html')

    def test__profile_url_when_not_logged_in__expect_response_code_302_redirect_to_login(self):

        url = reverse('profile-page')
        response = self.client.get(url)

        expected_url = reverse('account_login') + f'?next={reverse("profile-page")}'

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_url)

    def test__profile_url_when_logged_in__expect_response_code_200_template_used_profile_html(self):

        self._create_user()
        login_user = self.client.login(username=self.user['username'], password=self.user['password'])

        url = reverse('profile-page')
        response = self.client.get(url)

        self.assertTrue(login_user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile.html')

    # TODO: Create URL tests for the rest of the URL's to ensure that URL's are created correctly and are reachable
