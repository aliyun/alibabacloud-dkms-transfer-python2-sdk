# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.vendored.requests import codes
from sdk.models import SignRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    get_missing_parameter_client_exception, KmsTransferHandler
from alibabacloud_dkms_transfer.utils import consts


class AsymmetricSignTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        if not request.get_Digest():
            raise get_missing_parameter_client_exception("Digest")
        sign_dkms_request = SignRequest()
        sign_dkms_request.key_id = request.get_KeyId()
        sign_dkms_request.message = base64.b64decode(request.get_Digest())
        sign_dkms_request.algorithm = request.get_Algorithm()
        sign_dkms_request.message_type = consts.DIGEST_MESSAGE_TYPE
        return sign_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        return self.client.sign_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):
        body = {"KeyId": response.key_id, "Value": base64.b64encode(response.signature).decode("utf-8"),
                "RequestId": response.request_id, "KeyVersionId": None}
        return codes.OK, None, dict_to_body(body), None
