# -*- coding: utf-8 -*-
from aliyunsdkcore.vendored.requests import codes
from sdk.models import GetSecretValueRequest

from alibabacloud_dkms_transfer.handlers.kms_transfer_handler import KmsTransferHandler, dict_to_body


class GetSecretValueTransferHandler(KmsTransferHandler):

    def __init__(self, client, action):
        self.client = client
        self.action = action
        self.accept_format = "JSON"
        self.xml_root = "KMS"

    def get_client(self):
        return self.client

    def get_action(self):
        return self.action

    def build_dkms_request(self, request, runtime_options):
        self.accept_format = request.get_accept_format()
        get_secret_value_request = GetSecretValueRequest()
        get_secret_value_request.secret_name = request.get_SecretName()
        get_secret_value_request.version_id = request.get_VersionId()
        get_secret_value_request.version_stage = request.get_VersionStage()
        get_secret_value_request.fetch_extended_config = request.get_FetchExtendedConfig()
        return get_secret_value_request

    def transfer_response(self, response):
        body = {
            'SecretName': response.secret_name,
            'SecretType': response.secret_type,
            'SecretData': response.secret_data,
            'SecretDataType': response.secret_data_type,
            'VersionStages': {'VersionStage': response.version_stages},
            'VersionId': response.version_id,
            'CreateTime': response.create_time,
            'RequestId': response.request_id,
            'LastRotationDate': response.last_rotation_date,
            'NextRotationDate': response.next_rotation_date,
            'ExtendedConfig': response.extended_config,
            'AutomaticRotation': response.automatic_rotation,
            'RotationInterval': response.rotation_interval,
        }
        return codes.OK, None, dict_to_body(body, self.accept_format, self.xml_root), None

    def call_dkms(self, dkms_request, runtime_options):
        return self.client.get_secret_value_with_options(dkms_request, runtime_options)
