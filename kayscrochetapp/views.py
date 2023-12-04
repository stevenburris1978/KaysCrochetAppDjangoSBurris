from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views import generic
from django.views.generic import TemplateView

from .forms import SignUpForm, SignInForm, AddToCartForm
from .models import Choice, Item, LikeItem, Customerorder
import stripe
import logging


class IndexView(generic.ListView):
    template_name = "kayscrochetapp/index.html"
    context_object_name = "latest_item_list"

    def get_queryset(self):
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
        try:
            if form.is_valid():
                quantity = form.cleaned_data['quantity']

                # Retrieve or initialize the cart dictionary from the session
                cart = request.session.get('kayscrochetapp:cart', {})

                # Check if the item is already in the cart
                if item.pk in cart:
                    # Update the quantity for the existing item
                    cart[item.pk]['quantity'] += quantity
                    # Update the total_price for the existing item
                    cart[item.pk]['total_price'] = str(Decimal(cart[item.pk]['price']) * Decimal(cart[item.pk]['quantity']))
                else:
                    # Add a new entry for the item in the cart
                    cart[item.pk] = {'quantity': quantity, 'price': str(item.price), 'total_price': str(Decimal(item.price) * Decimal(quantity)),}

                # Save the updated cart back to the session
                request.session['kayscrochetapp:cart'] = cart

                messages.success(request, f"{quantity} {item.item_title}(s) added to your cart.")
                return redirect('kayscrochetapp:cart')  # Redirect to the cart page after adding the item
        except Exception as e:
            # Handle the exception here, e.g., log the error
            print(f"Error adding item to cart: {e}")
            messages.error(request, 'An error occurred while processing your request.')
    else:
        form = AddToCartForm()

    return render(request, 'kayscrochetapp/detail.html', {'item': item, 'form': form})



def cart(request):
    # Retrieve the cart data from the session
    cart = request.session.get('kayscrochetapp:cart', {})
    items = []

    for item_id, item_data in cart.items():
        item = get_object_or_404(Item, pk=item_id)
        quantity = item_data['quantity']
        price_str = item_data['price']
        # Convert price back to Decimal
        price = Decimal(price_str)
        total_price = quantity * price  # Calculate total price for the item

        items.append({'item': item, 'quantity': quantity, 'price': price, 'total_price': total_price})

    context = {'items': items,'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY}
    return render(request, 'kayscrochetapp/cart.html', context)



@require_POST
def remove_from_cart(request, item_id):
    # Retrieve the cart data from the session
    cart = request.session.get('kayscrochetapp:cart', {})

    # Check if the item is in the cart
    if str(item_id) in cart:
        # Get the removed item's total price
        removed_item_total_price = float(cart[str(item_id)]['total_price'])

        # Remove the item from the cart
        del cart[str(item_id)]

        # Save the updated cart back to the session
        request.session['kayscrochetapp:cart'] = cart

        # Print debug information
        print(f"Item {item_id} removed from the cart")

        return JsonResponse({'removed_item_total_price': removed_item_total_price})
    else:
        # If the item is not in the cart, return an error response
        return JsonResponse({'error': f'Item {item_id} not found in the cart'}, status=400)


def like_item(request):
    username = request.user.username
    item_id = request.GET.get('item_id')

    item = Item.objects.get(id=item_id)

    like_filter = LikeItem.objects.filter(item_id=item_id, username=username).first()

    if like_filter == None:
        new_like = LikeItem.objects.create(item_id=item_id, username=username)
        new_like.save()
        item.no_of_likes = item.no_of_likes+1
        item.save()
        return redirect('kayscrochetapp:index')
    else:
        like_filter.delete()
        item.no_of_likes = item.no_of_likes-1
        item.save()
        return redirect('kayscrochetapp:index')

class SuccessView(TemplateView):
    template_name = "kayscrochetapp/payment_success.html"


class CancelView(TemplateView):
    template_name = "kayscrochetapp/payment_canceled.html"


stripe.api_key = settings.STRIPE_SECRET_KEY

# Define a list of allowed IP addresses or domains
ALLOWED_ADDRESSES = ['127.0.0.1', '::1', 'www.kayscrochet.us', '127.0.0.1:8000', 'kayscrochet.us']

# Define the logger
logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def create_payment_intent(request):
    try:
        # Verify that the request is coming from an allowed IP address or domain
        client_address = request.META.get('REMOTE_ADDR')
        client_host = request.META.get('HTTP_HOST')
        if client_address not in ALLOWED_ADDRESSES and client_host not in ALLOWED_ADDRESSES:
            raise PermissionError("Unauthorized access")

        # Extract the amount from the request
        amount_cents = int(request.POST.get('amount', 0))

        # Validate required fields
        if not amount_cents:
            raise ValueError("Amount is required")

        # Convert amount to dollars
        amount_dollars = Decimal(amount_cents) / Decimal(100.0)

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            payment_method_types=['card'],
        )


        return JsonResponse({'clientSecret': intent.client_secret})

    except PermissionError as pe:
        logger.error(f"PermissionError: {pe}")
        return JsonResponse({'error': 'Permission denied'}, status=403)

    except stripe.error.CardError as ce:
        logger.error(f"CardError: {ce.error.message}")
        return JsonResponse({'error': f'Card error: {ce.error.message}'}, status=400)

    except stripe.error.RateLimitError as rle:
        logger.error(f"RateLimitError: {str(rle)}")
        return JsonResponse({'error': f'Rate limit error: {str(rle)}'}, status=429)

    except stripe.error.InvalidRequestError as ire:
        logger.error(f"InvalidRequestError: {str(ire)}")
        return JsonResponse({'error': f'Invalid request error: {str(ire)}'}, status=400)

    except stripe.error.AuthenticationError as ae:
        logger.error(f"AuthenticationError: {str(ae)}")
        return JsonResponse({'error': f'Authentication error: {str(ae)}'}, status=401)

    except stripe.error.StripeError as se:
        logger.error(f"StripeError: {str(se)}")
        return JsonResponse({'error': f'Stripe error: {str(se)}'}, status=500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)


@require_POST
def clear_cart(request):
    try:
        # Extract user information from the request
        full_name = request.POST.get('full_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        # Retrieve the cart data from the session
        cart = request.session.get('kayscrochetapp:cart', {})

        # Calculate the total price based on items in the cart
        total_price = sum(float(item_data['total_price']) for item_data in cart.values())

        # Use a database transaction to ensure consistency
        with transaction.atomic():
            # Create an Order instance and save it to the database
            customerorder = Customerorder.objects.create(
                full_name=full_name,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                total_price=total_price,
                item_title="Items",
            )

            # Create a list to store the titles of all items in the cart
            item_titles = []

            # Iterate over items in the cart and retrieve their titles
            for item_id, item_data in cart.items():
                item = get_object_or_404(Item, pk=item_id)
                item_titles.append(item.item_title)

                # Send email to the logged-in user
                user_email = request.user.email

                print(f"Sending email to user: {user_email}")

                subject = 'Order Confirmation'
                message = f'Thank you for your order. Your invoice details are:\n\nFull Name: {full_name}\nStreet: {street}\nCity: {city}\nState: {state}\nZIP Code: {zip_code}\nTotal Price: ${total_price:.2f}\nItems: {", ".join(item_titles)}\nShipping is included.\nPrice does not include sales or use tax that you may need to pay in your state.'
                from_email = 'kayscrochetus@gmail.com'
                recipient_list = [user_email]
                # Check if there's an error when sending the email
                try:
                    send_mail(subject, message, from_email, recipient_list)
                except Exception as email_error:
                    print(f"Email sending error: {email_error}")

            # Update the item_title field of the Order model
            customerorder.item_title = ", ".join(item_titles)
            customerorder.save()

        # Clear the cart in the session
        request.session['kayscrochetapp:cart'] = {}

        # Send email to kayscrochetus@gmail.com
        admin_email = 'kayscrochetus@gmail.com'
        subject = 'New Order Received'
        message = f'New order details:\n\nFull Name: {full_name}\nStreet: {street}\nCity: {city}\nState: {state}\nZIP Code: {zip_code}\nTotal Price: ${total_price:.2f}\nItems: {", ".join(item_titles)}'
        from_email = 'kayscrochetus@gmail.com'
        recipient_list = [admin_email]
        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'success': True})
    except Exception as e:
        # Handle the exception here
        return JsonResponse({'error': str(e)}, status=500)