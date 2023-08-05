from flask.signals import Namespace as SignalNamespace


_signals = SignalNamespace()
model_payment_method_updated = _signals.signal('stripe_model_payment_method_updated')
model_subscription_updated = _signals.signal('stripe_model_subscription_updated')
model_subscription_invoice_created = _signals.signal('stripe_model_subscription_invoice_created')
model_last_invoice_updated = _signals.signal('stripe_model_last_invoice_updated')
invoice_payment = _signals.signal('stripe_invoice_payment')


def stripe_event_signal(event_name):
    return _signals.signal('stripe_%s' % event_name)


def connect_to_stripe_event(event_name):
    return stripe_event_signal(event_name).connect
