import string
import random

def generate_reference_code(id=None, prefix='payment_test_'):
    if id is None:
        s = string.ascii_lowercase + string.digits
        id = ''.join(random.sample(s,10))
    return prefix + id
