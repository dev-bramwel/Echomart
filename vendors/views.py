from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User # type: ignore
from .models import Vendor, Order
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Vendor registration view
def register_view(request): # type: ignore
    if request.method == 'POST': # type: ignore
        form = UserCreationForm(request.POST) # type: ignore
        if form.is_valid():
            user = form.save()
            # Create a Vendor instance associated with this user
            Vendor.objects.create(user=user, shop_name="Your Shop", phone="0000000000")
            messages.success(request, 'Vendor account created successfully.') # type: ignore
            return redirect('login')  # or wherever your login URL is
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form}) # type: ignore


# Vendor dashboard view
@login_required
def vendor_dashboard(request): # type: ignore
    try:
        vendor = Vendor.objects.get(user=request.user) # type: ignore
        orders = Order.objects.filter(vendor=vendor)

        total_orders = orders.count()
        total_revenue = orders.aggregate(total=Sum('amount'))['total'] or 0.00

    except Vendor.DoesNotExist:
        vendor = None
        total_orders = 0
        total_revenue = 0.00

    context = { # type: ignore
        'user': request.user, # type: ignore
        'vendor': vendor,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }

    return render(request, 'dashboard.html', context) # type: ignore
