# Logchain

[![Pipeline status](https://gitlab.com/ggpack/logchain-py/badges/master/pipeline.svg)](https://gitlab.com/ggpack/logchain-py/pipelines)
[![Coverage report](https://gitlab.com/ggpack/logchain-py/badges/master/coverage.svg?job=unittest)](https://gitlab.com/ggpack/logchain-py/-/jobs)

[![Dependencies](https://img.shields.io/badge/dependencies-0-blue.svg)]()
[![License](https://img.shields.io/badge/license-ISC-blue.svg)](https://gitlab.com/ggpack/logchain-py/-/blob/master/LICENSE)
[![Package](https://img.shields.io/badge/PIP-logchain-blue.svg)](https://pypi.org/project/logchain)

Python logging secured by blockchain 📜⛓️

## Logs get chained
The current log line contains the signature of the previous line with your secret.
* detect lines deleted / lost
* detect logs tampering

## Philosophy
The package is intended to be a **lightweight** util for generating **incorruptible** logs.

For this pupose we rely as much as possible on standard packages: few dependencies, high quality.

The formatters are easily **extensible** by simply deriving from `Basic`.


# Usage

## Install
``` bash
pip install logchain
```

## Choose your log type

Many types of logs are supported out-of-the-box:
- `Basic` raw text, relying on the standard formatter
- `Json` structured log lines with static & dynamic fields

You can write a custom formatter in 20-ish lines.

## Init once in main
``` python
from logchain import LogChainer

# Initialize a default chainer.
chainer = LogChainer()

# Register the formatter to the logger.
chainer.initLogging()
```

Have a look at [the comprehensive guide of constructor parameters](#constructor-parameters).

## Use everywhere with python logging module
``` python
import logging

logging.debug("My message")
logging.info("Some information")
```

## Check your logs integrity afterwards
``` python
from logchain import LogChainer

aLogChain = [
	"2020-04-25 00:21:36.266 TestChaining.py:33 test_logging_happy_case hello gg |862101dead44e3fb",
	"2020-04-25 00:21:36.266 TestChaining.py:34 test_logging_happy_case voila1 |87f4b398040df0b0",
	"2020-04-25 00:21:36.266 TestChaining.py:35 test_logging_happy_case voila2 |98e33f86376f5858",
	"2020-04-25 00:21:36.267 TestChaining.py:36 test_logging_happy_case voila3 |0757cf00b412a767",
	"2020-04-25 00:21:36.267 TestChaining.py:37 test_logging_happy_case voila4 |95ea9b92cc3e1bc7"
]

chainer = LogChainer(secret = "Et2FwQefvb7HfCb7tATguSicVj_7TVlM")
result = chainer.verify(aLogChain)

if not result:
	print("Last good line", result.prevLine)
	print("First bad line", result.line)
else:
	print("All right")
```

## Constructor parameters

They are passed as named arguments.
``` python
from logchain import LogChainer

chainer = LogChainer(verbosity = 3, secret = "mySignatureKey")

params = {"verbosity": 3, "secret": "mySignatureKey", "timestamp": {"fmt": "%s"}}
chainer = LogChainer(**params)
```

| **Param** *Type* | Default value | Description |
| ----- | ------------- | ----------- |
| **name** *string* | None | Name of the logger instanciated, defaults to the root logger |
| **formatterCls** *class* | formatters.Basic | Type of logging to perform, raw text, json, custom |
| **format** *string* | see below | Placeholder string used by raw-text loggers |
| **secret** *string* | secrets.token_urlsafe(128) | Signature key to compute the line signature |
| **seed** *string* | secrets.token_urlsafe() | Random string to sign into the first log line |
| **timestamp** *dict* | see below | Group of properties for the timestamp |
| **stream** *stream* | stderr | Where the logs are sent, file/console/custom stream |
| **verbosity** *int* | 0 | Number [0..5] mapped to a logging.level |

The default format is `%(timestamp)s %(levelLetters)s %(fileLine)-15s %(funcName)-15s %(message)-60s |%(signature)s`. It relies on some extra fields like the signature at its end.


## Settings of `timestamp`
| **Param** *Type* | Default value | Description |
| ----- | ------------- | ----------- |
| **fmt** *string* | "iso" | iso for 8601 or `strftime` compatible placeholders (ex: "%F %T.%f" |
| **precision** *string* | "milliseconds" | `timespec` element used by [the datetime library](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat) |
| **utc** *bool* | False | Transform the timestamp to its value in UTC |


## Logchain extra logging fields
We enrich the standard logging record with some handy string fields:

| Name | Description |
| ---- | ----------- |
| **fileLine** | Widespread `filename:lineno` |
| **levelLetters** | 4 first letters of logging level names: short and unambiguous |
| **signature** | The digital signature of the previous line. Include it in all your lines to benefit from the chaining |
| **timestamp** | Improved version of `asctime`, see below |


The `timestamp` field offers more flexibility than `asctime` in regards to:
- the precision; can go up to the micro seconds (`msecs` cannot)
- the decimal separator; you choose, '.' by default
- utc or local timezone
- customize the format only in one place: `timestamp.fmt`


## Dynamic logging fields
The package is suitable for server/app logging which context changes from one transaction to another.
Here is an example of setting contextual information throughout the lifecycle of an app:

**App.py**
``` python
class App:
	def __init__(self, appName, logger):
		self.logger = logger
		self.logger.setFields(appName = appName)
		logging.info("Creating the app")

	def handleTransaction(self, userId, callback):
		with self.logger.managedFields(uId = userId, trxId = secrets.token_urlsafe(8)):
			callback()

	def close(self):
		logging.info("Closing the app")
```

**Callbacks.py**
``` python
# The log chain in transparent for the callbacks
def callback1():
	logging.warning("Something happened")

def callback2():
	logging.info("Serving a resource")
```

**main.py**
``` python
def main():
	chainer = logchain.LogChainer(formatterCls = logchain.formatters.Json)
	chainer.initLogging()

	app = App("MyApp", chainer)
	app.handleTransaction("user1", callback1)
	app.handleTransaction("user1", callback2)
	app.close()
```

You can either use:
* `setFields`: set some permanant fields, remove one by setting it to `None`.
* `managedFields`: set some temporary fields for the scope of the `context manager`.

## Using named loggers
``` python
from logchain import LogChainer

chainer = LogChainer()
logger = chainer.initLogging(name = __name__)
logger.info("I am special!")
```

## Verbosity to logging.levels
The default mapping is described by the variable `VerbosityToLevel` as follows:

| Verbosity |  Level  |
| :---------: | ------- |
| **0** | ERROR |
| **1** | WARNING |
| **2** | INFO |
| ***other*** | DEBUG |

----

# Contributing

## Install
[**The code is hosted on Gitlab 🦊**](https://gitlab.com/ggpack/logchain-py)

Simply clone and submit pull requests.

## Testing
The unit tests are located in the [test folder](https://gitlab.com/ggpack/logchain-py/-/blob/master/test) and discovered by the module `unittest`.

``` bash
# Run all
python -m unittest discover -s test

# Get additional options
python -m unittest --help
```

## Releasing
The process is triggered by a tag added to a commit. The tag must match the pattern `release_<VERSION>`
and `VERSION` has to comply to **[semver](https://semver.org)**.

[A CI/CD job](https://gitlab.com/ggpack/logchain-py/-/blob/master/.gitlab-ci.yml) handles the new tag event and publishes the package to PYPI using the awesome [Poetry tool](https://python-poetry.org).


# Thanks
Icons made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com)
