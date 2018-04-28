from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from shop.utils import unique_slug_generator
from profiles.models import Distributor

def item_upload_location(instance, filename):
    return "%s/%s" %(instance.slug, filename)

class Category(models.Model):
    name            = models.CharField(max_length=50)
    slug            = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:categories', kwargs={'slug': self.slug})

class Item(models.Model):
    owner           = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    name            = models.CharField(max_length=200)
    slug            = models.SlugField(unique=True, blank=True)
    description     = models.TextField(default='') 
    price           = models.IntegerField(default=0)
    sold            = models.IntegerField(default=0)
    weight          = models.IntegerField(default=0)
    stock           = models.IntegerField(default=0)
    is_approvaled   = models.BooleanField(default=False)
    is_updated      = models.BooleanField(default=False)
    is_deleted      = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    category        = models.ForeignKey(Category)
    related_product = models.ForeignKey('Item', null=True, blank=True)
    # Image
    image           = models.ImageField(upload_to=item_upload_location, width_field='width_field', height_field='height_field')
    width_field     = models.IntegerField(default=0)
    height_field    = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:detail', kwargs={'slug': self.slug})

class ShoppingCart(models.Model):
    owner           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_cart')
    items           = models.ManyToManyField(Item, blank=True, related_name='items')

    def __str__(self):
        return self.owner.username

class ItemExtra(models.Model):
    itemex          = models.OneToOneField(Item, related_name='itemex')
    shopcart        = models.ForeignKey(ShoppingCart)
    quantity        = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.itemex.name

class Order(models.Model):
    owner           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_cart       = models.ForeignKey(ShoppingCart)
    order_items     = models.ManyToManyField(Item, blank=True, related_name='order_items')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.owner.username

class Comment(models.Model):
    owner           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment         = models.TextField(max_length=500)

@receiver(pre_save, sender=Item)
@receiver(pre_save, sender=Category)
def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
