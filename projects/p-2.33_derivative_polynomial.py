"""
P-2.33: Write a Python program that inputs a polynomial in standard algebraic
notation and outputs the first derivative of that polynomial.

To find the derivative of polynomials, make use of the power rule:
For a real number n, (d/dx)f(x) = nx^(n-1)

What is our input?
Likely a string of some kind that we will need to parse
and extract the "parts" that make up a polynomial.
What are the parts of a polynomial?

Example: 4x^2 + 3x - 5
---
Coefficient(s): 4, 3
Variable(s): x
Exponent(s): 2
Constant(s): 5
"""

simple_example = "x^2"

for i, char in enumerate(simple_example):
    print(char)