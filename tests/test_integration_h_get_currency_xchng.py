# ---------------------------------------------------------------------------------------------------------------------#
#     Author : KYLASAM N A     Version History : version 1
#     Date   : 2020-05-01
#     Description : The purpose of this script is automate the complex scenario based Integration Testing
# ---------------------------------------------------------------------------------------------------------------------#
import unittest
import sys, os
from os import path
import requests
from pathlib import Path

sys.path.append(path.abspath('/Users/kylasam/PycharmProjects/CurrencyExchange/src/bin'))
import h_get_currency_xchng as currency_exchange


def assert_response(resp):
    assert resp.status_code == 200
    assert resp.reason == "OK"


def read_report_file(filename):
    with open(filename, 'r') as f:
        report_file_contents = f.read().split('\n')
        return report_file_contents


# ----------------------------------------------------------------------------------------------------------------------#
#                   Below class methods performs API related tests and on response results
# ----------------------------------------------------------------------------------------------------------------------#
class TestResponse(unittest.TestCase):
    # set up basic variables for reuse in various modules
    def setUp(self):
        self.country = currency_exchange.COUNTRY_CURRENCY[0]
        self.url = currency_exchange.URL

    def test_api_get_response(self):
        response = requests.get(self.url + self.country)
        assert response.status_code == 200

    def test_response_for_United_states_conversion_in_JSON(self):
        response = requests.get(self.url + self.country)
        assert response.headers['content-Type'] == "application/json"

    def test_response_for_United_states_filter(self):
        response = requests.get(self.url + self.country)
        response_body = response.json()
        assert response_body["base"] == "USD"


# ----------------------------------------------------------------------------------------------------------------------#
#                   Below class methods performs testing on the dumped report file.
# ----------------------------------------------------------------------------------------------------------------------#
class TestOutputFile(unittest.TestCase):
    # set up basic variables for reuse in various modules
    def setUp(self):
        # load test data
        self.output_file_name = 'data/output/USD_exchange_rates.csv'
        self.tota_number_of_columns = 34
        self.country = currency_exchange.COUNTRY_CURRENCY[0]

    # Test for the report file Existence
    def test_report_file_existance(self):
        try:
            self.assertTrue(os.stat(Path(self.output_file_name)).st_size)
        except FileNotFoundError:
            print("job Han't run yet!!")

    # Compare the Header results from File and the response, based on no.of columns to make sure any new added rate is
    # efficiently caught by our testing
    def test_file_contents_for_header_and_data_values(self):
        with open(self.output_file_name, 'r') as f:
            self.assertIn(",".join(currency_exchange.get_currency_rates()[0]), f.readline())
            length_of_body_record = len(f.read().split(","))
            self.assertEqual(length_of_body_record, self.tota_number_of_columns)


# ----------------------------------------------------------------------------------------------------------------------#
#           Below class methods performs Scenario based testing on delete and recreate, append methodology
# ----------------------------------------------------------------------------------------------------------------------#
class TestComplexData(unittest.TestCase):
    #set up basic variables for reuse in various modules
    def setUp(self):
        self.output_file_name = 'data/output/USD_exchange_rates.csv'
        self.tota_number_of_columns = 34
        self.country = currency_exchange.COUNTRY_CURRENCY[0]

    #delete the file and recreate with Header row and one line of api response row
    def test_delete_recreate_file_with_header(self):
        # Upon the file is missing, while creating the file, file should have both Header and body records
        try:
            os.remove(self.output_file_name)
        except FileNotFoundError:
            print("File doesn't exist!")

        self.assertFalse(os.path.isfile(self.output_file_name))
        currency_exchange.main()
        file_contents = read_report_file(self.output_file_name)
        self.assertEqual(sum(1 for line in file_contents if line), 2)  # Header, first data record

    #Test scenario on just appending the data with timestamp
    def test_data_append_without_header(self):
        # try appending a line into the file and we should see the count as 3 without duplicating Header row
        self.assertTrue(os.path.isfile(self.output_file_name))
        file_contents = read_report_file(self.output_file_name)
        previous_count_before_execution = sum(1 for line in file_contents if line)
        currency_exchange.main()
        file_contents = read_report_file(self.output_file_name)
        print(sum(1 for line in file_contents if line))
        self.assertEqual(sum(1 for line in file_contents if line), previous_count_before_execution + 1)  # Header, first data record and empty 3rd line
        currency_exchange.main()

    # Test scenario for response validation for USD
    def test_USD_value_in_respose(self):
        index_value_for_USD_from_responses = currency_exchange.get_currency_rates()[0].index(self.country)

        # Test the index for USD and the value from Header row
        self.assertEqual(currency_exchange.get_currency_rates()[0][index_value_for_USD_from_responses], self.country)
        # Test the index for USD and the value from conversion list row
        self.assertEqual(currency_exchange.get_currency_rates()[1][index_value_for_USD_from_responses], 1.0)


if __name__ == '__main__':
    unittest.main()
