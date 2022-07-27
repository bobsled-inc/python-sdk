# Bobsled Python SDK
> A Python library to interact with Bobsled

![](header.png)

## Installation

```sh
pip install bobsled-python-sdk
```

## Usage example

```sh
from bobsled_sdk import BobsledClient

credentials = { "email": "ex@mple.com", "password": "example"}

b = BobsledClient(credentials)
```

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

```sh
pip install -r requirements.txt
pytest tests
```

## Release History

* 0.0.1
    * Work in progress

## Meta

Danny Yu – danny@berkeley.edu

Distributed under the MIT License. See ``LICENSE`` for more information.

[https://github.com/danny-yu](https://github.com/danny-yu)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
