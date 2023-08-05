from typing import Union
from pydantic import BaseModel, conlist, conint, StrictBool, StrictStr, validator


class Secret(BaseModel):
    isKey: StrictBool = False
    isForCustomEncryption: StrictBool = False
    secret: Union[StrictStr, bytes]
    version: conint(strict=True, ge=0)

    @validator("isForCustomEncryption")
    def validate_custom_encryption(cls, value, values):
        if values.get("isKey", False) and value:
            raise ValueError("secret can either be 'isKey' or 'isForCustomEncryption', not both")
        return value

    @validator("secret", pre=True)
    def validate_secret_length(cls, value, values):
        from ..incountry_crypto import InCrypto

        if not isinstance(value, (str, bytes)):
            raise ValueError("should be bytes or base64-encoded string")

        if isinstance(value, str) and (values.get("isKey", False) or values.get("isForCustomEncryption", False)):
            try:
                value = InCrypto.base64_to_b(value)
            except Exception:
                raise ValueError("should be base64-encoded string")
        elif isinstance(value, str):
            value = value.encode("utf-8")

        if values.get("isKey", False) and len(value) != InCrypto.KEY_LENGTH:
            raise ValueError(
                f"wrong default key length. Should be {InCrypto.KEY_LENGTH}-byte-length 'base64' encoded string. "
                f"If it's a custom key, please provide 'isForCustomEncryption' param"
            )

        return value


class SecretsData(BaseModel):
    currentVersion: conint(strict=True, ge=0)
    secrets: conlist(Secret, min_items=1)

    @validator("secrets", each_item=True)
    def secrets_to_dict(cls, value):
        return value.dict()

    @validator("secrets")
    def validate_current_version_exists(cls, value, values):
        current_version_found = False
        for secret in value:
            if secret["version"] == values.get("currentVersion", False):
                current_version_found = True
        if not current_version_found:
            raise ValueError("none of the secret versions match currentVersion")
        return value


class SecretsDataForDefaultEncryption(SecretsData):
    @validator("secrets")
    def check_secrets(cls, value):
        has_custom_encryption_keys = False
        for secret in value:
            if secret.get("isForCustomEncryption", False):
                has_custom_encryption_keys = True
        if has_custom_encryption_keys:
            raise ValueError("found custom encryption keys when not using custom encryption")
        return value


class SecretsDataForCustomEncryption(SecretsData):
    @validator("secrets")
    def check_secrets(cls, value):
        has_custom_encryption_keys = False
        for secret in value:
            if secret.get("isForCustomEncryption", False):
                has_custom_encryption_keys = True
        if not has_custom_encryption_keys:
            raise ValueError("custom encryption keys not provided when using custom encryption")
        return value
