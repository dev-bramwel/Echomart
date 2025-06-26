from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.contrib.auth.views import LoginView #inbuilt login view

def register_view(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html' #Inbuilt login view