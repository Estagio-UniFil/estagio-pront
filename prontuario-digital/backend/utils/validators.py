from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _


def validate_cpf(cpf_str):
    """
    Validates a brazilian CPF
    """

    cpf = [int(digit) for digit in cpf_str]

    if len(cpf_str) != 11:
        raise ValidationError("CPF must contain 11 digits.")

    # If all digits are the same
    if cpf_str == cpf_str[0] * 11:
        raise ValidationError("Invalid CPF.")

    def _calculate_digit(cpf_digits):
        org_digits = cpf_digits
        val_digits = []
        sum = 0
        mod = 0

        for i in range(9):
            val_digits.append(org_digits[i])
            sum += org_digits[i] * (10 - i)

        mod = sum % 11

        if (11 - mod) > 9:
            first_digit = 0
        else:
            first_digit = 11 - mod

        val_digits.append(first_digit)
        sum = 0

        for i in range(11):
            if i > 9:
                break
            sum += val_digits[i] * (11 - i)

        mod = sum % 11

        if (11 - mod) > 10:
            second_digit = 0
        else:
            second_digit = 11 - mod

        val_digits.append(second_digit)

        return val_digits == org_digits

    if not _calculate_digit(cpf):
        raise ValidationError(("Invalid CPF."))

    return cpf_str


if __name__ == "__main__":
    valid_cpf = "12345678909"
    invalid_cpf = "123456789011"
    invalid_cpf_equal_digits = "11111111111"

    print(f"Testing valid CPF {valid_cpf}:")
    try:
        validate_cpf(valid_cpf)
        print("✅ Valid!")
    except ValidationError as e:
        print(f"❌ Error: {e.message}")

    print(f"\nTesting invalid CPF {invalid_cpf}:")
    try:
        validate_cpf(invalid_cpf)
        print("✅ Valid!")
    except ValidationError as e:
        print(f"❌ Error: {e.message}")
    print(f"\nTesting invalid CPF (all same digits) {invalid_cpf_equal_digits}:")
    try:
        validate_cpf(invalid_cpf_equal_digits)
        print("✅ Valid!")
    except ValidationError as e:
        print(f"❌ Error: {e.message}")
