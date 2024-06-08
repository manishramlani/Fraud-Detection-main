import random
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import joblib, sklearn
from .ml_ops import load_ml_model, make_prediction


# Create your views here.
def index(request):
    return render(request, 'index.html')

def loggin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']

        user = authenticate(username=username , password = pass1 )

        if user is not None:
            login(request , user)
            fname = user.first_name
            return render(request, 'home.html' , {'fname' : fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('login')

    return render(request, 'login.html')

        

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['confirm_password']
        
        if User.objects.filter(username = username):
            messages.error(request, "Username already exist! Try using differnt username")

        if User.objects.filter(email = email):
            messages.error(request, "Email already registered! Try using differnt username")

        if len(username)>10:
            messages.error(request, "Username can not exceed 10 letters")

        if (pass1 != pass2):
            messages.error(request, "Password does not match confirm password")
        


        messages.success(request, "Your Account has been created successfully.")


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        

        myuser.save()

        messages.success(request, "Your account has been successfully created")

        return redirect('register')



    return render(request, 'register.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully! ')
    return render(request, 'index.html')

from .forms import TransferForm
from .models import Account, Transaction
def transfer(request):
    try:
        sender_account = request.user.account
    except Account.DoesNotExist:
        # If the user doesn't have an associated account, create one
        sender_account = Account.objects.create(user=request.user, account_number="123456", account_balance=0.0)

    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            receiver_account_number = form.cleaned_data['receiver_account_number']

            # Retrieve sender and receiver accounts
            sender_account = request.user.account
            receiver_account = get_object_or_404(Account, account_number=receiver_account_number)

            user_profile = request.user.userprofile  # Assuming UserProfile is related to the User model
            city = user_profile.city
            transaction_location  = 'Jaipur'
            avg_amount = user_profile.avg_amouny

            # model = load_ml_model()
            input = [amount, avg_amount, city, transaction_location]
            # input_2d = [input]
            # prediction = make_prediction(model, input_2d)
            print(input)

            
            # Check if the sender has sufficient balance
            if sender_account.account_balance >= amount:
                # Perform the transaction
                sender_account.account_balance -= amount
                sender_account.save()

                receiver_account.account_balance += amount
                receiver_account.save()

                # Record the transaction
                Transaction.objects.create(
                    account=sender_account,
                    transaction_type='Transfer',
                    amount=-amount
                )

                Transaction.objects.create(
                    account=receiver_account,
                    transaction_type='Transfer',
                    amount=amount
                )

                return redirect('transaction_success')  # Redirect to a success page
            else:
                # Insufficient balance, show an error
                form.add_error('amount', 'Insufficient balance for the transaction.')
        else:
            # Form is not valid, handle accordingly
            pass
    else:
        form = TransferForm()

    return render(request, 'transfer.html', {'form': form})

from .models import Account, Transaction
def history(request):
    user_transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')
    return render(request, 'history.html', {'transactions': user_transactions})

def transaction_success(request):
    return render(request, 'transfer.html')