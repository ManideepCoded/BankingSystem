from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoanForm
from .models import Account, Transaction, Loan
from decimal import Decimal
from django.db import transaction


# ------------------ Redirect Home ------------------
def home_redirect(request):
    return redirect('login')


# ------------------ Register ------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# ------------------ Dashboard ------------------
@login_required
def dashboard(request):
    account, created = Account.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    return render(request, 'dashboard.html', {
        'account': account,
        'transactions': transactions
    })


# ------------------ Deposit ------------------
@login_required
def deposit(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Please enter amount")
            return redirect("deposit")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount")
            return redirect("deposit")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0")
            return redirect("deposit")

        try:
            with transaction.atomic():
                account = Account.objects.select_for_update().get(user=request.user)

                account.balance += amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type="Deposit",
                    amount=amount
                )

            messages.success(request, "Deposit successful!")
            return redirect("dashboard")

        except Account.DoesNotExist:
            messages.error(request, "Account not found")
            return redirect("dashboard")

    return render(request, "deposit.html")


# ------------------ Withdraw ------------------
@login_required
def withdraw(request):
    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Please enter amount")
            return redirect("withdraw")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount")
            return redirect("withdraw")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0")
            return redirect("withdraw")

        try:
            with transaction.atomic():
                account = Account.objects.select_for_update().get(user=request.user)

                if amount > account.balance:
                    messages.error(request, "Insufficient balance!")
                    return redirect("withdraw")

                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    transaction_type="Withdraw",
                    amount=amount
                )

            messages.success(request, "Withdrawal successful!")
            return redirect("dashboard")

        except Account.DoesNotExist:
            messages.error(request, "Account not found")
            return redirect("dashboard")

    return render(request, "withdraw.html")


# ------------------ Transfer ------------------
@login_required
def transfer(request):
    if request.method == "POST":
        receiver_account_number = request.POST.get("account_number")
        amount = request.POST.get("amount")

        if not receiver_account_number or not amount:
            messages.error(request, "All fields are required")
            return redirect("transfer")

        try:
            amount = Decimal(amount)
        except:
            messages.error(request, "Invalid amount")
            return redirect("transfer")

        if amount <= 0:
            messages.error(request, "Amount must be greater than 0")
            return redirect("transfer")

        try:
            with transaction.atomic():

                sender_account = Account.objects.select_for_update().get(user=request.user)
                receiver_account = Account.objects.select_for_update().get(
                    account_number=receiver_account_number
                )

                if receiver_account == sender_account:
                    messages.error(request, "You cannot transfer to your own account")
                    return redirect("transfer")

                if amount > sender_account.balance:
                    messages.error(request, "Insufficient balance")
                    return redirect("transfer")

                # Perform transfer
                sender_account.balance -= amount
                receiver_account.balance += amount

                sender_account.save()
                receiver_account.save()

                Transaction.objects.create(
                    account=sender_account,
                    transaction_type="Transfer Sent",
                    amount=amount
                )

                Transaction.objects.create(
                    account=receiver_account,
                    transaction_type="Transfer Received",
                    amount=amount
                )

            messages.success(request, "Transfer successful!")
            return redirect("dashboard")

        except Account.DoesNotExist:
            messages.error(request, "Receiver account not found")
            return redirect("transfer")

    return render(request, "transfer.html")


# ------------------ Transaction History ------------------
@login_required
def transaction_history(request):
    try:
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
        return render(request, 'transaction_history.html', {'transactions': transactions})
    except Account.DoesNotExist:
        messages.error(request, "Account not found")
        return redirect("dashboard")


# ------------------ Apply Loan ------------------
@login_required
def apply_loan(request):
    try:
        account = Account.objects.get(user=request.user)

        if request.method == "POST":
            form = LoanForm(request.POST)
            if form.is_valid():
                loan = form.save(commit=False)
                loan.account = account
                loan.interest_rate = 10.0
                loan.save()

                messages.success(request, "Loan application submitted!")
                return redirect('dashboard')
        else:
            form = LoanForm()

        return render(request, 'apply_loan.html', {'form': form})

    except Account.DoesNotExist:
        messages.error(request, "Account not found")
        return redirect("dashboard")