
# Healthier alimentation products finder

This application aims to help the user finds substitutes for all food related products. Based on a selection of product, this application will offer alternatives with a better nutrition grade (nutriscore in French). The user can then decide to save this alternative (or not) and review the saved alternatives.

##

## *The open food fact initiative:*

For more information please refer to: https://fr.openfoodfacts.org/

This application uses the open food fact API.

Open Food Facts is a non-profit project developed by thousands of volunteers from around the world.

As the data comes from volunteers, it might be incomplete and even sometimes not accurate, please use the information from this application with caution.

## Environment variables:
In order for this project to run, you need some environment variables.
The ones you need are all listed in the example.env file, please update this file with your database credentials and django secret key and then save it under the ".env" name.
**The other variables in this file are used for functionnal tests, please do not modify them**
  

## *Database connection parameters:*

Regarding the connection to your database, **please replace the values in the "DB credentials section of the example.env file** and then rename/setup this file to use it as source for your project environment variables.

  
## Requirements:

All required packages to run this app are listed in the requirements.txt file.

To install all requidred packages, please run

    pip install -r requirements.txt

  

## *Specific manage.py commands*


### Drop databases table:

There is a specific manage.py command to drop the 4 following tables from database:

- User (except admin, user id n°1)

- Product

- Favorites

- Categories

  

**USE WITH CAUTION, DATA CAN BE LOST USING THIS**

if you want to erase the four above tables, please use:

  

    python manage.py resetdb

  

## Import new data from teh open food fact API:

To import a new batch of products in the database you can use the following command:

  

    python manage.py fetch_api_data

  

## *Tests*


### Run tests

use the following command:

    python manage.py test

  

### Run functionnal tests only

For functionnal tests only regarding the *authentification* app:

    python manage.py test authentification.tests.tests_functionnals.MySeleniumTests

  

For functionnal tests only regarding the *substitution* app:

    python manage.py test substitution.tests.tests_functionnals.MySeleniumTests

  

### Run unitary tests only

For unitary tests only regarding the substitution app:

python manage.py test substitution.tests.tests_unitary

  
  

### *Tests coverage report*


To get a coverage report, please run

    coverage run manage.py test

And then:

    coverage report

  

*information:* the coverage report configuration is set in rootfolder in .coveragerc file, it excludes all the virtual environment files located in the 'envp8' directory.

  

## PEP8 compliance

Use of flake 8

There is a .flake8 configuration file in the root directory to exclude django generated files such as migrations and cache.