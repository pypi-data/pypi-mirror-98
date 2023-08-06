# Cloudera CDP Command Line Interface

This package provides a unified command line interface to the Cloudera Data
Platform (CDP) control plane API.

## Prerequisites

* Python 3.6 or higher

Earlier versions of Python are no longer supported for new releases, as of
January 2021. Previous CLI releases shall continue to work under earlier Python
versions.

Starting with version 0.9.24, the requests and urllib3 libraries are no longer
bundled with the CLI. When upgrading, watch for those new dependencies to be
installed.

## Installation

To install using `pip` from the
[cdpcli PyPI project](https://pypi.org/project/cdpcli/):

```
$ pip install cdpcli
```

To install from source:

```
$ git clone git@github.com:cloudera/cdpcli.git
$ cd cdpcli
$ pip install .
```

### Beta CLI

An alternative CLI exposing beta functionality is available in its own package.

```
$ pip install cdpcli-beta
```

Do not install both the regular and beta CLIs in the same Python environment,
as they use the same entry points and therefore conflict.

Any features exposed in the beta CLI that are not available in the regular CLI
are still under development. They are not yet supported, may not work, and are
subject to change in incompatible ways, including removal. Do not rely on beta
features for production use.

## Configuring

API calls through the CDP CLI require a key pair issued from the CDP control
plane. Use the CDP console to generate keys, following [documented
instructions](https://docs.cloudera.com/cdp/latest/cli/topics/mc-cli-generating-an-api-access-key.html).
Then, run `cdp configure` to provide the credentials to the CLI.

```
$ cdp configure
CDP Access Key ID [None]: xxx
CDP Private Key [None]: yyy
```

Credentials are stored under the "default" profile in *$HOME/.cdp/credentials*,
using the ini file format.

### Profiles

If you need to access the API as more than one user, set up a named profile for
each user. Each profile stores a separate set of credentials.

```
$ cdp configure --profile my-other-user
```

### Credential Environment Variables

An alternative to storing credentials in *$HOME/.cdp/credentials* is to pass
them using the environment variables `CDP_ACCESS_KEY_ID` and `CDP_PRIVATE_KEY`.
However, these variables are ignored when the `--profile` option is used when
running the CLI (see below).

## Running

Basic syntax:

```
cdp [options] <command> <subcommand> [parameters]
```

Examples:

```
$ cdp iam get-user
$ cdp environments describe-environments --environment-name myenv1
```

### Help

For general help, use any of these commands.

```
$ cdp help
$ cdp --help
$ cdp # no arguments
```

Most CLI commands correspond to API services. Subcommands correspond to
operations in services.

* For help on any command, run its `help` subcommand, or pass the `--help` parameter.
* For help on any subcommand, pass the `help` or `--help` parameter.

The same help content is available in online
[API documentation](https://cloudera.github.io/cdp-dev-docs/api-docs/).

### Profiles

By default, the CLI uses credentials in the "default" profile. Use a different
profile by passing the `--profile` option.

```
$ cdp --profile my-other-user iam get-user
```

## License

The CDP CLI is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
with a [supplemental license disclaimer](https://console.cdp.cloudera.com/downloads/LICENSE_SUPPLEMENTAL_DISCLAIMER.txt).
