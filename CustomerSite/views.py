from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .Forms import LaptopForm,CustomerCreationForm,ImageForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib import messages
# Create your views here.
from .decorator.Laptopdecorator import *
from paypalrestsdk import Payment
from django.contrib.auth import logout
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.http import HttpResponse

nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize text into individual words
    words = text.split()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join words back into a single string
    preprocessed_text = ' '.join(words)
    
    return preprocessed_text

import json
from .models import Laptop,Image,Brand,Account, Order, OrderItem
from .facadeDesign.facade import *
from django.views.generic import ListView
from django.views import View
def home(request):
    facade = HomeFacade()
    return facade.render(request)

def admin(request):
    facade = AdminFacade()
    return facade.render(request)

def directLink(request,stt):
    facade = DirectFacade()
    
    if stt==1:
        namePage = "tutorial-page.html"
        # return render("tutorial-page.html")
        return facade.render(request, namePage)
    elif stt == 2:
        namePage = "about-us.html"
        # return render("tutorial-page.html")
        return facade.render(request, namePage)
    elif stt == 3:
        namePage = "cart.html"
        # return render("tutorial-page.html")
        return facade.render(request, namePage)
    elif stt == 4:
        namePage = "register.html"
        # return render("tutorial-page.html")
        return facade.render(request, namePage)
    elif stt==5:
        namePage="trans.html"
        return facade.render(request, namePage)
    else :
        namePage = "index.html"
        # return render("tutorial-page.html")
        return facade.render(request, namePage)
    
    

class LaptopListView(ListView):
    model = Laptop
    template_name = 'all-product.html'

    def get_queryset(self):
        facade = LaptopStoreFacade(self.request)
        return facade.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        facade = LaptopStoreFacade(self.request)
        context.update(facade.get_context_data())
        return context

class CartListView(LoginRequiredMixin,ListView):
    model = OrderItem
    template_name = 'cart.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Retrieve the cart items for the logged-in user
            order = Order.objects.filter(account=user, complete=False).first()
            if order:
                queryset = order.orderitem_set.all()
                return queryset

        return OrderItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            # Retrieve the cart items for the logged-in user
            order = Order.objects.filter(account=user, complete=False).first()
            total_amount=0
            if order:
                # Create a list of dictionaries that contain the OrderItem object, the quantity,
                # the total price, and the associated Laptop for each item
                item_data = []
                for order_item in order.orderitem_set.all():
                    quantity = order_item.quantity
                    total_price = quantity * order_item.price
                    item_data.append({
                        'order_item': order_item,
                        'quantity': quantity,
                        'total_price': total_price,
                        'product': order_item.product,
                    })
                    total_amount+= total_price

                # Add the item data to the context dictionary
                context['items'] = item_data
                context["total_amount"]=total_amount

        return context


@login_required
def add_to_cart(request, laptop_id,quantity,price,ram,ssd):
    facade = CartFacade(request)
    facade.add_to_cart(laptop_id, quantity,price,ram,ssd)
    return redirect('laptop_detail', pk=laptop_id)

# chua facade
# chua facade
class LaptopDetailView(DetailView):
    model = Laptop
    template_name = 'product-page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the current laptop object
        current_laptop = self.get_object()
        all_laptops = Laptop.objects.exclude(pk=current_laptop.pk)
        ram=self.request.GET.get("ram")
        ssd=self.request.GET.get("ssd")
        context["get_price"]=int(current_laptop.get_price())
        context['ram']=1
        context['ssd']=2
        if ram and ssd is None:
            try:
                ram_obj=Ram.objects.get(pk=ram)
                
                laptop_ram_upgrade=ConcreteDecoratorRam(current_laptop,ram_obj.capacity)
                context["get_price"] =int(laptop_ram_upgrade.get_price())
                
            except:
               pass
        if ssd and ram is None:
            try:
                ssd_capacity=SSD.objects.get(pk=ssd).capacity
                laptop_ssd_upgrade=ConcreteDecoratorSSD(current_laptop,ssd_capacity)
                context["get_price"] =int(laptop_ssd_upgrade.get_price())
                
            except:
               pass
        if ssd is not None and ram is not None :
            try:
                ram_obj=Ram.objects.get(pk=ram)
                ssd_obj=SSD.objects.get(pk=ssd)
                
                laptop_ram_upgrade=ConcreteDecoratorRam(current_laptop,ram_obj.capacity)
                laptop_ssd_upgrade=ConcreteDecoratorSSD( laptop_ram_upgrade,ssd_obj.capacity)
                context["get_price"] =int(laptop_ssd_upgrade.get_price())
                context['ram']=ram
                context['ssd']=ssd
                context["ram_detail"]=ram_obj
                context["ssd_detail"]=ssd_obj
                
                
            except:
               print("loi")
        
        # Retrieve all laptops from the database excluding the current laptop
        
        # Extract the laptop descriptions
        laptop_descriptions = [
            ' '.join([
                laptop.description,
                laptop.brand.name,
                str(laptop.ram.capacity),
                laptop.VGA,
                laptop.name,
                laptop.processor
            ]) for laptop in all_laptops
        ]
        
        # Create a TF-IDF vectorizer and fit it on the laptop descriptions
        vectorizer = TfidfVectorizer()
        laptop_vectors = vectorizer.fit_transform(laptop_descriptions)
        
        # Transform the current laptop description into a vector
        current_laptop_vector = vectorizer.transform([' '.join([
            current_laptop.description,
            current_laptop.brand.name,
            str(current_laptop.ram.capacity),
            current_laptop.VGA,
            current_laptop.name,
            current_laptop.processor
        ])])
        
        # Calculate the similarity scores between the current laptop vector and other laptop vectors
        similarity_scores = cosine_similarity(current_laptop_vector, laptop_vectors).flatten()
        laptop_scores = list(zip(all_laptops,   similarity_scores))
        print( laptop_scores)
        laptop_scores.sort(key=lambda x: x[1], reverse=True)
        
        similar_laptops  = [laptop for laptop, _ in laptop_scores]
        similar_laptops=similar_laptops[:6]        
        context['similar_laptops'] = similar_laptops        
        return context   
    


def modify_cart_quantity(request, laptop_id):
    facade = CartFacade(request, laptop_id)
    facade.get_instance()
    return facade.modify_cart_quantity(request,laptop_id)

def remove_from_cart(request, pk):
    facade = CartFacade(request)    
    facade.get_instance()
    return facade.remove_from_cart(pk)

def subtract_quantity_cart(request, pk):
    facade = CartFacade(request)
    facade.get_instance()
    return facade.subtract_quantity_cart(pk)

def add_quantity_cart(request, pk):
    facade = CartFacade(request)
    facade.get_instance()
    return facade.add_quantity_cart(pk)

def add_laptop(request):
    facade = LaptopControlFacade()
    return facade.add_laptop(request)

def edit_laptop(request, pk):
    facade = LaptopControlFacade()
    return facade.edit_laptop(request,pk)

def delete_laptop(request,pk):
    facade = LaptopControlFacade()
    return facade.delete_laptop(request,pk)

def edit_images(request, pk):
    facade = LaptopControlFacade()
    return facade.edit_images(request,pk)

def edit_image(request, pk):
    facade = LaptopControlFacade()
    return facade.edit_image(request,pk)

def login_view(request):
    facade = AuthFacade()
    return facade.login_view(request)

def register_view(request):
    facade = AuthFacade()
    return facade.register_view(request)

def filter(request):
    facade = FilterFacade()
    return facade.filter(request)
def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def create_payment(request,pk):
    checkout=CheckoutDetail.objects.get(pk=pk)
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": f'http://127.0.0.1:8000/execute_payment/',
            "cancel_url": "http://127.0.0.1:8000/cancel_payment"
        },
        "transactions": [
            {
                "amount": {
                    "total": str(checkout.total_amount),
                    "currency": "USD"
                },
                "description": "Payment for Django item"
            }
        ]
    })

    if payment.create():
        # Redirect the user to PayPal to complete the payment
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)

    return HttpResponse('Error processing payment')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)
    print(request.user.pk)

    if payment.execute({"payer_id": payer_id}):
        checkout=CheckoutDetail.objects.filter(account=request.user,completed=False).first()
        checkout.completed=True
      
        checkout.order.complete=True
        checkout.save()
        checkout.order.save()  
        return render(request,"successPage.html")
    else:
        return HttpResponse('Error executing payment')
    

def cancel_payment(request):
    return redirect("cart_list")
@login_required
def checkout(request):
    customer=request.user
    customer=Account.objects.get(pk=customer.pk)
    if request.POST:
        try:
            order = Order.objects.get(account=customer, complete=False)
        except Order.DoesNotExist:
            messages.error(request, 'Cart is empty, please add item to cart first')
            return redirect("checkout")
       
        
        name=request.POST["customerName"]
        email=request.POST["customerEmail"]
        phone=request.POST["customerPhone"]
        address=request.POST["address"]
        
        checkout_detail, created = CheckoutDetail.objects.get_or_create(account=customer, order=order,email=email,phone_number=phone,address=address, total_amount=order.get_total_amount(),completed=False)

    #   
        if created:
            checkout_detail.phone_number = phone
            checkout_detail.total_amount = order.get_total_amount()
            checkout_detail.address = address
            checkout_detail.email=email
            checkout_detail.save()
            return redirect('create_payment',pk=checkout_detail.pk)
        else:
            checkout_detail.save()
            return redirect('create_payment',pk=checkout_detail.pk)
    return render(request,"trans.html",context={"customer":customer})