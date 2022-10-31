# Interfaces (Storages)
[![codecov](https://codecov.io/gh/MarkTLite/interfaces-storages/branch/main/graph/badge.svg?token=D1GG1EUSJL)](https://codecov.io/gh/MarkTLite/interfaces-storages)
![Test status](https://github.com/MarkTLite/interfaces-storages/actions/workflows/testcov.yml/badge.svg)
![Build Status](https://github.com/MarkTLite/landing-page-react/actions/workflows/heroku_deployer.yaml/badge.svg)

## Description
 This project involves the application of design patterns to develop an image storage app with the following advantages:
 - High extensibility (Storage Providers' function definitions like for dropbox can be added without complicating the codebase at all)
 - Dependency change does not fail the system

### Concepts applied
- Storage providers: Aws_S3, local disk storage
- Interfaces
- Dependency Injection
- Test driven development

## Adding Providers
add commandline argument for the new provider in the tests file
Make sure the test_databases.py tests even when unchanged pass for your newly added providers' logic

## Running Tests
pip install coverage<br>
Run tests for each provider in this format:<br/>
<code>
coverage run tests\test_storages.py aws_s3 
</code>
<br/>
where "aws_s3" is one of:
- aws_s3
- filesystem

### Getting coverage
use -a to append individual tests<br/>
<code>
coverage run tests\test_storages.py aws_s3 && coverage run -a tests\test_storages.py filesystem
</code><br/>
then <br/>
<code>coverage report</code>

## Environment files
Add these files in the /providers folder before running.
### .env for aws_s3
    aws_access_key_id = ***
    aws_secret_access_key = ***
    region=***



