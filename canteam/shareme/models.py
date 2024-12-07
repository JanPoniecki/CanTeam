from django.db import models

class User42(models.Model):
    name = models.CharField(max_length=20)
    balance = models.FloatField(default=0)
    coffee_score = models.IntegerField(default=0)
    color = models.CharField(max_length=7, default='#b8b8b8')
    color = models.CharField(max_length=20, blank=True, null=True)
    pwd = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name

class Sponsor(models.Model):
    user42 = models.ForeignKey(User42, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    real_name = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user42.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=7, default='#b8b8b8')
    price = models.FloatField(default=0)
    scoops = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    unit = models.CharField(max_length=100, blank=True, null=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.name

class Action(models.Model):
    user42 = models.ForeignKey(User42, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    scoops = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    paid = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    is_order = models.BooleanField(default=True)

