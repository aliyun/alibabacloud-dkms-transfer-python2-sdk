# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.vendored.requests import codes
from sdk.models import DecryptRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    get_missing_parameter_client_exception, KmsTransferHandler
from alibabacloud_dkms_transfer.utils import consts


class DecryptTransferHandler(KmsTransferHandler):

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
        if not request.get_CiphertextBlob():
            raise get_missing_parameter_client_exception("CiphertextBlob")
        ciphertext_blob_bytes = base64.b64decode(request.get_CiphertextBlob())
        ekt_id_bytes = ciphertext_blob_bytes[0:consts.EKT_ID_LENGTH]
        iv_bytes = ciphertext_blob_bytes[consts.EKT_ID_LENGTH:consts.EKT_ID_LENGTH + consts.GCM_IV_LENGTH]
        ciphertext_bytes = ciphertext_blob_bytes[consts.EKT_ID_LENGTH + consts.GCM_IV_LENGTH:]
        ekt_id = ekt_id_bytes.decode("utf-8")
        decrypt_dkms_request = DecryptRequest()
        decrypt_dkms_request.request_headers = {consts.MIGRATION_KEY_VERSION_ID_KEY: ekt_id}
        decrypt_dkms_request.iv = iv_bytes
        decrypt_dkms_request.ciphertext_blob = ciphertext_bytes
        if request.get_EncryptionContext():
            decrypt_dkms_request.aad = request.get_EncryptionContext().encode("utf-8")
        return decrypt_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        runtime_options.response_headers = self.response_headers
        return self.client.decrypt_with_options(dkms_request, runtime_options)

    def transfer_response(self, response):
        response_headers = response.response_headers
        key_version_id = response_headers.get(consts.MIGRATION_KEY_VERSION_ID_KEY)
        body = {"KeyId": response.key_id, "Plaintext": response.plaintext.decode("utf-8"),
                "RequestId": response.request_id, "KeyVersionId": key_version_id}
        return codes.OK, None, dict_to_body(body, self.accept_format, self.xml_root), None
