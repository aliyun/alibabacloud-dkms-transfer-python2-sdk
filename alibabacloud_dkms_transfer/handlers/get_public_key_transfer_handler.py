# -*- coding: utf-8 -*-
from aliyunsdkcore.vendored.requests import codes
from sdk.models import GetPublicKeyRequest
from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    KmsTransferHandler


class GetPublicKeyTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        get_public_key_dkms_request = GetPublicKeyRequest()
        get_public_key_dkms_request.key_id = request.get_KeyId()
        return get_public_key_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        return self.client.get_public_key_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):
        body = {"KeyId": response.key_id, "PublicKey": response.public_key,
                "RequestId": response.request_id, "KeyVersionId": None}
        return codes.OK, None, dict_to_body(body), None
