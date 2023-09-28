import re
from django.core.exceptions import ValidationError

def validate_text_with_spaces_and_punctuation(value):
    # Regular expression pattern to match valid characters (letters, numbers, spaces, and various punctuation)
    pattern = r'^[a-zA-Z0-9\s.,!?\'"()/-]+$'

    if not re.match(pattern, value):
        raise ValidationError('Enter a valid text consisting of letters, numbers, spaces, and common punctuation.')


def validate_letters_only(value):
    if not value.isalpha():
        raise ValidationError("This field should contain letters only.")