# Getting Started with APIMATIC Calculator

## Getting Started

### Introduction

Simple calculator API hosted on APIMATIC

### Install the Package

The package is compatible with Python versions `2 >=2.7.9` and `3 >=3.4`.
Install the package from PyPi using the following pip command:

```python
pip install absarsnew==1.1
```

You can also view the package at:
https://pypi.python.org/pypi/absarsnew

### Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 3** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 0** |

The API client can be initialized as follows:

```python
from apimaticcalculator.apimaticcalculator_client import ApimaticcalculatorClient
from apimaticcalculator.configuration import Environment

client = ApimaticcalculatorClient(
    environment = ,)
```

## Client Class Documentation

### APIMATIC Calculator Client

The gateway for the SDK. This class acts as a factory for the Controllers and also holds the configuration of the SDK.

### Controllers

| Name | Description |
|  --- | --- |
| simple_calculator | Gets SimpleCalculatorController |

## API Reference

### List of APIs

* [Simple Calculator](#simple-calculator)

### Simple Calculator

#### Overview

##### Get instance

An instance of the `SimpleCalculatorController` class can be accessed from the API Client.

```
simple_calculator_controller = client.simple_calculator
```

#### Get Calculate

Calculates the expression using the specified operation.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_calculate(self,
                 operation,
                 x,
                 y)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `operation` | [`OperationTypeEnum`](#operation-type) | Template, Required | The operator to apply on the variables |
| `x` | `float` | Query, Required | The LHS value |
| `y` | `float` | Query, Required | The RHS value |

##### Response Type

`float`

##### Example Usage

```python
operation = OperationTypeEnum.MULTIPLY
x = 222.14
y = 165.14

result = simple_calculator_controller.get_calculate(operation, x, y)
```

## Model Reference

### Enumerations

* [Operation Type](#operation-type)

#### Operation Type

Possible operators are sum, subtract, multiply, divide

##### Class Name

`OperationTypeEnum`

##### Fields

| Name |
|  --- |
| `SUM` |
| `SUBTRACT` |
| `MULTIPLY` |
| `DIVIDE` |

## Utility Classes Documentation

### ApiHelper

A utility class for processing API Calls. Also contains classes for supporting standard datetime formats.

#### Methods

| Name | Description |
|  --- | --- |
| json_deserialize | Deserializes a JSON string to a Python dictionary. |

#### Classes

| Name | Description |
|  --- | --- |
| HttpDateTime | A wrapper for datetime to support HTTP date format. |
| UnixDateTime | A wrapper for datetime to support Unix date format. |
| RFC3339DateTime | A wrapper for datetime to support RFC3339 format. |

## Common Code Documentation

### HttpResponse

Http response received.

#### Parameters

| Name | Type | Description |
|  --- | --- | --- |
| status_code | int | The status code returned by the server. |
| reason_phrase | str | The reason phrase returned by the server. |
| headers | dict | Response headers. |
| text | str | Response body. |
| request | HttpRequest | The request that resulted in this response. |

### HttpRequest

Represents a single Http Request.

#### Parameters

| Name | Type | Tag | Description |
|  --- | --- | --- | --- |
| http_method | HttpMethodEnum |  | The HTTP method of the request. |
| query_url | str |  | The endpoint URL for the API request. |
| headers | dict | optional | Request headers. |
| query_parameters | dict | optional | Query parameters to add in the URL. |
| parameters | dict &#124; str | optional | Request body, either as a serialized string or else a list of parameters to form encode. |
| files | dict | optional | Files to be sent with the request. |

