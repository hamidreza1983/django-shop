from django.db import models

# Create your models here.

from django.db import models

class Category(models.Model):
    # نام دسته‌بندی، با محدودیت 100 کاراکتر و مقدار یکتا
    name = models.CharField(max_length=100, unique=True)
    
    # فیلدی برای مشخص کردن والد دسته‌بندی، که به خود مدل اشاره می‌کند
    parent = models.ForeignKey(
        'self',                     # ارجاع به خود مدل
        on_delete=models.CASCADE,   # حذف زیر دسته‌ها در صورت حذف والد
        null=True,                  # دسته‌بندی اصلی می‌تواند والد نداشته باشد
        blank=True,                 # مقدار والد می‌تواند خالی باشد
        related_name='subcategories' # دسترسی به زیر دسته‌ها با این نام ممکن می‌شود
    )

    # نمایش رشته‌ای برای نمایش بهتر دسته‌بندی‌ها
    def __str__(self):
        # اگر دسته‌بندی والد داشته باشد، نام والد/نام دسته‌بندی نمایش داده می‌شود
        return f"{self.parent.name} / {self.name}" if self.parent else self.name

    class Meta:
        verbose_name = "Category"            # نام مفرد برای دسته‌بندی
        verbose_name_plural = "Categories"    # نام جمع برای دسته‌بندی‌ها