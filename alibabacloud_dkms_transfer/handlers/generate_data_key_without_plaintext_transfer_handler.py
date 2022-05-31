# -*- coding: utf-8 -*-
import base64

from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.vendored.requests import codes
from sdk.models import GenerateDataKeyRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import dict_to_body, \
    KmsTransferHandler, INVALID_PARAM_ERROR_CODE, \
    INVALID_PARAMETER_KEY_SPEC_ERROR_MESSAGE
from alibabacloud_dkms_transfer.utils import consts


class GenerateDataKeyWithoutPlaintextTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action
        self.response_headers = [consts.MIGRATION_KEY_VERSION_ID_KEY]

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        generate_data_key_without_plaintext_dkms_request = GenerateDataKeyRequest()
        generate_data_key_without_plaintext_dkms_request.key_id = request.get_KeyId()
        key_spec = request.get_KeySpec()
        number_of_bytes = request.get_NumberOfBytes()
        if not number_of_bytes:
            if not key_spec or consts.KMS_KEY_PAIR_AES_256 == key_spec:
                number_of_bytes = consts.NUMBER_OF_BYTES_AES_256
            elif consts.KMS_KEY_PAIR_AES_128 == key_spec:
                number_of_bytes = consts.NUMBER_OF_BYTES_AES_128
            else:
                raise ClientException(INVALID_PARAM_ERROR_CODE, INVALID_PARAMETER_KEY_SPEC_ERROR_MESSAGE)
        generate_data_key_without_plaintext_dkms_request.number_of_bytes = number_of_bytes
        if request.get_EncryptionContext():
            generate_data_key_without_plaintext_dkms_request.aad = request.get_EncryptionContext().encode("utf-8")
        return generate_data_key_without_plaintext_dkms_request

    def call_dkms(self, dkms_request, runtime_options):
        runtime_options.response_headers = self.response_headers
        return self.client.generate_data_key_with_options(dkms_request, runtime_options)

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
