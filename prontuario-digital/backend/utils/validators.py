"""
Validadores para documentos brasileiros
"""


class cpf:
    def slice_cpf_to_int(self, cpf):
        return [int(digit) for digit in cpf]

    def validate_cpf(self, cpf):
        org_digits = self.slice_cpf_to_int(cpf)
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


if __name__ == "__main__":
    cpf1 = cpf()
    cc = "12345678909"
    print(cpf1.validate_cpf(cc))
