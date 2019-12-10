# CdiscountApi

Python interface to the CdiscountMarketplace API.

* Get the seller information:

```python
c = Connection(login, password)
seller_info = c.seller.get_seller_info()
```

## Development

[konch](https://konch.readthedocs.io/en/latest/) is really useful to help in
interactive development. If you want to use it, make sure to export the
environment variables **CDISCOUNT_API_LOGIN**
and **CDISCOUNT_API_PASSWORD** and run:

``` sh
konch
```

in your terminal, in the project directory.

### Tests

We use vcrpy to mock the HTTP requests. It is recommended to install libyaml
before installing vcrpy in order to increase its speed.

```sh
sudo apt install libyaml-dev
```

* Install the requirements for the development:

```sh
make install-dev
```

* Run the tests using the cassettes recorded previously:

```sh
make test
```

* Run the tests by sending the requests to the server. (They are then recorded in the cassettes):

```sh
make test-renew-vcr-records
```

* Run all the tests (including those necessiting real data)

```sh
  CDISCOUNT_WITHOUT_DATA=0 make test
```

by default `CDISCOUNT_WITHOUT_DATA` equals 1. By setting this environment
variable to 0, the tests may fail if no real data there are available (and no
cassette is available)

### Contribute to the project

* Render the documentation:

```sh
make docs
```

* Publish a release on pypi

```sh
make publish
```

You can also just build the package without publishing it with:

```sh
make build
```
