from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import signup_form, ItemForm 
from .models import Item
from .hashmap import HashMapManager




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

@login_required  
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST) 
        
        if form.is_valid():
            
            if form.instance.name in Item.objects.values_list('name', flat=True):
                messages.error(request, "Item already exists... ")
                messages.info(request, f"do you want to edit {form.instance.name} instead?")  
                action = request.POST.get('action')
                if action == "yes":
                    ed_item(request, form.instance.id)
                else:
                    return redirect("add_item")
            else:
                form.save()
                HashMapManager.add_to_map(form.instance)
                messages.success(request, f"{form.instance.name} added successfully... ")
                return redirect("add_item")
        else:
            messages.success(request, "Error adding item... ")
            return redirect("add_item")  
    else:
        form = ItemForm() 
        return render(request, './add_item.html', {'form': form})
    
@login_required     
def display(request):
    items = Item.objects.all().values()
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'display.html', {'items' : items})
    
@login_required  
def ed_item(request, id):
    item = get_object_or_404(Item, id=id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "edit":
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                edited_item = form.save()
                HashMapManager.add_to_map(edited_item)  # Update the hashmap
                messages.success(request, f"{edited_item.name} edited successfully... ")
            else:
                messages.error(request, "Error editing item... ")
        elif action == "delete":
            delete_item(request, item)
        return redirect("display")
    else:
        form = ItemForm(instance=item)
        return render(request, './ed_item.html', {'form': form})

def delete_item(request, item):
    if request.method == "POST":
        try :
            item.delete()
            return messages.success(request, f"{item.name} deleted successfully... ")
        except Item.DoesNotExist:
            return messages.success(request, "Error deleting item... ")

@login_required
def search_items(request):
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()
        if query:
            result = Item.objects.get(name=query)
            if result:
                return render(request, 'search_results.html', {'items': [result]})
            else:
                messages.info(request, "No items found.")
        return render(request, 'search_results.html', {'items': []})