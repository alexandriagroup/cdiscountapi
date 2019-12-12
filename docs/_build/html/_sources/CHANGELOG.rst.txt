.. _changelog:


Change log
==========

All notable changes to this project will be documented in this file.
The format is based on `Keep a Changelog`_ and this project adheres to
`Semantic Versioning`_.


[0.1.11] - 2019-12-12
---------------------

Fixed
*****

* Fix bugs with the path of the templates.


[0.1.10] - 2019-12-12
---------------------

Fixed
*****

* Fix a bug in `OfferValidator` and `ProductValidator`.


[0.1.9] - 2019-12-11
--------------------

Fixed
*****

* Fix a bug in `generate_package`.


[0.1.8] - 2019-12-11
--------------------

Fixed
*****

* Add missing requirements.


[0.1.7] - 2019-12-11
--------------------

Fixed
*****

* Improve `overwrite` in `generate_package`.
  Both the zip file and the directory are deleted when `overwrite=True`


[0.1.6] - 2019-12-10
--------------------

Fixed
*****

* Fix a path issue with in `generate_package`


[0.1.5] - 2019-10-04
--------------------

Changed
*******

* Update the main dependencies


[0.1.4] - 2019-09-06
--------------------

Added
*****

* New optional argument `package_type` in `generate_offers_package`
* New optional argument `overwrite` in `generate_offers_package`: allows to
  overwrite an existing package
* `Orders.get_order_list` automatically adds the other date parameter
  in the order (because it is required by the API)
  (i.e BeginCreationDate and BeginModificationDate must be specified together.
  Idem for EndCreationDate and EndModificationDate.)

Fixed
*****

* Some tests are improved (more accurate and mocked)
* Fix `Offers.get_offer_list_paginated`. (Bug: only the first
  SellerProductIdList was taken into account)


[0.1.3] - 2019-08-06
--------------------

Added
*****

* New argument `package_name` in `generate_offers_package`: sets the value of
  the attribute Name of the OfferPackage in the XML


[0.1.2] - 2019-07-26
--------------------

Fixed
*****

* Add a missing dependency (PyYAML).


[0.1.1] - 2019-07-25
--------------------

* First release.


.. _Keep a changelog: http://keepachangelog.com/ 
.. _Semantic Versioning: http://semver.org/
