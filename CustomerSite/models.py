from django.db import models
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from abc import ABC, abstractmethod
import decimal
from django.contrib.auth import authenticate, login


class Voucher(models.Model):
    id=models.CharField(max_length=20, primary_key=True)
    value=models.FloatField(default=0)
    description=models.TextField()
    quantity=models.IntegerField(default=0)
    def __str__(self):
        return str(self.value)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ram(models.Model):

    CAPACITY_CHOICES = [
        (8, "8GB"),
        (16, "16GB"),
        (32, "32GB"),
    ]
    capacity = models.IntegerField( choices=CAPACITY_CHOICES)
    

    def __str__(self):
        return f"{self.capacity} GB"
class SSD(models.Model):
    CAPACITY_CHOICES = [
        (256, "256GB"),
        (512, "512GB"),
        (1024, "1TB"),
        # Add more capacity choices as needed
    ]
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    type = models.CharField(max_length=100)

    def __str__(self):
        if self.capacity==1024:
            return f"1TB {self.type} SSD"
            
        return f"{self.capacity}GB {self.type} SSD"

    
    
class Laptop(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,null=True)
    
    price = models.DecimalField(max_digits=13, decimal_places=2,default=0)
    description = models.TextField()
    processor = models.CharField(max_length=100,default='Unknown')
    ram = models.ForeignKey(Ram, on_delete=models.SET_NULL, null=True)
    ssd = models.ForeignKey(SSD,on_delete=models.SET_NULL,null=True)
    display_size = models.CharField(max_length=100,default='Unknown')
    weight = models.CharField(max_length=100,default='Unknown')
    battery_life = models.CharField(max_length=100,default='Unknown')
    VGA=models.CharField(max_length=100,default='Unknown')
    wireless=models.CharField(max_length=100,default='Unknown')
    warranty=models.IntegerField(default=24)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    @abstractmethod
    def get_price(self):
        return self.price
    def get_ram_capacity(self) -> int:
        
        
        return self.ram.capacity

    def get_ssd_capacity(self) -> int:
        return self.ssd.capacity

  
            
class Image(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True,blank=True)


class Account(User):
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.username

    def add_to_cart(self,laptop_id,quantity,price,ram,ssd):
        laptop = Laptop.objects.get(id=laptop_id)
        quantity = int(quantity)
        order, created = Order.objects.get_or_create(account= self ,complete=False)
        ram=Ram.objects.get(pk=ram)
        ssd=SSD.objects.get(pk=ssd)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=laptop,price=price,ram=ram,ssd=ssd)
        order_item.quantity = quantity
        try:
            order_item.save()
            order.save()
            return True    
            
        except Exception as e:
           return False
    def subtract_quantity_cart(self,id_OrderItem):
        itemCart=OrderItem.objects.get(id=id_OrderItem)
        if itemCart.quantity>1:
            itemCart.quantity=itemCart.quantity-1
            try:
                itemCart.save()
                return True
            except Exception as e:
                return False
        else:
            return False
    def add_quantity_cart(self,id_OrderItem):
        itemCart=OrderItem.objects.get(id=id_OrderItem)
        if itemCart.quantity:
            itemCart.quantity=itemCart.quantity+1
            try:
                itemCart.save()
                return True
            except Exception as e:
                return False
        else:
            return False
            
        
    def delete_itemcart(self,id_OrderItem):
        itemCart=OrderItem.objects.get(id=id_OrderItem)
        if itemCart:
            itemCart.delete()
            return True
        else:
            return False
        
        
        
            

        # Display a success message
        
class Stock(models.Model):
    laptop = models.OneToOneField(Laptop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)  

class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
  
 
    def __str__(self):
        return str(self.id)
    def get_total_amount(self):
        total = 0
        order_items = self.orderitem_set.all()
        for order_item in order_items:
            total += order_item.get_total
        return total
 
    


class OrderItem(models.Model):
    product = models.ForeignKey(Laptop, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    ram = models.ForeignKey(Ram, on_delete=models.SET_NULL, null=True)
    ssd = models.ForeignKey(SSD, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2,default=0)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.order)
 
    @property
    def get_total(self):
        total = self.price * self.quantity
        return total


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("C","Cancel"),
        ("D","Delivery"),
        ('S', 'Success'),
        ('F', 'Failed'),
        
    ]
    orders = models.ManyToManyField(Order)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username} - {self.order.laptop.name}"
    def Cancel(self):
        existing_transaction=Transaction.objects.filter(customer=self.customer,order=self.orders).first()
        if(existing_transaction is not None):
            if(existing_transaction.status=="O"):
                existing_transaction.status="C"
                existing_transaction.save()
                return True
            else:
                return False
        else:
            return False
    
        
    




class CheckoutDetail(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email=models.CharField(max_length=150)
    address = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    completed=models.BooleanField(default=False)
 
    def __str__(self):
        return self.address