from .models import Customer
from .utilities import transaction_api
from .forms import CreateCustomer, CollectPin, CollectNumber

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404


def index(request):
    return render(request, "index.html")


def customer_creation(request):
    message = 'Let\'s create a simple customer to test the system'
    button = 'Create Customer'
    extra = True
    cancel = False

    if request.method == 'POST':
        form = CreateCustomer(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            full_name, account_number, amount, pin = [
                cd[item]
                for item in [
                    'full_name',
                    'account_number',
                    'amount',
                    'pin'
                ]
            ]

            Customer.objects.create(
                full_name=full_name,
                account_number=account_number,
                amount=amount,
                pin=pin
            ).save()

            messages.success(request, 'Customer Created! Do you wish to create another?')
        else:
            messages.error(request, "Form not valid! Couldn't create customer")
    else:
        form = CreateCustomer()

    context = {
        'form': form,
        'message': message,
        'button': button,
        'extra': extra,
        'cancel': cancel
    }

    return render(request, "atm_simulation/forms.html", context)


def start_atm_operation(request):
    message = 'Assume your ATM card has been entered.'
    button = 'Proceed'
    extra = False
    cancel = True

    if request.method == 'POST':
        form = CollectPin(request.POST)

        if form.is_valid():
            pin = form.cleaned_data['pin']

            return HttpResponseRedirect(reverse('atm_operations', args=[pin]))
        else:
            messages.error(request, "Invalid pin for ATM card!")
    else:
        form = CollectPin()

    context = {
        'form': form,
        'message': message,
        'button': button,
        'extra': extra,
        'cancel': cancel
    }

    return render(request, "atm_simulation/forms.html", context)


def atm_operations(request, pin):
    if pin not in [p.pin for p in Customer.objects.all()]:
        messages.error(request, "Pin does not match imputed card")
        return HttpResponseRedirect(reverse('start_atm_operation'))
    else:
        return render(request, "atm_simulation/operations.html", {'customer': get_object_or_404(Customer, pin=pin)})


def check_balance(request, pin):
    customer = get_object_or_404(Customer, pin=pin)
    amount_left = customer.amount

    context = {
        'customer': customer,
        'amount_left': amount_left
    }

    return render(request, "atm_simulation/check_balance.html", context)


def change_pin(request, pin):
    customer = get_object_or_404(Customer, pin=pin)

    message = 'Enter the new pin you desire to make use of...'
    button = 'Change Pin'
    extra = False
    cancel = False

    if request.method == 'POST':
        form = CollectPin(request.POST)

        if form.is_valid():
            customer.pin = form.cleaned_data['pin']
            customer.save()

            return HttpResponseRedirect(reverse('perform_another_trans'))
        else:
            messages.error(request, "Invalid pin for ATM card!")
    else:
        form = CollectPin()

    context = {
        'customer': customer,
        'form': form,
        'message': message,
        'button': button,
        'extra': extra,
        'cancel': cancel
    }

    return render(request, "atm_simulation/forms.html", context)


def send_money(request, pin, num_type):
    if num_type == 'acc':
        num_type = 'Account Number'
    else:
        num_type = 'Mobile Number'

    message = 'Enter Amount'
    button = 'Proceed'
    extra = False
    cancel = True

    if request.method == 'POST':
        form = CollectNumber(request.POST)

        if form.is_valid():
            number = str(form.cleaned_data['number'])

            return HttpResponseRedirect(reverse('collect_number', args=[pin, num_type, number]))
        else:
            messages.error(request, "Invalid pin for ATM card!")
    else:
        form = CollectNumber()

    context = {
        'form': form,
        'message': message,
        'button': button,
        'extra': extra,
        'cancel': cancel,
    }

    return render(request, "atm_simulation/forms.html", context)


def collect_number(request, pin, num_type, amt):
    amt = int(amt)

    customer = get_object_or_404(Customer, pin=pin)

    message = f'Enter Beneficiary {num_type}'
    button = 'Proceed'
    extra = False
    cancel = True

    if request.method == 'POST':
        form = CollectNumber(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']

            if num_type == 'Account Number':
                trans_customer = get_object_or_404(Customer, account_number=number)
                return HttpResponseRedirect(reverse('transfer_operation', args=[pin, amt, trans_customer]))
            else:
                return HttpResponseRedirect(reverse('withdraw_operation', args=[pin, amt]))
        else:
            messages.error(request, "Invalid pin for ATM card!")
    else:
        form = CollectNumber()

    context = {
        'customer': customer,
        'form': form,
        'message': message,
        'button': button,
        'extra': extra,
        'cancel': cancel,
    }

    return render(request, "atm_simulation/forms.html", context)


def button_operations(request, pin, trans_type):
    return render(request, "atm_simulation/button_operations.html", {
        'trans_type': trans_type,
        'customer': get_object_or_404(Customer, pin=pin)
    })


def withdraw_operation(request, pin, amt):
    amt = int(amt)
    customer = get_object_or_404(Customer, pin=pin)
    result = transaction_api.transaction(amt, customer, 'withdraw')

    if result is not None:
        messages.error(request, result[1])
    else:
        messages.success(request, "Transaction Successful!")

    return HttpResponseRedirect(reverse('perform_another_trans'))


def transfer_operation(request, pin, amt, trans_customer):
    amt = int(amt)
    customer = get_object_or_404(Customer, pin=pin)
    result = transaction_api.transaction(amt, customer, 'transfer', trans_customer)

    if result is not None:
        messages.error(request, result[1])
    else:
        messages.success(request, "Transaction Successful!")

    return HttpResponseRedirect(reverse('perform_another_trans'))


def perform_another_trans(request):
    return render(request, "atm_simulation/another_trans.html")
