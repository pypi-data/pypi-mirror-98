'''
<p align="center"><img src="https://github.com/charlesdotfish/smtp-credentials-cdk-construct/raw/main/media/logo.png" alt="Charles Dot Fish" width="400"></p>

# SMTP Credentials CDK Construct

This construct creates an IAM user, with a policy permitting emails to be sent via SES from a specified email address, creates an access key associated with this user, and converts the access key to SMTP credentials.

The generated SMTP credentials are stored as a parameter in Parameter Store, and the name of this parameter is output as a CloudFormation output. The parameter may be safely deleted, once the credentials have been accessed.

## Example Usage

See [API.md](https://github.com/charlesdotfish/smtp-credentials-cdk-construct/blob/main/API.md) for details on the exposed API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SmtpCredentials(self, "SmtpCredentials",
    email_address="me@charles.fish"
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class SmtpCredentials(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@charlesdotfish/smtp-credentials-cdk-construct.SmtpCredentials",
):
    '''This construct creates an IAM user, with a policy permitting emails to be sent via SES from a specified email address, creates an access key associated with this user, and converts the access key to SMTP credentials.

    The generated SMTP credentials are stored as a parameter in Parameter Store, and the name of
    this parameter is output as a CloudFormation output. The parameter may be safely deleted, once
    the credentials have been accessed.

    Example::

        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        SmtpCredentials(self, "SmtpCredentials",
            email_address="me@charles.fish"
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        email_address: builtins.str,
    ) -> None:
        '''
        :param scope: A reference to the stack which this construct will be created in. Note that the SMTP credentials generated will only be permitted to send emails in this stack's region.
        :param id: A unique identifier, within the context that this construct is created.
        :param email_address: The email address that the generated SMTP credentials will permit emails to be sent from.
        '''
        props = SmtpCredentialsProps(email_address=email_address)

        jsii.create(SmtpCredentials, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@charlesdotfish/smtp-credentials-cdk-construct.SmtpCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"email_address": "emailAddress"},
)
class SmtpCredentialsProps:
    def __init__(self, *, email_address: builtins.str) -> None:
        '''This struct provides the configuration required to construct an instance of @see SmtpCredentials.

        :param email_address: The email address that the generated SMTP credentials will permit emails to be sent from.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "email_address": email_address,
        }

    @builtins.property
    def email_address(self) -> builtins.str:
        '''The email address that the generated SMTP credentials will permit emails to be sent from.'''
        result = self._values.get("email_address")
        assert result is not None, "Required property 'email_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SmtpCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SmtpCredentials",
    "SmtpCredentialsProps",
]

publication.publish()
