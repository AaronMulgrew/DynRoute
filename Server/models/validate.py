
def validate_numbers(numbers):
    ## this function validations to make
    ## sure that numbers are really numbers
    if isinstance(numbers, list):
        for num in numbers:
            try:
                int(num)
            except Exception as e:
                return False
            return True
    else:
        try:
            int(numbers)
            return True
        except Exception:
            return False
