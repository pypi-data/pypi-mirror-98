'''
Created on 4 Mar 2021

@author: jacklok
'''
from trexlib.utils.common.format_util import format_with_commas

def format_currency(value_2_format=0, currency_label='$', floating_point=2, decimal_separator='.', thousand_separator=',', 
                    show_thousand_separator=True, show_currency_label=False):
    pattern             = u'%.' + str(floating_point)+'f'

    if not show_thousand_separator:
        thousand_separator = ''

    if show_currency_label:
        return '%s %s' % (currency_label, format_with_commas(pattern, value_2_format, thousand_separator, decimal_separator))
    else:
        return format_with_commas(pattern, value_2_format, thousand_separator, decimal_separator)

    
