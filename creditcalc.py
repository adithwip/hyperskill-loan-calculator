import argparse
import math

type_of_payment = None
p_loan_principal = 0
a_annuity_monthly_payment = 0
n_number_of_payment_periods = 0  # Or number of periods. e.g. 10 months of payments periods
i_loan_interest = 0
months_to_repay = 0  # The value of calculated type 'n'
annuity_monthly_payment = 0  # The value of calculated type 'a'
loan_principal = 0  # The value of calculated type 'p'


def raw_user_input_parser(raw_user_input):
    decimal_point = '.'
    if raw_user_input is None:
        return None
    elif decimal_point in raw_user_input:
        return float(raw_user_input)
    else:
        return int(raw_user_input)


def get_years_from_months():
    return n_number_of_payment_periods // 12


def get_remaining_months():
    return n_number_of_payment_periods % 12


def parse_months_to_repay_to_sentence():
    years = get_years_from_months()
    remaining_months = get_remaining_months()

    if years > 0 and remaining_months > 0:
        return f"It will take {years} years and {remaining_months} months to repay this loan!"
    if years == 0 and remaining_months > 0:
        return f"It will take {remaining_months} months to repay this loan!"
    if years > 0 and remaining_months == 0:
        return f"It will take {years} years to repay this loan!"
    if years == 1 and remaining_months == 0:
        return f"It will take {years} year to repay this loan!"


def calculate_interest_rate():
    return (i_loan_interest / 100) / 12 * (100 / 100)


def calculate_number_of_monthly_payment():  # The formula of `n = log 1 + i (A / A − i ∗ P)`
    i = calculate_interest_rate()
    a = a_annuity_monthly_payment
    p = p_loan_principal

    x = (a / (a - i * p))
    log_base = 1 + i

    n = math.log(x, log_base)

    # Round up the number of monthly payments
    return math.ceil(n)


def calculate_annuity_monthly_payment():
    p = p_loan_principal
    n = n_number_of_payment_periods
    i = calculate_interest_rate()

    a = p * ((i * ((1 + i) ** n)) / (((1 + i) ** n) - 1))

    return math.ceil(a)


def calculate_loan_principal():
    a = a_annuity_monthly_payment
    i = calculate_interest_rate()
    n = n_number_of_payment_periods

    p = a / ((i * ((1 + i) ** n)) / (((1 + i) ** n) - 1))

    return math.floor(p)


def calculate_differentiate(m):
    p = p_loan_principal
    n = n_number_of_payment_periods
    i = calculate_interest_rate()

    d = p / n + (p - (m - 1) * (p / n)) * i
    return math.ceil(d)


def process_differentiate_payment():
    total_payments = 0
    for m in range(1, n_number_of_payment_periods + 1):
        diff = calculate_differentiate(m)
        total_payments += diff
        print(f"Month {m}: payment is", diff)

    print(f"Overpayment =", total_payments - p_loan_principal)


def process_annuity_payment():
    global a_annuity_monthly_payment
    a_annuity_monthly_payment = calculate_annuity_monthly_payment()
    print(f"You annuity payment =", a_annuity_monthly_payment)
    print(f"Overpayment =", (a_annuity_monthly_payment * n_number_of_payment_periods) - p_loan_principal)


def process_loan_principal():
    global p_loan_principal
    p_loan_principal = calculate_loan_principal()
    print("Your loan principal =", p_loan_principal)
    print(f"Overpayment =", (a_annuity_monthly_payment * n_number_of_payment_periods) - p_loan_principal)


def process_payment_periods():
    global n_number_of_payment_periods
    n_number_of_payment_periods = calculate_number_of_monthly_payment()
    print(parse_months_to_repay_to_sentence())
    print(f"Overpayment =", (a_annuity_monthly_payment * n_number_of_payment_periods) - p_loan_principal)


class CheckNegative(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if raw_user_input_parser(values) < 0:
            # raise argparse.ArgumentTypeError(f"{option_string} value must be positive, but got {values}")
            print('Incorrect parameters')
            exit()
        setattr(namespace, self.dest, values)


def parse_user_input():
    global type_of_payment
    global p_loan_principal
    global a_annuity_monthly_payment
    global n_number_of_payment_periods
    global i_loan_interest

    parser = argparse.ArgumentParser(description="This program will help you calculate your debt.")

    parser.add_argument("--type", choices=["annuity", "diff"],  # type_of_payment
                        help="Incorrect parameters. Choose one from 'annuity' or 'diff.'")
    parser.add_argument("--payment",  # a_annuity_monthly_payment
                        help="Annuity monthly payment.", action=CheckNegative)
    parser.add_argument("--principal",  # p_loan_principal
                        help="Loan principal.", action=CheckNegative)
    parser.add_argument("--periods",  # n_number_of_payment_periods
                        help="Number of payment periods.", action=CheckNegative)
    parser.add_argument("--interest",  # i_loan_interest
                        help="Interest rate.",
                        action=CheckNegative)

    args = parser.parse_args()

    type_of_payment = args.type
    p_loan_principal = raw_user_input_parser(args.principal)
    a_annuity_monthly_payment = raw_user_input_parser(args.payment)
    n_number_of_payment_periods = raw_user_input_parser(args.periods)
    i_loan_interest = raw_user_input_parser(args.interest)

    all_available_arguments = [type_of_payment, p_loan_principal, a_annuity_monthly_payment,
                               n_number_of_payment_periods,
                               i_loan_interest]
    num_provided_args = sum(arg is not None for arg in all_available_arguments)

    if num_provided_args < 4:
        print('Incorrect parameters.')
        exit()
    elif args.type == 'diff':
        if a_annuity_monthly_payment is not None:
            print("Incorrect parameters")
            exit()
        process_differentiate_payment()
        exit()
    elif args.type == 'annuity':
        if a_annuity_monthly_payment is None:
            process_annuity_payment()
        if p_loan_principal is None:
            process_loan_principal()
        if n_number_of_payment_periods is None:
            process_payment_periods()


def main():
    parse_user_input()


main()
