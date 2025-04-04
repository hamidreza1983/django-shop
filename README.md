# 🚀 Django + Docker + PostgreSQL Online Shop

یک پروژه حرفه ای فروشگاه آنلاین با جنگو ، جاوااسکریپت و قالب بوت استرپ

---

## ✨ ویژگی‌ها
- استفاده از **Docker** برای مدیریت سرویس‌ها
- پایگاه داده **PostgreSQL**
- یک پایگاه داده تست جهت بررسی شما در کنار پروژه قرار دارد
- به راحتی بخش محصولات و مرچنت خود را برای سبد خرید اضافه کنید و لذت ببرید
- بهترین روش های فیلترینگ بر اساس بازه قیمت و کتگوری و موارد دارای گارانتی در دسترس است
- محصولات رنگ بندی دارند و امکان انتخاب رنگ وجود دارد

---

## 🛠 پیش‌نیازها
قبل از شروع، مطمئن شوید که ابزارهای زیر نصب شده‌اند:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🚦 راه‌اندازی پروژه

1. کد را کلون کنید:
```bash
git clone https://github.com/hamidreza1983/django-shop.git
cd django-shop
```

2. فایل `.env` را تنظیم کنید:
```bash
nano .env
```
- این فایل برای تنظیمات امنیتی سکرت کی و مشخصات smtp sever  میباشد و باید حسب نیاز شما بروز رسانی شود

3. کانتینرها را اجرا کنید:
```bash
docker compose up -d
```

4. اجرای مهاجرت‌ها:
```bash
docker compose exec django python manage.py makemigration
docker compose exec django python manage.py migrate
```

5. ایجاد سوپر یوزر:
```bash
docker compose exec django python manage.py createsuperuser
```

6. دسترسی به پروژه در مرورگر:
```bash
http://localhost:8000/admin
```
---

## ⚙️ دستورات کاربردی

- پس از ورود به پنل ادمین محصولات را ایجاد کنید . کتگوری ها را بسازید
- بخش های مختلف در پنل ادمین به ساده ترین وجه ممکن بصورت رابطه ای در دسترس میباشند
- دیاگرام مدل در کنار فایل پروژه در دسترس است

---

## 📎 لینک‌های مفید
- [مستندات جنگو](https://docs.djangoproject.com/en/stable/)
- [مستندات PostgreSQL](https://www.postgresql.org/docs/)
- [مستندات Docker](https://docs.docker.com/)

---

✨ با عشق ساخته شده برای حمایت از کسب و کار های نوپا❤️

