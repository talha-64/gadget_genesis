from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import products,categories, order
from .forms import contactForm

def register(request):
  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if User.objects.filter(username = username).exists():
      messages.error(request, "Username already exists.")
      return redirect('register')
    
    if User.objects.filter(email = email).exists():
      messages.error(request, "Account already exists on this Email.")
      return redirect('register')

    try:
      validate_password(password)
    except ValidationError as e:
      for error in e:
        messages.error(request, error)
        return redirect('register')

    user = User.objects.create(
    first_name = first_name,
    last_name = last_name,
    email = email,
    username = username
    )

    user.set_password(password)
    user.save()

    messages.success(request, "Account Created Succesfully. Login")
    
    return redirect('login')

  return render(request, "register.html")

def login_page(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not User.objects.filter(email = email).exists():
      messages.error(request, "Invalid email.")
      return redirect('login')
    
    try:
      user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
      messages.error(request, "Invalid email.")
      return redirect('login')

    user = authenticate(username = user_obj.username, password = password)
      
    if user is None:
      messages.error(request, "Invalid password.")
      return redirect('login')
    
    else:
      login(request, user)
      return redirect('home')
  
  return render(request, "login.html")

@login_required
def logout_page(request):
  logout(request)
  return redirect('home')


@login_required
def profile(request):
  # user_id = request.user.id

  orders = order.objects.filter(user = request.user)

  return render(request, 'profile.html', {'orders':orders})


def home(request):
  productss = products.objects.all()
  category = categories.objects.all()

  now = timezone.now()  # Get current timezone-aware datetime
  local_now = timezone.localtime(now) # Convert to current timezone
  time_obj = local_now.time()

  return render(request, "index.html", context={'products':productss, 'categories' : category, 'time':time_obj})


def shop(request):
  sort_opt = request.GET.get('sort')
  category_id = request.GET.get('category')

  productss = products.objects.all()

  if category_id:
    productss = productss.filter(category = category_id)

  if sort_opt == '':
    productss = productss
  elif sort_opt == 'price_low':
    productss = productss.order_by('price')
  elif sort_opt == 'price_high':
    productss = productss.order_by('-price')

  all_categories = categories.objects.all()
  
  return render(request, "shop.html", context={'products': productss, 'categories': all_categories, 'selected_category':int(category_id) if category_id else None})


def product(request, id):
  product = get_object_or_404(products, pk=id)
  return render(request, "product.html", context= {"product": product})


@login_required
def contact(request):
  if request.method == 'POST':
    form = contactForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('contact')
  else:
    form = contactForm()
  return render(request, "contact.html", {'form': form})


@login_required
def cart(request, id = None):
  product_id = request.GET.get('product_id')
  product = None
  total = 0
  quant = 0

  if product_id:
    try:
      product = products.objects.get(id=product_id)
      prod_price = product.price
      quant = int(request.GET.get('quantity', 1))
      total = prod_price * quant

      request.session['product_id'] = product_id
      request.session['total'] = total
      request.session['quantity'] = quant
    except products.DoesNotExist:
      product = None

  return render(request, "cart.html", context={"cartItems": [product] if product else [], 'total':total, 'quantity': quant})

@login_required
def checkout(request):
    product_id = request.session.get('product_id')
    total = request.session.get('total', 0)
    quantity = request.session.get('quantity', 1)

    prod = get_object_or_404(products, pk=product_id)

    shipping_cost = 200
    updated_total = total + shipping_cost

    if request.method == 'POST':
      name = request.POST.get('name')
      phone_number = request.POST.get('phone')
      email = request.POST.get('email')
      address = request.POST.get('address')

      new_order = order.objects.create(
        name=name,
        phone_number=phone_number,
        email=email,
        address=address,
        product=prod,
        prod_quantity=quantity,
        total_price=updated_total,
        user=request.user
      )
      try:
        new_order.full_clean()  # 🔍 Enforces model field validations
        new_order.save()
      except ValidationError as e:
        return render(request, 'checkout.html', {
          'product': prod,
          'total': total,
          'quantity': quantity,
          'shipping_cost': shipping_cost,
          'gtotal': updated_total,
          'errors': e.message_dict
      })
    
      request.session['last_order_id'] = new_order.id

      return redirect('ordercompleted')

    return render(request, 'checkout.html', {'product':prod,'total': total,'quantity': quantity,'shipping_cost': shipping_cost,'gtotal': updated_total,})

@login_required
def ordercompleted(request):

  order_id = (request.session.get('last_order_id'))

  if not order_id:
    return render(request, 'ordercompleted.html', {'error': 'No recent order found.'})

  latest_order = get_object_or_404(order, pk=order_id)

  for key in ['product_id', 'total', 'quantity', 'shipping_cost', 'last_order_id']:
    request.session.pop(key, None)

  return render(request, 'ordercompleted.html', {'order': latest_order})



