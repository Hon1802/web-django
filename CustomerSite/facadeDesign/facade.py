from ..Forms import *
from ..models import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import redirect
from django.shortcuts import render

class LaptopStoreFacade:
    def __init__(self, request):
        self.request = request
    def get_queryset(self):
        queryset = Laptop.objects.all()

        brand = self.request.GET.get('brand')
        ram_size = self.request.GET.get('ram_size')
        cpu_type = self.request.GET.get('cpu_type')
        sort_by = self.request.GET.get('sort_by')
        search_query = self.request.GET.get('search_query')

        if brand:
            queryset = queryset.filter(brand=brand)
        if ram_size:
            queryset = queryset.filter(ram__capacity=ram_size)
        if cpu_type:
            queryset = queryset.filter(processor__contains=cpu_type)
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')

        if search_query:
            preprocessed_query = self.preprocess_text(search_query)
            laptop_descriptions = [
                ' '.join([
                    laptop.description,
                    laptop.brand.name,
                    str(laptop.ram),
                    laptop.VGA,
                    laptop.name,
                    laptop.processor
                ]) for laptop in queryset
            ]

            vectorizer = TfidfVectorizer()
            laptop_vectors = vectorizer.fit_transform(laptop_descriptions)
            query_vector = vectorizer.transform([preprocessed_query])
            similarities = cosine_similarity(query_vector, laptop_vectors).flatten()
            laptop_scores = list(zip(queryset, similarities))
            laptop_scores.sort(key=lambda x: x[1], reverse=True)
            queryset = [laptop for laptop, _ in laptop_scores]

        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context['title'] = 'All Products'
        context['brands'] = Brand.objects.all()
        context['ram_types'] = Ram.objects.values_list('capacity', flat=True).distinct()
        # context['ram_gb'] = [ram.split()[0] for ram in context['ram_types']]
        return context

    @staticmethod
    def preprocess_text(text):
        return text.lower().strip()

class HomeFacade:
    @staticmethod
    def get_context_data():
        # laptops = Laptop.objects.all()[0:10]
        laptops = [
            '../../static/image/banner/bn_1.jpg',
            '../../static/image/banner/bn_2.jbg.jpg',
            '../../static/image/banner/bn_3.jpg',
            '../../static/image/banner/bn_4.jpg',
            '../../static/image/banner/bn_5.jpg',
            '../../static/image/banner/bn_6.jpg',
            '../../static/image/banner/bn_7.png',
            '../../static/image/banner/bn_8.jpg',
            '../../static/image/banner/bn_9.jpg',
            '../../static/image/banner/bn_10.png'
        ]
        return {'laptops': laptops}

    @staticmethod
    def render(request):
        context = HomeFacade.get_context_data()
        return render(request, 'index.html', context)

class AdminFacade:
    @staticmethod
    def get_context_data():
        laptops = Laptop.objects.all()
        return {'laptops': laptops}

    @staticmethod
    def render(request):
        context = AdminFacade.get_context_data()
        return render(request, 'admin.html', context)

class LaptopDetailViewFacade:
    def __init__(self, request, laptop_id):
        self.request = request
        self.laptop_id = laptop_id
    
    def get_laptop(self):
        try:
            return Laptop.objects.get(pk=self.laptop_id)
        except Laptop.DoesNotExist:
            return None
    
    def get_similar_laptops(self, current_laptop):
        # Retrieve all laptops from the database excluding the current laptop
        all_laptops = Laptop.objects.exclude(pk=current_laptop.pk)
        
        # Extract the laptop descriptions
        laptop_descriptions = [
            ' '.join([
                laptop.description,
                laptop.brand.name,
                str(laptop.ram),
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
            str(current_laptop.ram),
            current_laptop.VGA,
            current_laptop.name,
            current_laptop.processor
        ])])
        
        # Calculate the similarity scores between the current laptop vector and other laptop vectors
        similarity_scores = cosine_similarity(current_laptop_vector, laptop_vectors).flatten()
        laptop_scores = list(zip(all_laptops, similarity_scores))
        laptop_scores.sort(key=lambda x: x[1], reverse=True)
        
        similar_laptops = [laptop for laptop, _ in laptop_scores][:6]
        
        return similar_laptops    
   
    def render(self):
        current_laptop = self.get_laptop()
        if current_laptop is None:
            # Xử lý trường hợp laptop không tồn tại
            return render(self.request, 'error.html', {'message': 'Laptop not found.'})
        
        similar_laptops = self.get_similar_laptops(current_laptop)
        
        context = {
            'current_laptop': current_laptop,
            'similar_laptops': similar_laptops,
        }
        
        return render(self.request, 'product-page.html', context)



class CartListViewFacade:
    def __init__(self, user):
        self.user = user

    def get_cart_items(self):
        if self.user.is_authenticated:
            order = Order.objects.filter(account=self.user, complete=False).first()
            if order:
                item_data = []
                for order_item in order.orderitem_set.all():
                    quantity = order_item.quantity
                    total_price = quantity * order_item.product.price
                    item_data.append({
                        'order_item': order_item,
                        'quantity': quantity,
                        'total_price': total_price,
                        'product': order_item.product,
                    })
                return item_data
        return []

    def get_queryset(self):
        if self.user.is_authenticated:
            order = Order.objects.filter(account=self.user, complete=False).first()
            if order:
                queryset = order.orderitem_set.all()
                return queryset
        return OrderItem.objects.none()
    
class CartFacade:

    _instance = None

    @staticmethod
    def get_instance():
        if CartFacade._instance is None:
            CartFacade._instance = CartFacade()
        return CartFacade._instance
    
    def __init__(self, request =None, laptop_id=None, quantity=None, pk=None):
        self.request = request
        self.laptop_id = laptop_id
        self.quantity = quantity
        self.pk = pk

    def add_to_cart(self, laptop_id, price,quantity,ram,ssd):
        if self.request.method == 'GET':
            laptop = Laptop.objects.get(id=laptop_id)

            account = self.request.user.id
            # Assuming the authenticated user has an associated Account instance
            customer = Account.objects.get(id=account)
            print("account:", customer)
            quantity = int(quantity)

            check = customer.add_to_cart(laptop_id, quantity,price,ram,ssd)
            if check:
                messages.success(self.request, 'Item added to cart successfully!')
            else:
                messages.error(self.request, 'Item added to cart error ')

    def modify_cart_quantity(self, laptop_id):
       
        laptop_id = self.laptop_id
        if self.request.method == 'POST':
            new_quantity = int(self.request.POST.get('quantity'))

            # Retrieve the logged-in user's cart
            user = self.request.user
            order = Order.objects.filter(account=user, complete=False).first()
            if order:
                # Get the order item for the given laptop ID
                order_item = get_object_or_404(OrderItem, order=order, product_id=laptop_id)

                # Update the quantity of the order item
                order_item.quantity = new_quantity
                order_item.save()

                messages.success(self.request, 'Cart quantity updated successfully!')
            else:
                messages.error(self.request, 'Invalid cart')

        return redirect('cart')
  
    def remove_from_cart(self, pk):

        user = self.request.user
        if user.is_authenticated:
            account = self.request.user.id
            # Assuming the authenticated user has an associated Account instance
            Customer = Account.objects.get(id=account)

            Check = Customer.delete_itemcart(pk)
            if Check == True:
                messages.success(self.request, 'Item added to cart successfully!')
                return redirect("cart_list")

            else:
                messages.error(self.request, 'Item added to cart error ')
                return redirect("cart_list")

        else:
            return redirect("login")

    def subtract_quantity_cart(self, pk):
        user = self.request.user
        if user.is_authenticated:
            account = self.request.user.id
            # Assuming the authenticated user has an associated Account instance
            Customer = Account.objects.get(id=account)

            Check = Customer.subtract_quantity_cart(pk)
            if Check == True:
                messages.success(self.request, 'Item added to cart successfully!')
                return redirect("cart_list")

            else:
                messages.error(self.request, 'Item added to cart error ')
                return redirect("cart_list")
        else:
            return redirect("login")

    def add_quantity_cart(self, pk):
        user = self.request.user
        if user.is_authenticated:
            account = self.request.user.id
            # Assuming the authenticated user has an associated Account instance
            Customer = Account.objects.get(id=account)

            Check = Customer.add_quantity_cart(pk)
            if Check == True:
                messages.success(self.request, 'Item added to cart successfully!')
                return redirect("cart_list")

            else:
                messages.error(self.request, 'Item added to cart error ')
                return redirect("cart_list")

        else:
            return redirect("login")


class LaptopControlFacade:
    @staticmethod
    def add_laptop(request):
        if request.method == 'POST':
            laptop_form = LaptopForm(request.POST)
            image_form = ImageForm(request.POST)

            files = request.FILES.getlist("image")

            if laptop_form.is_valid():
                laptop = laptop_form.save(commit=False)
                laptop.save()
                for file in files:
                    Image.objects.create(laptop=laptop, image=file)
                messages.success(request, "New Laptop added")

        else:
            laptop_form = LaptopForm()
            image_form = ImageForm()

        return render(request, 'add_product.html', {'laptop_form': laptop_form, "image_form": image_form})

    @staticmethod
    def edit_laptop(request, pk):
        laptop = get_object_or_404(Laptop, pk=pk)
        if request.method == 'POST':
            form = LaptopForm(request.POST, request.FILES, instance=laptop)
            if form.is_valid():
                form.save()
                messages.success(request, "Edit success")
        else:
            form = LaptopForm(instance=laptop)

        return render(request, 'edit-product.html', {'form': form})

    @staticmethod
    def delete_laptop(request, pk):
        laptop = get_object_or_404(Laptop, pk=pk)
        laptop.is_active = False
        laptop.save()

        return redirect('admin')

    @staticmethod
    def edit_images(request, pk):
        laptop = get_object_or_404(Laptop, pk=pk)

        return render(request, 'edit_images.html', {'laptop': laptop})

    @staticmethod
    def edit_image(request, pk):
        image = get_object_or_404(Image, pk=pk)

        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES, instance=image)
            if form.is_valid():
                form.save()
                return redirect('edit_image', pk=image.pk)
        else:
            form = ImageForm(instance=image)

        return render(request, 'edit-image.html', {'form': form, 'image': image})


class AuthFacade:
    @staticmethod
    def login_view(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('laptop_list')  # redirect somewhere you wants
                else:
                    return render(request, 'login.html', {'error': 'Your account is disabled'})
            else:
                return render(request, 'login.html', {'error': 'Invalid login credentials'})
        else:
            return render(request, 'login.html')

    @staticmethod
    def register_view(request):
        if request.method == 'POST':
            form = CustomerCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = CustomerCreationForm()
        return render(request, 'register.html', {'form': form})


class FilterFacade:
    @staticmethod
    def filter(request):
        Filter_brand = Brand.objects.all()
        return render(request, 'all-product.html', {"Brand": Filter_brand})

class HomeViewFacade:
    @staticmethod
    def redirect_home():
        return redirect('home')

class CartListViewFacade:
    def __init__(self, request):
        self.request = request

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Retrieve the cart items for the logged-in user
            order = Order.objects.filter(account=user, complete=False).first()
            if order:
                queryset = order.orderitem_set.all()
                return queryset

        return OrderItem.objects.none()

    def get_context_data(self):
        context = {}

        user = self.request.user
        if user.is_authenticated:
            # Retrieve the cart items for the logged-in user
            order = Order.objects.filter(account=user, complete=False).first()
            if order:
                # Create a list of dictionaries that contain the OrderItem object, the quantity,
                # the total price, and the associated Laptop for each item
                item_data = []
                for order_item in order.orderitem_set.all():
                    quantity = order_item.quantity
                    total_price = quantity * order_item.product.price
                    item_data.append({
                        'order_item': order_item,
                        'quantity': quantity,
                        'total_price': total_price,
                        'product': order_item.product,
                    })

                # Add the item data to the context dictionary
                context['items'] = item_data
        return context
    

class DirectFacade:
    @staticmethod
    def get_context_data():
        return {}

    @staticmethod
    def render(request, templateName):
        context = DirectFacade.get_context_data()

        return render(request, templateName, context)