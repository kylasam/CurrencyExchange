Exchange Rate:
 Foreign exchange rates from Foreign exchange rates API
with currency conversion application that fetches conversion rates for USD in hourly basis.


Source Data:

Data is gathered from https://exchangeratesapi.io/. Exchange rates API is a free service for current and historical foreign exchange rates published by the European Central Bank


In this dataset, granularity is 1 based on the requirement:
•	Hourly

For each extract, one row gets appended in final target file with added timestamp.

Dataset Information:

	/data/output/USD_exchange_rates.csv [ Target file with data append every 1 Hour with added timestamp column]

        The data has following information’s:
	currency rate values from column range A:AG (CSV file)
	EDW_PUBLICATION_ID   Extraction timestamp in YYYYMMDDHHMMSS format.               

	/data/lookup/currency_country_code_lookup.lkp [ Lookup to get the currency and country names]

The data has following information’s:
	Currency_ISO_code
	Currency_name     
	Country_name

Production Deployment:
	Please perform the below steps in sequence for deployment, Unit testing and production scheduling.

•	Clone the repo from GitHub into prod server.
•	Navigate to the HomePath of the project folder
•	Type make and hit Enter,
	Internally make file would be called
	venv set up would be done
	Installing all requirement would happen
	Main script would be called from src/bin/location
•	Type make test to call the unit and Integration tests sequentially.
•	Type make clean-venv to clean the venv and its contents
•	Please look for options in makefile.venv for more options.

Scheduling:
                     Since the requirement is ti run the jobs hourly, please set up the same via Scheduling tools. Shown below is an example of Jenkins set up ( cron or Control-M or Tivoli uses different set up )
 H * * * *

Under Build Plugin:
        
	cd ~/PycharmProjects/CurrencyExchange
        
	.~/PycharmProjects/CurrencyExchange/venv/bin/activate
        
	Python ~/PycharmProjects/CurrencyExchange/src/bin/h_get_currency_xchng.py
	
        deactivate

Automated Test cases:
     Type make test to call the unit and Integration tests sequentially.

Unit testing       : There were 7 test cases written
Integration Testing: There were 8 test cases written



	cd ~/PycharmProjects/CurrencyExchange
        
	kylasam@~/PycharmProjects/CurrencyExchange$ make test

	python3 -m venv /Users/kylasam/PycharmProjects/CurrencyExchange/.venv

	/Users/kylasam/PycharmProjects/CurrencyExchange/.venv/bin/python -m pip install --upgrade pip setuptools
	Collecting pip
  	Using cached https://files.pythonhosted.org/packages/54/2e/df11ea7e23e7e761d484ed3740285a34e38548cf2bad2bed3dd5768ec8b9/pip-20.1-py2.py3-none-any.whl
	Collecting setuptools
  	Using cached https://files.pythonhosted.org/packages/a0/df/635cdb901ee4a8a42ec68e480c49f85f4c59e8816effbf57d9e6ee8b3588/setuptools-46.1.3-py3-none-any.whl
	Installing collected packages: pip, setuptools
  	Found existing installation: pip 19.2.3
  	  Uninstalling pip-19.2.3:
   	   Successfully uninstalled pip-19.2.3
 	 Found existing installation: setuptools 41.2.0
   	 Uninstalling setuptools-41.2.0:
   	   Successfully uninstalled setuptools-41.2.0
		Successfully installed pip-20.1 setuptools-46.1.3
	/Users/kylasam/PycharmProjects/CurrencyExchange/.venv/bin/pip install -r requirements.txt
	Collecting python-dateutil
	  Using cached python_dateutil-2.8.1-py2.py3-none-any.whl (227 kB)
	Collecting requests
	  Using cached requests-2.23.0-py2.py3-none-any.whl (58 kB)
	Collecting console
	  Using cached console-0.990-py2.py3-none-any.whl (74 kB)
	Collecting six>=1.5
	  Using cached six-1.14.0-py2.py3-none-any.whl (10 kB)
	Collecting chardet<4,>=3.0.2
	  Using cached chardet-3.0.4-py2.py3-none-any.whl (133 kB)
	Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1
	  Using cached urllib3-1.25.9-py2.py3-none-any.whl (126 kB)
	Collecting certifi>=2017.4.17
	  Using cached certifi-2020.4.5.1-py2.py3-none-any.whl (157 kB)
	Collecting idna<3,>=2.5
	  Using cached idna-2.9-py2.py3-none-any.whl (58 kB)
	Collecting ezenv
	  Using cached ezenv-0.91-py2.py3-none-any.whl (10 kB)
	Installing collected packages: six, python-dateutil, chardet, urllib3, certifi, idna, requests, ezenv, console
	Successfully installed certifi-2020.4.5.1 chardet-3.0.4 console-0.990 ezenv-0.91 idna-2.9 python-dateutil-2.8.1 requests-2.23.0 six-1.14.0 urllib3-1.25.9
	touch /Users/kylasam/PycharmProjects/CurrencyExchange/.venv/bin/.initialized-with-Makefile.venv
	/Users/kylasam/PycharmProjects/CurrencyExchange/.venv/bin/python -m unittest tests/test_unit_h_get_currency_xchng.py
	.......
	----------------------------------------------------------------------
	Ran 7 tests in 0.779s
	
	OK
	/Users/kylasam/PycharmProjects/CurrencyExchange/.venv/bin/python -m unittest tests/test_integration_h_get_currency_xchng.py
	.3
	.......
	----------------------------------------------------------------------
	Ran 8 tests in 1.410s
	
	OK
