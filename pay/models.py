from django.db import models
import secrets
from .paystack import Paystack

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref=models.CharField( max_length=200)
    email=models.EmailField( max_length=254)
    verified=models.BooleanField(default=False)
    date_created=models.DateTimeField( auto_now=False, auto_now_add=True)

    class Meta:
        ordering=['-date_created']
        verbose_name='Payment'
        verbose_name_plural='Payments'


    def __str__(self):
        return f"email:{self.email} amount:{self.amount}"

    def save(self, *args, **kwargs)->None:
        while not self.ref:
            ref = secrets.token_urlsafe(16)
            object_with_similar_ref=Payment.objects.filter(ref=ref)
            if not  object_with_similar_ref:
                self.ref=ref
        super().save(*args, **kwargs)


    def amount_value(self):
        return self.amount*100

    def verify_payment(self):
        paystack=Paystack()
        status, result=paystack.verify_payment(ref=self.ref,amount=self.amount)
        if status:
            if result['amount']  /100  == self.amount:
                self.verified=True
            self.save()

            if self.verified:
                return True
    
        return False



    
    


