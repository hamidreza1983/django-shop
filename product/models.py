from django.db import models
from accounts.models import Profile, User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

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

class Attribute(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class ProductsColor(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)  # Hex code for the color (e.g., #FF5733)

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    has_discount = models.BooleanField(default=False)
    discount_price = models.PositiveBigIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    price = models.PositiveBigIntegerField()
    color = models.ManyToManyField(ProductsColor, blank=True)  # Many-to-many relationship with ProductsColor
    image = models.ImageField(upload_to='products/')
    # ویژگی‌های اضافی
    total_sold = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_favorites = models.PositiveIntegerField(default=0)
    total_vots = models.PositiveIntegerField(default=0)
    has_guarantee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
       
    def get_comments(self):
        return self.comments.filter(status=True)
    
    def comment_count(self):
        return self.comments.count()
    
    def get_average_score(self):
        scores = self.scores.all()
        if scores.exists():
            total_score = sum([item.score for item in scores])
            return round(total_score / scores.count())
        return 0
    
    def get_guarantees(self):
        return self.guarantees.all()
    
    def get_specifications(self):
        return self.specifications.all()
    
    def get_discounted_price(self):
        price = (int(self.price) - (int(self.price)*int(self.discount_price)/100))
        price = round(price)
        return str(price)

    
class ProductAttribute(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="specifications")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)  # مقدار ویژگی (مثلاً "چرم طبیعی" یا "6.5 اینچ")

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
    

class ProductComment(models.Model):
    product = models.ForeignKey(Products, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name.user.email
    
    def get_replays(self):
        return self.replays.filter(status=True)
    
class ProductReplay(models.Model):
    comment = models.ForeignKey(ProductComment, related_name='replays', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name.user.email
    
class ProductScore(models.Model):
    product = models.ForeignKey(Products, related_name='scores', on_delete=models.CASCADE)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)  # مقدار امتیاز (مثلاً از 1 تا 5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.user.email
    
class Guarantee(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="guarantees")
    mounts = models.PositiveBigIntegerField(default=0)
    price_increase = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} guarantee {self.mounts} mounts"
    
class SpecialOffer(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def remaining_time(self):
        """محاسبه زمان باقی‌مانده به صورت دیکشنری"""
        remaining = self.end_date - timezone.now()
        
        if remaining.total_seconds() < 0:
            return {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
        
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}
    
    def __str__(self):
        return self.product.name

