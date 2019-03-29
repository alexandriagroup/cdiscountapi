# CdiscountApi

Python interface to the CdiscountMarketplace API.

* Get the seller information

    c = Connection(login, password)
    seller_info = c.seller.get_seller_info()


## Development

### Tests

We use vcrpy to mock the HTTP requests. It is recommended to install libyaml
before installing vcrpy in order to increase its speed.

    sudo apt install libyaml-dev

* Run the tests using the cassettes recorded previously

    make test-no-vcr

* Run the tests by sending the requests to the server. (They are then recorded in the cassettes)

    make test-renew-vcr-records
