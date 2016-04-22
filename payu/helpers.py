import string
import random

def generate_reference_code(id=None, prefix='payment_test_'):
    if id is None:
        s = string.ascii_lowercase + string.digits
        id = ''.join(random.sample(s,10))
    return prefix + id


def mask_credit_card_number(number):
    """ Mask credit card, keeping the first 6 (Issuer Identification Number)
    and last 4 digits visible """
    return number[:6] + 'X' * 6 + number[-4:]
