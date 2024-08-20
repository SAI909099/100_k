from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ForeignKey, CASCADE, Model, DateTimeField, SlugField, ImageField, FloatField, \
    IntegerField, TextField
from django.utils.text import slugify
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    phone_number = CharField(max_length=12, unique=True)
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='users', null=True)


class Region(Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, unique=True)
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModelSlug(Model):
    name = CharField(max_length=255)
    slug = SlugField(unique=True)

    class Meta:
        abstract = True  # o`zi table bo1lib yaratilmasligi kerak # noqa

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):  # noqa
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += '-1'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name


class Category(BaseModel, BaseModelSlug):
    image = ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseModel, BaseModelSlug):
    price = FloatField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, to_field='slug', related_name='product')
    order_count = IntegerField(default=0)
    description = TextField()

    def __str__(self):
        return self.name


class ProductImage(Model):
    image = ResizedImageField(size=[200, 200], quality=100, upload_to='product/')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')
