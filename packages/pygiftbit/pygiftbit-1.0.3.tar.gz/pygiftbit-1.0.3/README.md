# pygiftbit - A Python Interface for GiftBit

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=DonaldKBrown_pygiftbit&metric=security_rating)](https://sonarcloud.io/dashboard?id=DonaldKBrown_pygiftbit)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DonaldKBrown_pygiftbit&metric=coverage)](https://sonarcloud.io/dashboard?id=DonaldKBrown_pygiftbit)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=DonaldKBrown_pygiftbit&metric=bugs)](https://sonarcloud.io/dashboard?id=DonaldKBrown_pygiftbit)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=DonaldKBrown_pygiftbit&metric=code_smells)](https://sonarcloud.io/dashboard?id=DonaldKBrown_pygiftbit)
![Test with Pytest](https://github.com/DonaldKBrown/pygiftbit/workflows/Test%20With%20Pytest/badge.svg)
![Publish to PyPi](https://github.com/DonaldKBrown/pygiftbit/workflows/Publish%20to%20PyPi/badge.svg)

pygiftbit is a simple API wrapper for the [GiftBit](https://giftbit.com) Gift API so that you can easily send out e-giftcards of various kinds over e-mail. It is designed for you to be able to easily:

* Check for supported gift cards
* Check your account balance
* Fund your account
* Send a gift card of a desired brand and value combination
* Check the status of a sent gift card

Please note, however, that an account with GiftBit **is required** and this library will not function without a valid API key from them.

There are other projects intended for this same purpose. However, they appear to not be in active development and are incomplete. They do not offer the same set of commands or level of documentation as this project.

## Installation

Using `pip`:

```
pip install pygiftbit
```

## Usage

Usage requires simply importing the client and initializing it with your API key and letting it know whether or not you are using the testbed:

```python
from pygiftbit.giftbit import Client

gift_client = Client(api_key="<YOUR_API_KEY>", testing=False)
```

By default, the library uses the testbed. Make sure you declare `testing=false` in your production application.

From there, you have multiple commands available to you:

### Client.list_regions()

This command returns a `dict()` of the available regions as such:

```python
{
    1: 'Canda',
    2: 'USA',
    3: 'Global',
    4: 'Australia'
}
```

### Client.get_brand_codes(**search_arg_modifiers)

This command will list available brand codes with some simple search arguments. There are a few default values:

| Argument Name | Data Type | Default | Description |
| --- | --- | --- | --- |
| region | int | 3 | Specifies the region to search. Use `Client.list_regions()` for a valid list. |
| limit | int | 20 | Specifies how many results to return. |
| offset | int | 0 | Specifies the offset to search by with a limit. |

Other options to search by include:

| Argument Name | Data Type | Description |
| --- | --- | --- |
| search | str | A specific search term to be found in the brand name or description. |
| min_price_in_cents | int | The minium value a gift card can be set to. |
| max_price_in_cents | int | The maximum value a gift card can be set to. |
| currencyisocode | str | Search for gift cards available in either "CAD", "USD", or "AUD". |
| embeddable | bool | If set to true, brands that cannot be used for in-app delivery are omitted. |

For example, if you only wanted to find gift cards with a minimum value of $5 USD in the USA, you could search by:

```python
Client.get_brand_codes(region=2, currencyisocode='USD', min_price_in_cents=500)
```

### Client.brand_info(brand_code)

This command will retrieve detailed information about a brand. the `brand_code` argument is required and should be a string retrieved from `Client.get_brand_codes()`.

### Client.create_campaign(*args)

This command will create a campaign to send gift cards to multiple recipients, allowing them to choose between multiple cards if you wish. Several arguments are needed for this function:

| Argument Name | Data Type | Required | Description |
| --- | --- | --- | --- |
| expiration_date | str | Yes | A `YYYY-MM-DD` formatted date string. After 11:59:59 PM PST on this date, the gifts are no longer redeemable. |
| contacts | list | Yes | A list of contacts to send gifts to. Contacts must be dicts such as `{'firstname': 'John', 'lastname': 'Doe', 'email': 'john.doe@example.com'}` |
| brand_codes | list | Yes | A list of brand codes to offer. Must be valid codes from `Client.get_brand_codes()` |
| price_in_cents | int | Yes | The value of giftcard to send. |
| id | str | Yes | A unique, memorable ID for this campaign. Used for getting campaign status. |
| message | str | Possibly | A custom message to send with the gift card. Only required if gift_template is not supplied. |
| subject | str | Possibly | A custom email subject line to send. Only required if gift_template is not supplied. |
| gift_template | str | Possibly | The name of a template you have created on the website. Required if message and subject are not supplied. |

### Client.check_campaign(id)

This command will fetch the current status of a previously created campaign. The `id` must be a previously created campaign's `user_supplied_id`.

### Client.check_funds()

This command will show you your current available, pending, and reserved funds. Pending funds are funds you have added but have not yet cleared, reserved funds are funds that have been set aside for gifts, but the gifts have not yet been claimed.

### Client.add_funds(currency, amount_in_cents)

This command is used to add funds to your account using the credit card on file for your account. The `currency` argument can be on of "USD" or "CAD", and the `amount_in_cents` can be anything from 25000 and 1000000.

### Client.list_gifts(**filters)

Retrive a list of previously sent gifts and their statuses. For a full set of filters, view the [documentation for the Giftbit API](https://www.giftbit.com/giftbitapi/#/reference/1/gifts/list-gifts).

### Client.get_gift_status(uuid)

Retrieve the status of a single gift by UUID.

### Client.cancel_gift(uuid)

Cancel a previously sent gift and reclaim the funds to your account. Cannot be done if gift is already redeemed.

### Client.resend_gift(uuid)

Resend the email for a previously sent gift. This should be used if a gift was previously set to `TEMPORARILY_UNDELIVERABLE` or if a customer reaches out and says they accidentally deleted the email. This will not generate a new gift or affect your available fund balance.