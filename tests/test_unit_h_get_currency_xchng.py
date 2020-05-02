# ---------------------------------------------------------------------------------------------------------------------#
#     Author : KYLASAM N A     Version History : version 1
#     Date   : 2020-05-01
#     Description : The purpose of this script is automate the unit test results
# ---------------------------------------------------------------------------------------------------------------------#
import sys
import unittest
from os import path
from dateutil.parser import parse

sys.path.append(path.abspath('/Users/kylasam/PycharmProjects/CurrencyExchange/src/bin'))
import h_get_currency_xchng as currency_exchange


# ----------------------------------------------------------------------------------------------------------------------#
#  Below class methods performs basic sanity check on the results, data, response and so on.
# ----------------------------------------------------------------------------------------------------------------------#
class CurrencyExchange(unittest.TestCase):
    # Load the configuration values
    def setUp(self):
        self.output_file_location = 'data/output/USD_exchange_rates.csv'
        self.output_file_name = 'USD_exchange_rates.csv'
        self.base_country_for_conversion = "USD"
        self.timestamp_column_index = 33

    # Test the execution only for base country value USD alone [ NO LOOP for other elements ]. Length of list should be 1
    def test_check_currency_list(self):
        result = len(currency_exchange.COUNTRY_CURRENCY)
        self.assertEqual(result, 1)

    # Test the variable value against USD where the execution happen
    def test_check_currency_USD(self):
        self.assertEqual(currency_exchange.COUNTRY_CURRENCY, [self.base_country_for_conversion])

    # Test the dynamically created Output filename based on the base country value
    def test_check_output_filename(self):
        self.assertEqual(currency_exchange.get_currency_rates()[2], self.output_file_name, msg="File Name Error")

    # Check the Header results for not EMPTY values from the API response.
    def test_check_output_header(self):
        self.assertIsNotNone(currency_exchange.get_currency_rates()[0])

    # Check the Conversion list results for not EMPTY values from the API response.
    def test_check_output_currency_list(self):
        self.assertIsNotNone(currency_exchange.get_currency_rates()[1])

    # Check the correspondence between Header & conversion value to have always 1:1
    def test_check_count_for_country_list_vs_currency_list(self):
        self.assertEqual(len(currency_exchange.get_currency_rates()[0]), len(currency_exchange.get_currency_rates()[1]))

    # Appended data should have timestamp ( insertion time value as a last column ) which is of %Y%m%d%H%M%S format.
    def test_timestamp_hourly_extraction_format_for_last_insert(self):
        with open(self.output_file_location, 'r') as f:
            edw_record_insert_time = (list(f)[-1].split(',')[self.timestamp_column_index])
            try:
                parse(edw_record_insert_time)
            except ValueError:
                raise ValueError("Incorrect data format, should be '%Y%m%d%H%M%S'")


if __name__ == '__main__':
    unittest.main()
