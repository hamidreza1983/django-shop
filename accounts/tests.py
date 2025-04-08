from django.test import TestCase
from accounts.models import User
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
User = get_user_model()

class LoginViewTestCase(TestCase):
    # این تابع به ازای هر تست اتوماتیک صدا زده میشود

    def setUp(self):
        """ برای هر تست یک کاربر میسازیم """
        self.user = User.objects.create_user(
            email='test@example.com',
            password='J@midreza62'
        )
        self.url = reverse_lazy('accounts:login')  # باید URL مناسب برای ورود رو قرار بدی

    # بررسی اینکه به ازای درخواست گت آدرس تمپلیت درستی رندر میشود یا نه
    def test_template_login(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'registrations/login.html')
    # بررسی اینکه در ازای گت آیا استتوس کد 200 است یا دستکاری شده
    def test_template_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code , 200)
    # بررسی اینکه آیا اگر به این ویو درخواست درستی ارسال شود به صفحه باز میگردد یا نه
    def test_login_valid(self):
        """ تست موفقیت ورود به سیستم """
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'J@midreza62',
        })

        # بررسی که کاربر هدایت شده به صفحه خانه شده
        self.assertRedirects(response, reverse_lazy('root:home'))
        # بررسی که پیغام موفقیت آمیز در messages وجود داره
        messages = [m.message for m in response.wsgi_request._messages]
        self.assertIn('ورود موفقیت آمیز', messages)

    def test_login_invalid_credentials(self):
        """ تست ورود با ایمیل یا پسورد اشتباه """
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        })

        # بررسی که کاربر هنوز در صفحه ورود باقی می‌مونه (نیاز به ریدایرکت نداره)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        messages = [m.message for m in response.wsgi_request._messages]
        self.assertIn('کلمه کاربری یا پسورد اشتباه است', messages)

    def test_login_invalid_data(self):
        """ تست ارسال داده‌های نامعتبر """
        response = self.client.post(self.url, {
            'email': '',
            'password': '',
        })

        # بررسی که دوباره به صفحه ورود هدایت شده
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)
        messages = [m.message for m in response.wsgi_request._messages]
        self.assertIn('داده های ورودی نامعتبر میباشد', messages)



class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='H@midreza62'
        )
        self.client.login(email='test@example.com', password='H@midreza62')  # لاگین کاربر

    def test_logout_view(self):
        """کاربر لاگین‌شده باید بعد از logout ریدایرکت و غیرفعال شود"""
        response = self.client.get(reverse('accounts:logout'))  # فرض بر اینه که URL با نام logout تعریف شده

        # چک اینکه کاربر ریدایرکت شده به صفحه اصلی
        self.assertRedirects(response, "/")

        # چک اینکه کاربر دیگه لاگین نیست
        self.assertFalse('_auth_user_id' in self.client.session)

        # چک وجود پیام موفقیت در پیام‌ها
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'خروج از حساب کاربری با موفقیت انجام شد')



