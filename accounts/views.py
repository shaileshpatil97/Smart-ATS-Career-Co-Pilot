from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'registration/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/signup.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'registration/signup.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('/upload/')

    return render(request, 'registration/signup.html')


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/upload/')
        return render(request, "registration/login.html", {"error": "Invalid credentials"})

    return render(request, "registration/login.html")


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def delete_account(request):
    request.user.delete()
    logout(request)
    return redirect('/')
