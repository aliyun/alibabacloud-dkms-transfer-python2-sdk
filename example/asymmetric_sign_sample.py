# -*- coding: utf-8 -*-
import os

from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.client import AcsClient
from aliyunsdkkms.request.v20160120.AsymmetricSignRequest import AsymmetricSignRequest
from openapi.models import Config

from alibabacloud_dkms_transfer.kms_transfer_acs_client import KmsTransferAcsClient


def transfer_sdk_asymmetric_sign():
    config = Config()
    config.protocol = "https"
    config.client_key_file = "<your-client-key-file-path>"
    config.password = "<your-password>"
    config.endpoint = "<your-endpoint>"
    credentials = AccessKeyCredential(os.getenv('ACCESS_KEY_ID'), os.getenv('ACCESS_KEY_SECRET'))
    # verify可以设置为: 1.False (忽略ssl验证) 2.ca证书路径
    client = KmsTransferAcsClient(config, credential=credentials, verify='<your-ca-certificate-file-path>')
    request = AsymmetricSignRequest()
    request.set_KeyId("<your-key-id>")
    request.set_Digest("<your-digest>")
    request.set_Algorithm("<your-algorithm>")
    response = client.do_action_with_exception(request)
    print(str(response))


def kms_sdk_asymmetric_sign():
    credentials = AccessKeyCredential(os.getenv('ACCESS_KEY_ID'), os.getenv('ACCESS_KEY_SECRET'))
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    client = AcsClient(region_id="<your-region-id>", credential=credentials)
    request = AsymmetricSignRequest()
    request.set_accept_format('json')
    request.set_KeyId("<your-key-id>")
    request.set_KeyVersionId("<your-key-version-id>")
    request.set_Digest("<your-digest>")
    request.set_Algorithm("<your-algorithm>")
    response = client.do_action_with_exception(request)
    print(str(response))


transfer_sdk_asymmetric_sign()
kms_sdk_asymmetric_sign()
