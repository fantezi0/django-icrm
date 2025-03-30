from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import signup_form, Item_form
from .models import Item
from .hashmap import HashMapManager
from .signals import hash_map


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, './home.html', {})


def login_user(request):
    #checking and geting user data
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('home')
        else:
            messages.success(request,"Error logging in... check username and password")
            return redirect('login')
    else:
        return render(request, './login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You are logged out... ")
    return redirect('login')

def signup_user(request):
    #checking and geting user data
    if request.method == 'POST':
        form = signup_form(request.POST)
        
        if form.is_valid():
            form.save()
        
        #authenticate user   
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "you signed up successfully")
            return redirect('home')
        
        else:
            messages.success(request, "Error signing up... ")
            return redirect('signup')
        
    #rendering empty form
    else:
        form = signup_form()
        return render(request, './signup.html', {'form': form})
    
def add_item(request):
    if request.method == 'POST':
        item = Item_form(request.POST)
        if item.is_valid():
            new_item = Item.objects.create(**item.cleaned_data)
            hash_map.register_item(new_item)
            messages.success(request, f"{new_item.name} added successfully... ")
            return redirect("add_item")
        else:
            messages.success(request, "Error adding item... ")
            return redirect("add_item")  
    else:
        form = Item_form()
        return render(request, './add_item.html', {'form': form})
    
def display(request):
    items = Item.objects.all().values()
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, './display.html', {'items' : items})

def ed_item(request, id):
    item = get_object_or_404(Item, id = id)
    form = Item_form(instance = item)
    if request.method == 'POST':
        if request.POST.get('action') == "edit":
            item = Item_form(request.POST, instance = item)
            if item.is_valid():
                edited_item = item.save()
                messages.success(request, f"{edited_item.name} edited successfully... ")
                return redirect("display")
            else:
                messages.success(request, "Error editing item... ")
                return redirect("display")
        if request.POST.get('action') == "delete":
            delet_item(request, item)
            return redirect("display")
    else:
        return render (request, './ed_item.html', {'form' : form})
    
def delet_item(request, item):
     item.delete()
     return messages.success(request, f"{item.name} deleted successfully... ")
        