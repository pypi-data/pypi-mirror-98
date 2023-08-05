[![Build status](https://github.com/jamsidedown/sawpit/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/jamsidedown/sawpit/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

# sawpit
## Work in progress fork/continuation of [pywsitest](https://github.com/gridsmartercities/pywsitest)

A python API to assist with automated websocket integration testing

## Installation
```
// TODO
```

## Package contents
### [WSTest](https://github.com/jamsidedown/sawpit/blob/main/sawpit/ws_test.py)
WSTest is the main test running class in sawpit. It currently has the following methods:
- **with_parameter**: add a query parameter to the connection
- **with_header**: add a header to the connection
- **with_response**: add an expected response to the test runner
- **with_message**: add a message for the test runner to send on connection
- **with_request**: attach a rest api request to the instance of this class
- **with_response_timeout**: set the timeout in seconds for the test runner to wait for a response from the websocket
- **with_message_timeout**: set the timeout in seconds for the test runner to wait while trying to send a message to the websocket
- **with_request_timeout**: set the timeout in seconds for the rest request attached to the instance of this class
- **with_test_timeout**: set the timeout in seconds for the test runner to run for
- **with_received_response_logging**: enable logging of received responses on response timeout error
- **run**: asyncronously run the test runner, sending all messages and listening for responses
- **is_complete**: check whether all expected responses have been received and messages have been sent

### [WSResponse](https://github.com/jamsidedown/sawpit/blob/main/sawpit/ws_response.py)
WSResponse is a class to represent an expected response from the websocket
- **with_attribute**: add an attribute to check an incoming response against
- **with_trigger**: add a message to trigger when a response matching this instance has been received
- **is_match**: check whether a received response matches the attributes of this instance

### [WSMessage](https://github.com/jamsidedown/sawpit/blob/main/sawpit/ws_message.py)
WSMessage is a class to represent a message to send to the websocket
- **with_attribute**: add an attribute to the message to be sent to the websocket host
- **with_delay**: add a delay to the message to be sent to the websocket host

### [RestRequest](https://github.com/jamsidedown/sawpit/blob/main/sawpit/rest_request.py)
RestRequest is a class to represent a request to send to rest api
- **with_header**: add a header to the request to be sent to the rest api
- **with_body**: add a body to the request to be sent to the rest api
- **with_delay**: add a delay to the request to be sent to the rest api

## Examples

### Response testing
Testing a response with a body is received on connection to a websocket host:
```py
from sawpit import WSTest, WSResponse

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Testing that a response with the following more complicated body is received on connection to a websocket host:
```json
{
    "body": {
        "attribute": "value"
    }
}
```

```py
from sawpit import WSTest, WSResponse

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body")
        .with_attribute("body/attribute", "value")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Testing that a response with the following body with a list is received on connection to a websocket host:
```json
{
    "body": [
        {"colour": "red"},
        {"colour": "green"},
        {"colour": "blue"}
    ]
}
```

```py
from sawpit import WSTest, WSResponse

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body/0/colour", "red")
        .with_attribute("body/1/colour", "green")
        .with_attribute("body/2/colour", "blue")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Testing that a response with the following body with a list containing the colour `green` somewhere is received on connection to a websocket host:
```json
{
    "body": [
        {"colour": "red"},
        {"colour": "green"},
        {"colour": "blue"}
    ]
}
```

```py
from sawpit import WSTest, WSResponse

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body//colour", "green")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

### Message sending
Sending a message on connection to a websocket host:
```py
from sawpit import WSTest, WSMessage

ws_test = (
    WSTest("wss://example.com")
    .with_message(
        WSMessage()
        .with_attribute("body", "Hello, world!")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Triggering a message to be sent with extracted data when the following response is received:
```json
{
    "body": {
        "message": "Hello, world!"
    }
}
```

```py
from sawpit import WSTest, WSResponse, WSMessage

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body/message")
        .with_trigger(
            WSMessage()
            .with_attribute("body", "${body/message}")
        )
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Triggering a message to be sent with the first colour extracted from a list when the following response is received:
```json
{
    "body": [
        {"colour": "red"},
        {"colour": "green"},
        {"colour": "blue"}
    ]
}
```

```py
from sawpit import WSTest, WSResponse, WSMessage

ws_test = (
    WSTest("wss://example.com")
    .with_response(
        WSResponse()
        .with_attribute("body/0/colour")
        .with_trigger(
            WSMessage()
            .with_attribute("body", "${body/0/colour}")
        )
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

### Using rest requests
Attaching simple rest get request and sending it:
```py
rest_request = (
    RestRequest("https://example.com", "GET")
    .with_body({"some_key": some_value})
)

ws_test = (
    WSTest("wss://example.com")
    .with_request(rest_request)
)

await ws_test.run()

for response in ws_tester.received_request_responses:
    print(response.status_code)
    print(response.json())

assert ws_test.is_complete()
```

### Error handling
Force a test to fail is execution takes more than 30 seconds (default 60 seconds)
```py
ws_test = (
    WSTest("wss://example.com")
    .with_test_timeout(30)
    .with_response(
        WSResponse()
        .with_attribute("body")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Force a test to fail if no response is received for 15 seconds (default 10 seconds) 
- Any responses that haven't been sent will be output along with the `WSTimeoutError`
- Received responses can be output too by calling `with_received_response_logging` on the `WSTest` instance
```py
ws_test = (
    WSTest("wss://example.com")
    .with_response_timeout(15)
    .with_received_response_logging()
    .with_response(
        WSResponse()
        .with_attribute("body")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

Force a test to fail is a message takes longer than 15 seconds to send (default 10 seconds)
- The message that the test runner failed to send will be output along with the `WSTimeoutError`
```py
ws_test = (
    WSTest("wss://example.com")
    .with_message_timeout(15)
    .with_message(
        WSMessage()
        .with_attribute("body", "Hello, world!")
    )
)

await ws_test.run()

assert ws_test.is_complete()
```

## Documentation
Users can get the docstring help by running:
```py
from sawpit import WSTest
help(WSTest.with_response)
```

## Links
- [Github](https://github.com/jamsidedown/sawpit)
- PyPI // TODO
- Test PyPI // TODO