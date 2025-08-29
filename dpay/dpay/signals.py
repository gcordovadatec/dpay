from django.dispatch import receiver
from pretix.base.signals import register_payment_providers
from .payment import DpayPaymentProvider

@receiver(register_payment_providers, dispatch_uid="register_dpay_payment_provider")
def register_dpay_payment_provider(sender, **kwargs):
    return DpayPaymentProvider