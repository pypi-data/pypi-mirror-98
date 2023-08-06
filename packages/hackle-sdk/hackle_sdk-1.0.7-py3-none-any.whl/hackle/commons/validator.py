import math
import numbers

from six import integer_types
from six import string_types

from hackle import model


def is_non_empty_string(input_id_key):
    if input_id_key and isinstance(input_id_key, string_types):
        return True

    return False


def is_non_zero_and_empty_int(input_id_key):
    if input_id_key and isinstance(input_id_key, integer_types) and input_id_key > 0:
        return True

    return False


def is_number(input_id_key):
    if input_id_key and isinstance(input_id_key, numbers.Number):
        return True

    return False


def is_event_value_valid(attribute_value):
    if attribute_value is None:
        return True

    if isinstance(attribute_value, (numbers.Integral, float)):
        return is_finite_number(attribute_value)

    return False


def is_finite_number(value):
    if not isinstance(value, (numbers.Integral, float)):
        # numbers.Integral instead of int to accommodate long integer in python 2
        return False

    if isinstance(value, bool):
        # bool is a subclass of int
        return False

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return False

    if abs(value) > (2 ** 53):
        return False

    return True


def is_valid_user(user):
    if user is None:
        return False

    if user and not isinstance(user, model.User):
        return False

    if user and user.id is None:
        return False

    if user and not isinstance(user.id, string_types):
        return False

    return True


def is_valid_event(event):
    if event is None:
        return False

    if event and not isinstance(event, model.Event):
        return False

    if event and event.key is None:
        return False

    if event and not isinstance(event.key, string_types):
        return False

    if event and event.value and not is_event_value_valid(event.value):
        return False

    return True
