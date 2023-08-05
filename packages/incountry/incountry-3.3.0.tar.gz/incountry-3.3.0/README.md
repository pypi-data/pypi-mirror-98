InCountry Storage SDK
============
[![Build Status](https://travis-ci.com/incountry/sdk-python.svg?branch=master)](https://travis-ci.com/incountry/sdk-python)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=incountry_sdk-python&metric=alert_status)](https://sonarcloud.io/dashboard?id=incountry_sdk-python)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=incountry_sdk-python&metric=coverage)](https://sonarcloud.io/dashboard?id=incountry_sdk-python)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=incountry_sdk-python&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=incountry_sdk-python)

## Installation
To install Python SDK, use `pipenv` (or `pip`), as follows:
```
$ pipenv install incountry
```

## Countries List
To get the full list of supported countries and their codes, please [follow this link](countries.md).


## Quickstart guide
To access your data in InCountry Platform by using Python SDK, you need to create an instance of the Storage class. You can retrieve the `client_id`, `client_secret` and `environment_id` variables from your dashboard on InCountry Portal.

```python
from incountry import Storage, SecretKeyAccessor

storage = Storage(
    client_id="<client_id>",
    client_secret="<client_secret>",
    environment_id="<environment_id>",
    secret_key_accessor=SecretKeyAccessor(lambda: "<encryption_secret>"),
)
```

## Storage Configuration
Below you can find a full list of possible configuration options for creating a Storage instance.

```python
class Storage:
    def __init__(
        self,
        # Required.
        # Can be set via INC_ENVIRONMENT_ID env variable.
        environment_id: Optional[str] = None,

        # Required when using API key authorization.
        # Can be set via INC_API_KEY env variable.
        api_key: Optional[str] = None,

        # Required when using oAuth authorization.
        # Can be set via INC_CLIENT_ID env variable.
        client_id: Optional[str] = None,

        # Required when using oAuth authorization.
        # Can be set via INC_CLIENT_SECRET env variable.
        client_secret: Optional[str] = None,

        # Instance of the SecretKeyAccessor class.
        # Used to fetch the encryption secret.
        secret_key_accessor: Optional[SecretKeyAccessor] = None,

        # Optional. Defines API URL.
        # Can be set via INC_ENDPOINT env variable.
        endpoint: Optional[str] = None,

        # Optional. If False, encryption is not applied.
        encrypt: Optional[bool] = True,

        # Optional. If True enables the additional debug logging.
        debug: Optional[bool] = False,

         # Optional. Used to fine-tune some configurations.
        options: Optional[Dict[str, Any]] = {},

        # Optional. List of custom encryption configurations.
        custom_encryption_configs: Optional[List[dict]] = None,
    ):
        ...
```

---
**WARNING**

API Key authorization is being deprecated. The backward compatibility is preserved for the `api_key` parameter but you no longer can access API keys (neither old nor new) from your dashboard.

Below you can find API Key authorization usage example:

```python
from incountry import Storage, SecretKeyAccessor

storage = Storage(
    api_key="<api_key>",
    environment_id="<environment_id>",
    secret_key_accessor=SecretKeyAccessor(lambda: "<encryption_secret>"),
)
```

---


#### Extra Storage options
You can use the `options` parameter to tweak some SDK configurations:

```python
storage = Storage(
    ...,
    options={
        "http_options": {
            "timeout": int,         # In seconds. Should be greater than 0.
        },                          # Defines http requests timeout

        "auth_endpoints": dict,     # A custom endpoints map that should be used for
                                    # fetching oAuth tokens

        "countries_endpoint": str,  # If your PoPAPI configuration relies on a custom
                                    # PoPAPI server (rather than the default one)
                                    # use the `countries_endpoint` option to specify
                                    # the endpoint responsible for fetching the list
                                    # of supported countries

        "endpoint_mask": str,       # Defines API base hostname part to use.
                                    # If set, all requests will be sent to
                                    # https://${country}${endpoint_mask} host
                                    # instead of the default one
                                    # (https://${country}-mt-01.api.incountry.io)
    }
)
```


#### oAuth options configuration
The SDK allows to precisely configure oAuth authorization endpoints (if needed). Use this option only if your plan configuration requires so.

Below you can find the example of how to create a storage instance with custom oAuth endpoints:

```python
storage = Storage(
    client_id="<client_id>",
    client_secret="<client_secret>",
    environment_id="<environment_id>",
    secret_key_accessor=SecretKeyAccessor(lambda: "<encryption_secret>"),
    options={
        "auth_endpoints": {
            "default": "<default_auth_endpoint>",
            "emea": "<auth_endpoint_for_emea_region>",
            "apac": "<auth_endpoint_for_apac_region>",
            "amer": "<auth_endpoint_for_amer_region>",
        },
    },
)
```


#### Encryption key/secret

The `secret_key_accessor` variable is used to pass a key or secret used for data encryption.

The `SecretKeyAccessor` class constructor allows you to pass a function that should return either a string representing your secret or a dictionary (we call it `secrets_data` object):

```python
{
  "secrets": [{
       "secret": str,
       "version": int, # Should be an integer greater than or equal to 0
       "isKey": bool,  # Should be True only for user-defined encryption keys
    }
  }, ....],
  "currentVersion": int,
}
```

Note: even though SDK uses PBKDF2 to generate a cryptographically strong encryption key, you must ensure that you provide a secret/password which follows the modern security best practices and standards.

The `secrets_data` variable allows you to specify multiple keys/secrets which SDK will use for data decryption based on the version of the key or secret used for encryption. Meanwhile SDK will encrypt data only by using a key (or secret) which matches the `currentVersion` parameter provided in the `secrets_data` object.

This enables the flexibility required to support Key Rotation policies when secrets (or keys) must be changed with time. The SDK will encrypt data by using the current secret (or key) while maintaining the ability to decrypt data records that were encrypted with old secrets (or keys). The SDK also provides a method for data migration which allows you to re-encrypt data with the newest secret (or key). For details please see the `migrate` method.

The SDK allows you to use custom encryption keys, instead of secrets. Please note that a user-defined encryption key should be a base64-encoded 32-bytes-long key as required by AES-256 cryptographic algorithm.


Below you can find several examples of how you can use `SecretKeyAccessor` module.
```python
# Get a secret from a variable
from incountry import SecretKeyAccessor

password = "password"
secret_key_accessor = SecretKeyAccessor(lambda: password)

# Get secrets via an HTTP request
from incountry import SecretKeyAccessor
import requests as req

def get_secrets_data():
    url = "<your_secret_url>"
    r = req.get(url)
    return r.json() # assuming response is a `secrets_data` object

secret_key_accessor = SecretKeyAccessor(get_secrets_data)
```

### Writing data to Storage

Use the `write` method in order to create/replace a record (by `record_key`).
```python
def write(self, country: str, record_key: str, **record_data: Union[str, int]) -> Dict[str, TRecord]:
    ...


# write returns created record dict on success
{
    "record": Dict
}
```


Below you can find an example of how you can use the `write` method.
```python
write_result = storage.write(
    country="us",
    record_key="user_1",
    body="some PII data",
    profile_key="customer",
    range_key1=10000,
    key1="english",
    key2="rolls-royce",
)

# write_result would be as follows
write_result = {
    "record": {
        "record_key": "user_1",
        "body": "some PII data",
        "profile_key": "customer",
        "range_key1": 10000,
        "key1": "english",
        "key2": "rolls-royce",
    }
}
```

For the list of possible `record_data` kwargs, see the section below.


#### List of available record fields
v3.0.0 release introduced a series of new fields available for data storage. Below you can find the full list of all the fields available for storage in InCountry Platform along with their types and storage methods. Each field is either encrypted, hashed or stored as is:
```python
# String fields, hashed
record_key
key1
key2
key3
key4
key5
key6
key7
key8
key9
key10
profile_key
service_key1
service_key2

# String fields, encrypted
body
precommit_body

# Int fields, plain
range_key1
range_key2
range_key3
range_key4
range_key5
range_key6
range_key7
range_key8
range_key9
range_key10
```

#### Batches
Use the `batch_write` method to create/replace multiple records at once.

```python
def batch_write(self, country: str, records: List[TRecord]) -> Dict[str, List[TRecord]]:
    ...


# batch_write returns the following dict of created records
{
    "records": List
}
```

Below you can find an example of how to use this method.
```python
batch_result = storage.batch_write(
    country="us",
    records=[
        {"record_key": "key1", "body": "body1", ...},
        {"record_key": "key2", "body": "body2", ...},
    ],
)

# batch_result would be as follows
batch_result = {
    "records": [
        {"record_key": "key1", "body": "body1", ...},
        {"record_key": "key2", "body": "body2", ...},
    ]
}
```


### Reading stored data

You can read the stored data records by its `record_key` using the `read` method.

```python
def read(self, country: str, record_key: str) -> Dict[str, TRecord]:
    ...


# The read method returns the record dictionary if the record is found
{
    "record": Dict
}
```

#### Date fields
Use the `created_at` and `updated_at` fields to access date-related information about records. The `created_at` field stores a date when a record was initially created in the target country. The `updated_at` field stores a date of the latest write operation for the given `record_key`.

The `read` method usage is as follows:
```python
read_result = storage.read(country="us", record_key="user1")

# read_result would be as follows
read_result = {
    "record": {
        "record_key": "user_1",
        "body": "some PII data",
        "profile_key": "customer",
        "range_key1": 10000,
        "key1": "english",
        "key2": "rolls-royce",
        "created_at": datetime.datetime(...),
        "updated_at": datetime.datetime(...),
    }
}
```

### Find records

You can look up for records by keys or version using the `find` method.
```python
def find(
        self,
        country: str,
        limit: Optional[int] = FIND_LIMIT,
        offset: Optional[int] = 0,
        **filters: Union[TIntFilter, TStringFilter],
    ) -> Dict[str, Any]:
    ...
```
Note: SDK returns 100 records at most.

The returned object looks like the following:
```python
{
    "data": List,
    "errors": List, # optional
    "meta": {
        "limit": int,
        "offset": int,
        "total": int,  # total records matching filter, ignoring limit
    }
}
```
You can use the following options to look up for records by hashed string keys from the [list above](#list-of-available-record-fields):
```python
# single value
key1="value1" # records with key1 equal to "value1"

# list of values
key2=["value1", "value2"] # records with key2 equal to "value1" or "value2"

# dict with $not operator
key3={"$not": "value1"} # records with key3 not equal "value1"
key4={"$not": ["value1", "value2"]} # records with key4 equal to neither "value1" or "value2"
```

You can use special `search_keys` filter to search records by partial match (similar to `LIKE` SQL operator) among record's text fields `key1, ..., key10`.
```python
search_keys="text to find"
```
---
**NOTE**

`search_keys` cannot be used in combination with any of `key1, key2, ..., key10` keys and works only in combination with non-hashing Storage mode (with `hash_search_keys` Storage option set to `False`).

---


You can use the following options to look up for records by int keys from the [list above](#list-of-available-record-fields):
```python
# single value
range_key1=1 # records with range_key1 equal to 1

# list of values
range_key2=[1, 2] # records with range_key2 equal to 1 or 2

# dictionary with comparison operators
range_key3={"$gt": 1} # records with range_key3 greater than 1
range_key4={"$gte": 1} # records with range_key4 greater than or equal to 1
range_key5={"$lt": 1} # records with range_key5 less than 1
range_key6={"$lte": 1} # records with range_key6 less than or equal to 1

# you can combine different comparison operators
range_key7={"$gt": 1, "$lte": 10} # records with range_key7 greater than 1 and less than or equal to 10

# you cannot combine similar comparison operators - e.g. $gt and $gte, $lt and $lte
```


You can use the following option to look up for records by `version` (encryption key version):
```python
# single value
version=1 # records with version equal to 1

# list of values
version=[1, 2] # records with version equal to 1 or 2

# dictionary with $not operator
version={"$not": 1} # records with version not equal 1
version={"$not": [1, 2]} # records with version equal to neither 1 or 2
```

Below you can find an example of how you can use the `find` method:
```python
find_result = storage.find(country="us", limit=10, offset=10, key1="value1", key2=["value2", "value3"])

# find_result would be as follows
find_result = {
    "data": [
        {
            "record_key": "<record_key>",
            "body": "<body>",
            "key1": "value1",
            "key2": "value2",
            "created_at": datetime.datetime(...),
            "updated_at": datetime.datetime(...),
            ...
        }
    ],
    "meta": {
        "limit": 10,
        "offset": 10,
        "total": 100,
    }
}
```

#### Error handling

There may be a situation when the `find` method receives records that cannot be decrypted.
For example, this may happen once the encryption key has been changed while the found data was encrypted with the older version of that key.
In such cases data returned by the find() method will be as follows:

```python
{
    "data": [...],  # successfully decrypted records
    "errors": [{
        "rawData",  # raw record which caused decryption error
        "error",    # decryption error description
    }, ...],
    "meta": { ... }
}
```

### Find one record matching a filter

If you need to find only one of the records matching a specific filter, you can use the `find_one` method.
```python
def find_one(
        self, country: str, offset: Optional[int] = 0, **filters: Union[TIntFilter, TStringFilter],
    ) -> Union[None, Dict[str, Dict]]:
    ...


# If a record is not found, the find_one method returns `None`. Otherwise it returns a record dictionary.
{
    "record": Dict
}
```

Below you can find the example of how to use the `find_one` method:
```python
find_one_result = storage.find_one(country="us", key1="english", key2=["rolls-royce", "bmw"])

# find_one_result would be as follows
find_one_result = {
    "record": {
        "record_key": "user_1",
        "body": "some PII data",
        "profile_key": "customer",
        "range_key1": 10000,
        "key1": "english",
        "key2": "rolls-royce",
    }
}
```


### Delete records
Use the `delete` method in order to delete a record from InCountry Platform. It is only possible by using the `record_key` field.
```python
def delete(self, country: str, record_key: str) -> Dict[str, bool]:
    ...


# the delete method returns the following dictionary upon success
{
    "success": True
}
```

Below you can find the example of how to use the delete method:
```python
delete_result = storage.delete(country="us", record_key="<record_key>")

# delete_result would be as follows
delete_result = {
    "success": True
}
```

## Attaching files to a record

**NOTE**

Attachments are currently available for InCountry dedicated instances only. Please check your subscription plan for details. This may require specifying your dedicated instance endpoint when configuring Python SDK Storage.

---


InCountry Storage allows you to attach files to the previously created records. Attachments' meta information is available through the `attachments` field of `record` dictionary, returned by `read`, `find` and `find_one` methods.


```python
read_result = storage.read(country="us", record_key="<record_key>")

# read_result with attachments would be as follows
read_result = {
    "record": {
        "record_key": "user_1",
        ...,
        "attachments": [
            {
                "created_at": datetime,
                "updated_at": datetime,
                "download_link": "<download_url>",
                "file_id": "<file_id>",
                "filename": "<file_name>.<ext>",
                "hash": "<hash>",
                "mime_type": "<mime_type>",
                "size": 1,
            },
        ],
    },
}
```


### Adding attachments

---
Note:
---

The `add_attachment` method allows you to add or replace attachments.
File data can be provided either as `BinaryIO` object or `string` with a path to the file in the file system.

```python
def add_attachment(
    self, country: str, record_key: str, file: Union[BinaryIO, str], mime_type: str = None, upsert: bool = False
) -> Dict[str, Union[str, int, datetime]]:
    ...

# The add_attachment returns attachment_meta dictionary
{
    "attachment_meta": {
        "created_at": datetime,
        "updated_at": datetime,
        "download_link": "<download_url>",
        "file_id": "<file_id>",
        "filename": "<file_name>.<ext>",
        "hash": "<hash>",
        "mime_type": "<mime_type>",
        "size": 1,
    }
}
```

Example of usage:
```python
# using file path
storage.add_attachment(country="us", record_key="<record_key>", file="./README.md")

# using BinaryIO object
with open("./README.md", "rb") as attachment_file:
    storage.add_attachment(country="<country>", record_key="<record_key>", file=attachment_file)
```

### Deleting attachments
The `delete_attachment` method allows you to delete attachment using its `file_id`.

```python
def delete_attachment(self, country: str, record_key: str, file_id: str) -> Dict[str, bool]:
    ...

# the delete_attachment method returns the following dictionary upon success
{
    "success": True
}
```

Example of usage:
```python
delete_result = storage.delete_attachment(country="us", record_key="<record_key>", file_id="<file_id>")

# delete_result would be as follows
delete_result = {
    "success": True
}
```

### Downloading attachments
The `get_attachment_file` method allows you to download attachment contents.
It returns dictionary with readable file body and filename.

```python
def get_attachment_file(self, country: str, record_key: str, file_id: str) -> Dict[str, Dict]:
    ...

# the get_attachment_file method returns the following dictionary upon success
{
    "attachment_data": {
        "filename": str,
        "file": BytesIO,
    }
}
```

Example of usage:
```python
get_attachment_res = storage.get_attachment_file(country="us", record_key="<record_key>", file_id="<file_id>")
attachment_data = get_attachment_res["attachment_data"]

with open(attachment_data["filename"], "wb") as f:
    f.write(attachment_data["file"].read())
```

### Working with attachment meta info
The `get_attachment_meta` method allows you to retrieve attachment's metadata using its `file_id`.

```python
def get_attachment_meta(self, country: str, record_key: str, file_id: str) -> Dict[str, Union[str, int, datetime]]:
    ...

# The get_attachment_meta returns attachment_meta dictionary
{
    "attachment_meta": {
        "created_at": datetime,
        "updated_at": datetime,
        "download_link": "<download_url>",
        "file_id": "<file_id>",
        "filename": "<file_name>.<ext>",
        "hash": "<hash>",
        "mime_type": "<mime_type>",
        "size": 1,
    }
}
```

Example of usage:
```python
get_attachment_meta_res = storage.get_attachment_meta(country="us", record_key="<record_key>", file_id="<file_id>")
```

The `update_attachment_meta` method allows you to update attachment's metadata (MIME type and file name).

```python
def update_attachment_meta(
        self, country: str, record_key: str, file_id: str, filename: str = None, mime_type: str = None
    ) -> Dict[str, Union[str, int, datetime]]:
    ...


# The update_attachment_meta returns attachment_meta dictionary
{
    "attachment_meta": {
        "created_at": datetime,
        "updated_at": datetime,
        "download_link": "<download_url>",
        "file_id": "<file_id>",
        "filename": "<file_name>.<ext>",
        "hash": "<hash>",
        "mime_type": "<mime_type>",
        "size": 1,
    }
}
```

Example of usage:
```python
storage.update_attachment_meta(country="us", record_key="<record_key>", file_id="<file_id>", filename="new_file_name.txt", mime_type="text/plain")
```

## Data Migration and Key Rotation support
Using `secret_key_accessor` which provides the `secrets_data` object enables key rotation and data migration support.

SDK introduces the `migrate` method which allows you to re-encrypt data encrypted with older versions of the secret.
```python
def migrate(self, country: str, limit: Optional[int] = FIND_LIMIT) -> Dict[str, int]:
    ...


# The migrate method returns the following dictionary with meta information
{
    "migrated": int   # the number of records migrated
	"total_left": int # the number of records left to migrate (number of records with version
                      # different from `currentVersion` provided by `secret_key_accessor`)
}
```
You should specify the `country` parameter which you want to perform migration in. Additionally, you need to specify the `limit` parameter for a precise number of records to migrate.


Note: the maximum number of records that can be migrated per one request is 100.

For a detailed example of a migration script, please see `/examples/full_migration.py`

Error Handling
-----

InCountry Python SDK may throw the following Exceptions:

- **StorageClientException** - it is used for various input validation errors. Can be thrown by all public methods.

- **StorageServerException** - it is thrown if SDK fails to communicate with InCountry servers or if a server response validation fails.

- **StorageCryptoException** - it is thrown during encryption/decryption procedures (both default and custom). This may be an indication of malformed/corrupted data or a wrong encryption key provided to the SDK.

- **StorageException** - general exception. Inherited by all the other exceptions.

We strongly recommend you to gracefully handle all the possible exceptions:

```python
try:
    # use InCountry Storage instance here
except StorageClientException as e:
    # some input validation error
except StorageServerException as e:
    # some server error
except StorageCryptoException as e:
    # some encryption error
except StorageException as e:
    # general error
except Exception as e:
    # something else happened not related to InCountry SDK
```

Custom Encryption Support
-----
SDK supports a capability to provide custom encryption/decryption methods if you decide to use your own algorithm instead of the default one.

The `Storage` constructor allows you to pass `custom_encryption_configs` parameters as an array of custom encryption configurations within the following schema which enables custom encryption:

```python
{
    "encrypt": Callable,
    "decrypt": Callable,
    "isCurrent": bool,
    "version": str
}
```

Both `encrypt` and `decrypt` attributes should be functions implementing the following interface (with exactly the same argument names)

```python
encrypt(input:str, key:bytes, key_version:int) -> str:
    ...

decrypt(input:str, key:bytes, key_version:int) -> str:
    ...
```
They should accept raw data to encrypt/decrypt, key data (represented as bytes array) and key version received from `SecretKeyAccessor`.
The resulted encrypted/decrypted data should be a string.

---
**NOTE**

You should provide a specific encryption key through `secrets_data` passed to `SecretKeyAccessor`. This secret should use the `isForCustomEncryption` flag instead of the regular `isKey` flag.

```python
secrets_data = {
  "secrets": [{
       "secret": "<secret for custom encryption>",
       "version": 1,
       "isForCustomEncryption": True,
    }
  }],
  "currentVersion": 1,
}

secret_accessor = SecretKeyAccessor(lambda: secrets_data)
```
---

The `version` attribute is used to differentiate custom encryptions from each other and from the default encryption as well.
This way SDK will be able to successfully decrypt any old data if encryption changes with time.

The `isCurrent` attribute allows you to specify one of the custom encryption configurations which should be used for encryption. Only one encryption configuration can be set as `"isCurrent": True`.

If none of the encryption configurations have `"isCurrent": True` then the SDK will use default encryption configuration to encrypt stored data. At the same time it will preserve the ability to decrypt old data which was encrypted with custom encryption configuration (if any).

Below you can find the example of how you can set up the SDK to use custom encryption (using Fernet encryption method from https://cryptography.io/en/latest/fernet/)

```python
import os

from incountry import InCrypto, SecretKeyAccessor, Storage
from cryptography.fernet import Fernet

def enc(input: str, key: bytes, key_version: int):
    # Fernet cipher from cryptography package accepts keys as base64-encoded string
    # while InCountry SDK decodes keys as bytes
    # thus we need to do some bytes-to-b64 encoding
    cipher = Fernet(InCrypto.b_to_base64(key))
    return cipher.encrypt(input.encode("utf8")).decode("utf8")

def dec(input: str, key: bytes, key_version: int):
    cipher = Fernet(InCrypto.b_to_base64(key))
    return cipher.decrypt(input.encode("utf8")).decode("utf8")

custom_encryption_configs = [
    {
        "encrypt": enc,
        "decrypt": dec,
        "version": "test",
        "isCurrent": True,
    }
]

key = os.urandom(InCrypto.KEY_LENGTH)  # Fernet uses 32-byte length keys

secret_key_accessor = SecretKeyAccessor(
    lambda: {
        "currentVersion": 1,
        "secrets": [{"secret": key, "version": 1, "isForCustomEncryption": True}],
    }
)

storage = Storage(
    api_key="<api_key>",
    environment_id="<env_id>",
    secret_key_accessor=secret_key_accessor,
    custom_encryption_configs=custom_encryption_configs,
)

storage.write(country="us", record_key="<record_key>", body="<body>")
```

Testing Locally
-----

1. In terminal run `pipenv run tests` for unit tests
2. In terminal run `pipenv run integrations` to run integration tests
