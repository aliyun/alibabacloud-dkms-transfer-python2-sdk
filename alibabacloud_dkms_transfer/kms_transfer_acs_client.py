# -*- coding: utf-8 -*-
from aliyunsdkcore.client import AcsClient
from openapi_util.models import RuntimeOptions
from sdk.client import Client

from alibabacloud_dkms_transfer.handlers.asymmetic_decrypt_transfer_handler import AsymmetricDecryptTransferHandler
from alibabacloud_dkms_transfer.handlers.asymmetic_encrypt_transfer_handler import AsymmetricEncryptTransferHandler
from alibabacloud_dkms_transfer.handlers.asymmetic_sign_transfer_handler import AsymmetricSignTransferHandler
from alibabacloud_dkms_transfer.handlers.asymmetic_verify_transfer_handler import AsymmetricVerifyTransferHandler
from alibabacloud_dkms_transfer.handlers.decrypt_transfer_handler import DecryptTransferHandler
from alibabacloud_dkms_transfer.handlers.encrypt_transfer_handler import EncryptTransferHandler
from alibabacloud_dkms_transfer.handlers.generate_data_key_transfer_handler import GenerateDataKeyTransferHandler
from alibabacloud_dkms_transfer.handlers.generate_data_key_without_plaintext_transfer_handler import \
    GenerateDataKeyWithoutPlaintextTransferHandler
from alibabacloud_dkms_transfer.handlers.get_public_key_transfer_handler import GetPublicKeyTransferHandler
from alibabacloud_dkms_transfer.handlers.get_secret_value_transfer_handler import GetSecretValueTransferHandler
from alibabacloud_dkms_transfer.utils.consts import *


class KmsTransferAcsClient(AcsClient):

    def __init__(self, config,
                 ak=None,
                 secret=None,
                 region_id="cn-hangzhou",
                 auto_retry=True,
                 max_retry_time=None,
                 user_agent=None,
                 port=80,
                 connect_timeout=None,
                 timeout=None,
                 public_key_id=None,
                 private_key=None,
                 session_period=3600,
                 credential=None,
                 debug=False,
                 verify=None,
                 pool_size=10,
                 proxy=None):
        AcsClient.__init__(self, ak=ak,
                           secret=secret,
                           region_id=region_id,
                           auto_retry=auto_retry,
                           max_retry_time=max_retry_time,
                           user_agent=user_agent,
                           port=port,
                           connect_timeout=connect_timeout,
                           timeout=timeout,
                           public_key_id=public_key_id,
                           private_key=private_key,
                           session_period=session_period,
                           credential=credential,
                           debug=debug,
                           verify=verify,
                           pool_size=pool_size,
                           proxy=proxy)
        self.handlers = dict()
        self.client = Client(config)
        self.init_kms_transfer_handlers()

    def init_kms_transfer_handlers(self):
        self.handlers[ENCRYPT_API_NAME] = EncryptTransferHandler(self.client, ENCRYPT_API_NAME)
        self.handlers[DECRYPT_API_NAME] = DecryptTransferHandler(self.client, DECRYPT_API_NAME)
        self.handlers[ASYMMETRIC_ENCRYPT_API_NAME] = AsymmetricEncryptTransferHandler(self.client,
                                                                                      ASYMMETRIC_ENCRYPT_API_NAME)
        self.handlers[ASYMMETRIC_DECRYPT_API_NAME] = AsymmetricDecryptTransferHandler(self.client,
                                                                                      ASYMMETRIC_DECRYPT_API_NAME)
        self.handlers[ASYMMETRIC_SIGN_API_NAME] = AsymmetricSignTransferHandler(self.client,
                                                                                ASYMMETRIC_SIGN_API_NAME)
        self.handlers[ASYMMETRIC_VERIFY_API_NAME] = AsymmetricVerifyTransferHandler(self.client,
                                                                                    ASYMMETRIC_VERIFY_API_NAME)
        self.handlers[GENERATE_DATA_KEY_API_NAME] = GenerateDataKeyTransferHandler(self.client,
                                                                                   GENERATE_DATA_KEY_API_NAME)
        self.handlers[GENERATE_DATA_KEY_WITHOUT_PLAINTEXT_API_NAME] = GenerateDataKeyWithoutPlaintextTransferHandler(
            self.client,
            GENERATE_DATA_KEY_WITHOUT_PLAINTEXT_API_NAME)
        self.handlers[GET_PUBLIC_KEY_API_NAME] = GetPublicKeyTransferHandler(self.client, GET_PUBLIC_KEY_API_NAME)
        self.handlers[GET_SECRET_VALUE_API_NAME] = GetSecretValueTransferHandler(self.client, GET_SECRET_VALUE_API_NAME)

    def _implementation_of_do_action(self, request, signer=None):
        if self.handlers.__contains__(request.get_action_name()):
            return self.dispatch_dkms_action(request)
        return super(KmsTransferAcsClient,
                     self)._implementation_of_do_action(request, signer)

    def dispatch_dkms_action(self, request):
        runtime_options = RuntimeOptions()
        if not self.get_verify():
            runtime_options.ignore_ssl = not self.get_verify()
        else:
            runtime_options.verify = self.get_verify()
        return self.handlers.get(request.get_action_name()).handler_dkms_request_with_options(request, runtime_options)
