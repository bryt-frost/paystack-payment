from django.shortcuts import render,redirect
from .forms import PaymentForm
from django.conf import settings
from django.contrib import messages
from .models import Payment
# Create your views here.
def initiate_payment(request):
    if request.method=='POST':
        payment_form=PaymentForm(request.POST)
        if payment_form.is_valid():
            payment= payment_form.save()
            return render(request, 'make_payment.html', {"payment":payment,"paystack_public_key":settings.PAYSTACK_PUBLIC_KEY})
    else:
        payment_form=PaymentForm()
    return render(request, 'initiate_payment.html',{"payment_form":payment_form})


def verify_payment(request,ref):
    payment=Payment.objects.get(ref=ref)
    verified=payment.verify_payment()
    if verified:
        messages.success(request, 'Verification Successful')
    else:
        messages.error(request, 'Verification Failed')
    return redirect('initiate-payment')