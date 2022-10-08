# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.vendored.requests import codes
from sdk.models import EncryptRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    get_missing_parameter_client_exception, KmsTransferHandler
from alibabacloud_dkms_transfer.utils import consts


class AsymmetricEncryptTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action
        self.response_headers = [consts.MIGRATION_KEY_VERSION_ID_KEY]
        self.accept_format = "JSON"
        self.xml_root = "KMS"

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        self.accept_format = request.get_accept_format()
        if not request.get_Plaintext():
            raise get_missing_parameter_client_exception("Plaintext")
        encrypt_dkms_request = EncryptRequest()
        encrypt_dkms_request.key_id = request.get_KeyId()
        encrypt_dkms_request.plaintext = base64.b64decode(request.get_Plaintext())
        encrypt_dkms_request.algorithm = request.get_Algorithm()
        return encrypt_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        runtime_options.response_headers = self.response_headers
        return self.client.encrypt_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):
        response_headers = response.response_headers
        key_version_id = response_headers.get(consts.MIGRATION_KEY_VERSION_ID_KEY)
        body = {"KeyId": response.key_id, "CiphertextBlob": base64.b64encode(response.ciphertext_blob).decode("utf-8"),
                "RequestId": response.request_id, "KeyVersionId": key_version_id}
        return codes.OK, None, dict_to_body(body, self.accept_format, self.xml_root), None
