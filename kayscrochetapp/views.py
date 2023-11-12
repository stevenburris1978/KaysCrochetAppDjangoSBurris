from decimal import Decimal
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from .forms import SignUpForm, SignInForm, AddToCartForm
from .models import Choice, Item


class IndexView(generic.ListView):
    template_name = "kayscrochetapp/index.html"
    context_object_name = "latest_item_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by("-pub_date")[:100]

    @method_decorator(login_required(login_url='kayscrochetapp:signin'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DetailView(generic.DetailView):
    model = Item
    template_name = "kayscrochetapp/detail.html"

    @method_decorator(login_required(login_url='kayscrochetapp:signin'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResultsView(generic.DetailView):
    model = Item
    template_name = "kayscrochetapp/results.html"

    @method_decorator(login_required(login_url='kayscrochetapp:signin'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def like(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
        selected_choice = item.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "kayscrochetapp/detail.html",
            {
                "item": item,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.likes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("kayscrochetapp:results", args=(item.id,)))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('kayscrochetapp:index')
    else:
        form = SignUpForm()
    return render(request, 'kayscrochetapp/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('kayscrochetapp:index')
    else:
        form = SignInForm()
    return render(request, 'kayscrochetapp/signin.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('kayscrochetapp:index')


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Retrieve or initialize the cart dictionary from the session
            cart = request.session.get('kayscrochetapp:cart', {})

            # Check if the item is already in the cart
            if item.pk in cart:
                # Update the quantity for the existing item
                cart[item.pk]['quantity'] += quantity
            else:
                # Add a new entry for the item in the cart
                cart[item.pk] = {'quantity': quantity, 'price': str(item.price)}

            # Save the updated cart back to the session
            request.session['kayscrochetapp:cart'] = cart

            return redirect('kayscrochetapp:cart')  # Redirect to the cart page after adding the item
    else:
        form = AddToCartForm()

    return render(request, 'kayscrochetapp/detail.html', {'item': item, 'form': form})


def cart(request):
    # Retrieve the cart data from the session
    cart = request.session.get('kayscrochetapp:cart', {})
    items = []

    # Assuming you have a model named Item, and you want to display item details in the cart
    for item_id, item_data in cart.items():
        item = get_object_or_404(Item, pk=item_id)
        quantity = item_data['quantity']
        price_str = item_data['price']
        # Convert price back to Decimal
        price = Decimal(price_str)
        total_price = quantity * price  # Calculate total price for the item

        items.append({'item': item, 'quantity': quantity, 'price': price, 'total_price': total_price})

    context = {'items': items}
    return render(request, 'kayscrochetapp/cart.html', context)
