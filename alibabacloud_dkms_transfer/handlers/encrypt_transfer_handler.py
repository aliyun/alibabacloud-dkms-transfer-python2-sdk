# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.vendored.requests import codes
from sdk.models import EncryptRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    get_missing_parameter_client_exception, KmsTransferHandler
from alibabacloud_dkms_transfer.utils import consts


class EncryptTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action
        self.response_headers = [consts.MIGRATION_KEY_VERSION_ID_KEY]

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        if not request.get_Plaintext():
            raise get_missing_parameter_client_exception("Plaintext")
        encrypt_dkms_request = EncryptRequest()
        encrypt_dkms_request.key_id = request.get_KeyId()
        encrypt_dkms_request.plaintext = base64.b64decode(request.get_Plaintext())
        if request.get_EncryptionContext():
            encrypt_dkms_request.aad = request.get_EncryptionContext().encode("utf-8")
        return encrypt_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        runtime_options.response_headers = self.response_headers
        return self.client.encrypt_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):

        response_headers = response.response_headers
        version_id = response_headers.get(consts.MIGRATION_KEY_VERSION_ID_KEY)
        if not response_headers or not version_id:
            raise ClientException("",
                                  "Can not found response headers parameter[%s]" % consts.MIGRATION_KEY_VERSION_ID_KEY)
        ciphertext_blob = version_id.encode("utf-8") + response.iv + response.ciphertext_blob
        body = {"KeyId": response.key_id, "CiphertextBlob": base64.b64encode(ciphertext_blob).decode("utf-8"),
                "RequestId": response.request_id, "KeyVersionId": None}
        return codes.OK, None, dict_to_body(body), None
