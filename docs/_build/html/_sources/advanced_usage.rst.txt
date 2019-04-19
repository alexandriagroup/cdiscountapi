.. _advanced_usage:


Advanced usage
==============

Get the latest request and response
-----------------------------------

::
    
  >>> api.seller.get_seller_information()
  >>> api.latest_request
  >>> api.latest_response


Use a configuration file
------------------------

You can use a YAML configuration file to store the information used in the HeaderMessage_. 

For example:

.. code-block:: yaml

    Version: '1.0'

    Context:
        SiteID: 100
        CatalogID: 1
        CustomerNumber: XXX

    Localization:
        Country: 'Fr'
        Currency: 'Eur'
        DecimalPosition: 2

    Security:
        UserName: ''
        SubjectLocality:
            Address: XXX
            DnsName: XXX

.. note:: 
   
   1. The field TokenId doesn't have to be provided as it will be retrieved
      automatically.

   2. The fields not provided will have default values:

   - SiteID: 100
   - CatalogID: 1

   ``None`` for all the other fields.
    
.. _HeaderMessage: https://dev.cdiscount.com/marketplace/?page_id=212
