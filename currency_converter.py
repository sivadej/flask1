from flask import Flask, redirect, session, request, url_for, flash
from decimal import *
from forex_python.converter import CurrencyRates, CurrencyCodes
from session_validator import validate_data, make_uppercase_and_decimal

# instantiate rate converter
c = CurrencyRates()
s = CurrencyCodes()

def get_result_msg():
    session_data = {
        'convert_from' : session['convert_from'],
        'convert_to' : session['convert_to'],
        'amount' : session['amount'],
    }
    update_session_data(make_uppercase_and_decimal(session_data))
    if validate_data(session_data) is True:
        return get_conversion_msg()
    else:
        return ''
    
def get_conversion_msg():
    """ Returns string with message showing final conversions. Amounts are rounded to two decimal places.
    This function should only be called with validated inputs stored in session. """

    # Determine and assign currency symbols.
    
    symbol_from = s.get_symbol(session['convert_from'])
    symbol_to = s.get_symbol(session['convert_to'])

    # Get converted amount and generate string to be displayed
    converted_amount = get_converted_amount()
    success_msg = f"{symbol_from} {round(session['amount'],2)} = {symbol_to} {converted_amount}"
    return success_msg

def get_converted_amount():
    amt = c.convert(session['convert_from'], session['convert_to'], session['amount'])
    return round(amt,2)

def update_session_data(data):
    session['convert_from'] = data['convert_from']
    session['convert_to'] = data['convert_to']
    session['amount'] = data['amount']

def update_session_from_form(form_data):
    session['convert_from'] = form_data['conv_from']
    session['convert_to'] = form_data['conv_to']
    session['amount'] = form_data['amount']

def clear_session():
    session['convert_from'] = ''
    session['convert_to'] = ''
    session['amount'] = ''