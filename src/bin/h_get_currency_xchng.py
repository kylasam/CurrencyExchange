# -------------------------------------------------------------------------------------------------------------------------------#
#     Author : KYLASAM N A     Version History : version 1
#     Date   : 2020-04-30
#     Description : The purpose of this script is to perform the data extraction from Currency exchange API for list of Countries
# -------------------------------------------------------------------------------------------------------------------------------#
import requests
import json
import logging
from datetime import datetime
import os, sys
import csv
from pathlib import Path

LOG_FILE_NAME = datetime.now().strftime(
    'logs/' + os.path.basename(sys.argv[0]).strip(".py") + '_%Y%m%d%H%M%S.log')
logging.basicConfig(filename=LOG_FILE_NAME,
                    format='%(levelname)s::%(asctime)s.%(msecs)03d  From Module = ":%(funcName)s:" Message=> %(message)s.',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

COUNTRY_CURRENCY = ["USD"]
URL = "https://api.exchangeratesapi.io/latest?base="
TARGET_FILE_LOCATION = "data/output/"
TARGET_FILE_SUFFIX = "_exchange_rates.csv"


# ----------------------------------------------------------------------------------------------------------------------#
#  Below mentioned module builds the URL based on country value and extracts the results and returns Header,Conversion rate
# ----------------------------------------------------------------------------------------------------------------------#

def get_currency_rates():
    for currency in COUNTRY_CURRENCY:
        OUTPUT_FILE = currency + TARGET_FILE_SUFFIX
        currency_conversion_factor, header_row = [], []
        logging.info("Target file for dumping the data would be : " + OUTPUT_FILE)
        url = URL + currency
        logging.info("URL : " + url)
        response = requests.get(url).text
        parsed = json.loads(response)
        rates = parsed["rates"]
        for k, v in rates.items():
            header_row.append(k)
            currency_conversion_factor.append(v)
        return header_row, currency_conversion_factor, OUTPUT_FILE


# ----------------------------------------------------------------------------------------------------------------------#
#  Below mentioned module adds enterprise data warehouse publication id ( timestamp ) with results and appends CSV file
# ----------------------------------------------------------------------------------------------------------------------#


def data_dump_to_csv(header, currency_value, target_file):
    header.append("edw_publication_id")
    currency_value.append(datetime.now().strftime('%Y%m%d%H%M%S'))
    logging.info(
        "Header row from the API would be =" + str(header) + " and the currency value is = " + str(currency_value))
    logging.info("The extraction TIMESTAMP=" + datetime.now().strftime('%Y%m%d%H%M%S'))
    target_file = Path(TARGET_FILE_LOCATION + target_file)
    logging.info("Try block to dump the data into CSV file at " + str(target_file))
    try:
        with open(target_file, "a+", newline='') as fp:
            writer = csv.writer(fp, dialect='excel')
            if os.stat(target_file).st_size == 0:
                writer.writerow(header)
                writer.writerow(currency_value)
            else:
                writer.writerow(currency_value)
    except Exception as err:
        logging.error("One or More file transactions FAILED!!! Error Details =" + str(err))
        exit(100)
    else:
        logging.info("File Transcations completed successfully!!. File is found at " + str(target_file))


# ----------------------------------------------------------------------------------------------------------------------#
#  Below mentioned module invokes the User defined modules sequentially
# ----------------------------------------------------------------------------------------------------------------------#

def main():
    logging.info("Invoking main function")
    Header, conversion_value, target_file = get_currency_rates()
    data_dump_to_csv(Header, conversion_value, target_file)


if __name__ == '__main__':
    logging.info("Executing Currency Exchange Extractor job..")
    main()
