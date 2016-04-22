import re
import string
import random

CREDIT_CARD_PATTERNS = {
    'VISA': re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$'),
    'MASTERCARD': re.compile(r'^5[1-5][0-9]{14}$'),
    'AMEX': re.compile(r'^3[47][0-9]{13}$'),
    'DINERS': re.compile(r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$'),
    'DISCOVER': re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$')
}

def clean_cc_number(number):
    return number.replace(" ", "")

def card_type_from_number(number):
    if not number:
        return None
    number = clean_cc_number(number)
    for type, regexp in CREDIT_CARD_PATTERNS.items():
        if regexp.match(str(number)):
            return type
    return None

def generate_reference_code(id=None, prefix='payment_test_'):
    if id is None:
        s = string.ascii_lowercase + string.digits
        id = ''.join(random.sample(s,10))
    return prefix + str(id)


def mask_credit_card_number(number):
    """ Mask credit card, keeping the first 6 (Issuer Identification Number)
    and last 4 digits visible """
    return number[:6] + 'X' * 6 + number[-4:]
