#!/usr/bin/env python3

"""Calculate deposit percent yield based on time period.

Imagine your friend wants to put money on a deposit.
He has got many offers from different banks:
- First bank declares +A% each day;
- Second bank promises +B% each month;
- Third bank offers +C% by the end of the year;
- The 4th bank promotes +D% in a 10-year term;
- ... and so on ...

Your friend gets a terrible headache calculating all this stuff,
and asks you to help checking everything. You quickly realize
it is a common task and having a simple script is a great idea.

Let's implement this.

A simplified task:
Given the SUM amount of money, and PERCENT yield promised in a
FIXED_PERIOD of time, calculate the TOTAL equivalent of money
in a SET_PERIOD of time.

Math formula:
p = PERCENT / 100
TOTAL = SUM * ((1 + p) ** (SET_PERIOD / FIXED_PERIOD))
"""


# TODO: add lines to calculate yields for some common periods
#       of time (e.g. 1 month, 1 year, 5 years, 10 years)
# TODO: change the script to output the 1-year percent yield
#       as well
# TODO: (extra) Output only percents if the initial SUM is
#       not known at the moment the script is run


USAGE = """USAGE: {script} initial_sum percent fixed_period set_period

Calculate deposit yield. See script source for more details.
All time periods shell be set in days.
If initial_sum is unknown, enter 0 to calculate percentage.
All output data are provided in gross, exept 1-year percent yield.
"""
USAGE = USAGE.strip()

MONTH = 30
YEAR = 365
FIVE_YEAR = 1826
TEN_YEAR = 3652

def deposit(initial_sum, percent, fixed_period, set_period):
    """Calculate deposit yield."""

    per = 1 + percent / 100
    percents = (
        per ** (set_period / fixed_period),
        per ** (MONTH / fixed_period),
        per ** (YEAR / fixed_period),
        per ** (FIVE_YEAR / fixed_period),
        per ** (TEN_YEAR / fixed_period),
    )
    result = tuple(map(lambda x: x * initial_sum, percents)) if initial_sum else percents

    return result, percents[2] - 1  # year_per


def main(args: list):
    """Gets called when run as a script."""

    if len(args) != 4 + 1:
       exit(USAGE.format(script=args[0]))

    args = args[1:]

    initial_sum, percent, fixed_period, set_period = map(float, args)

    res, year_per = deposit(initial_sum, percent, fixed_period, set_period)
    var_names = ['set period %s', 'one month %s', 'one year %s', 'five year %s', 'ten year %s']
    def format_output(pair):
        name, x = pair
        name %= 'yield' if initial_sum else '%'
        x *= 1 if initial_sum else 100
        return '%s = %.2f' % (name, x)
    for line in map(format_output, zip(var_names, res)):
        print(line)
    print('one year % net = ', round(year_per * 100, 2))

if __name__ == '__main__':
    import sys

    main(sys.argv)
