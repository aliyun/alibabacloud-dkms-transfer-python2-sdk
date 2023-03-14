# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.vendored.requests import codes
from sdk.models import EncryptRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    get_missing_parameter_client_exception, KmsTransferHandler, encode_user_encryption_context
from alibabacloud_dkms_transfer.utils import consts


class EncryptTransferHandler(KmsTransferHandler):

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
        plaintext = request.get_Plaintext()
        if not plaintext:
            raise get_missing_parameter_client_exception("Plaintext")
        encrypt_dkms_request = EncryptRequest()
        encrypt_dkms_request.key_id = request.get_KeyId()
        if isinstance(plaintext, str):
            encrypt_dkms_request.plaintext = plaintext.encode("utf-8")
        else:
            encrypt_dkms_request.plaintext = plaintext
        if request.get_EncryptionContext():
            encrypt_dkms_request.aad = encode_user_encryption_context(request.get_EncryptionContext())
        return encrypt_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        runtime_options.response_headers = self.response_headers
        return self.client.encrypt_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):
        response_headers = response.response_headers
        key_version_id = response_headers.get(consts.MIGRATION_KEY_VERSION_ID_KEY)
        if not response_headers or not key_version_id:
            raise ClientException("",
                                  "Can not found response headers parameter[%s]" % consts.MIGRATION_KEY_VERSION_ID_KEY)
        ciphertext_blob = key_version_id.encode("utf-8") + response.iv + response.ciphertext_blob
        body = {"KeyId": response.key_id, "CiphertextBlob": base64.b64encode(ciphertext_blob).decode("utf-8"),
                "RequestId": response.request_id, "KeyVersionId": key_version_id}
        return codes.OK, None, dict_to_body(body, self.accept_format, self.xml_root), None
