django-datatrans-gateway
========================

[![Build Status](https://travis-ci.org/skioo/django-datatrans-gateway.svg?branch=master)](https://travis-ci.org/skioo/django-datatrans-gateway)
[![PyPI version](https://badge.fury.io/py/django-datatrans-gateway.svg)](https://badge.fury.io/py/django-datatrans-gateway)
[![Requirements Status](https://requires.io/github/skioo/django-datatrans-gateway/requirements.svg?branch=master)](https://requires.io/github/skioo/django-datatrans-gateway/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/skioo/django-datatrans-gateway/badge.svg?branch=master)](https://coveralls.io/github/skioo/django-datatrans-gateway?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A django integration for the datatrans payment gateway.

Supports:
- Direct payment by the user.
- Registration of a credit card alias by the user, followed by one or more charges (without the user being present).
- Refund (total or partial) of a previous successful charge.


This implementation:
- Handles the exchanges with datatrans, including the signing of requests and the verification of the signature of notifications. All exchanges are logged as structured events, to make auditing easy.
- Introduces persistent models for AliasRegistration, Payment, and Refund. Both successes and failures are stored.
- Offers a rich admin interface, allowing ad-hoc payments using registered credit cards, as well as refunds. 
- Sends signals whenever an AliasRegistration, Payment, or Refund is done. The signal is sent even if the operation failed, 
the receiver should check the `success` flag received with the signal.


Requirements
------------

* Python: 3.6 and over
* Django: 2.0 and over


Usage
-----

Add datatrans to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'datatrans.apps.DatatransConfig',
    )


Include `datatrans-urls` to the urlpatterns in your urls.py, for instance:

    urlpatterns = [
        url(r'^datatrans/', include('datatrans.urls')),
    ]

Configure the callback url in the datatrans UPP Administration page.

In your settings.py, enter the configuration for your web and mpo merchants. For instance:

    DATATRANS = {
        'WEB_MERCHANT_ID': '1111111111',
        'WEB_HMAC_KEY': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
        'MPO_MERCHANT_ID': '2222222222',
        'MPO_HMAC_KEY': 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    }


Troubleshooting
---------------

If you don't see a payment (or a payment error) in the database, and you are sure you've properly configured the callback in the upp,
then start by looking in the log for a `datatrans-notification`.


Development
-----------

To install all dependencies:

    pip install -e .


To run tests:

    pip install pytest-django
    pytest


To lint, typecheck, test, and verify you didn't forget to create a migration:

    pip install tox
    tox


To install the version being developed into another django project:

    pip install -e <path-to-this-directory>
