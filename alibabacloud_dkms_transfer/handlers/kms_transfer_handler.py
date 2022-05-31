# -*- coding: utf-8 -*-
import abc
import json

from Tea.exceptions import TeaException, UnretryableException
from alibabacloud_dkms_transfer.utils.consts import *
from alibabacloud_dkms_transfer.utils.kms_error_code_transfer_utils import *


def get_missing_parameter_client_exception(param_name):
    return ClientException(MISSING_PARAMETER_ERROR_CODE,
                           ("The parameter  %s  needed but no provided." % param_name))


def transfer_tea_exception(e):
    data = e.data
    request_id = ""
    status_code = None
    if data:
        request_id = data.get(REQUEST_ID_KEY_NAME, "")
        status_code = data.get(HTTP_CODE_KEY_NAME)
    if e.code == INVALID_PARAM_ERROR_CODE:
        if e.message == INVALID_PARAM_DATE_ERROR_MESSAGE:
            server_exception = transfer_invalid_date_exception()
            server_exception.request_id = request_id
            server_exception.http_status = status_code
            return status_code, server_exception
        elif e.message == INVALID_PARAM_AUTHORIZATION_ERROR_MESSAGE:
            server_exception = transfer_incomplete_signature_exception()
            server_exception.request_id = request_id
            server_exception.http_status = status_code
            return status_code, server_exception
    elif e.code == UNAUTHORIZED_ERROR_CODE:
        server_exception = transfer_invalid_access_key_id_exception()
        server_exception.request_id = request_id
        server_exception.http_status = status_code
        return status_code, server_exception
    else:
        error_message = transfer_error_message(e.code)
        error_message = error_message if error_message else e.message
        return status_code, ServerException(e.code, error_message, request_id=request_id, http_status=status_code)


def dict_to_body(dic):
    return json.dumps(dic, indent=4, ensure_ascii=False).encode("utf-8")


class KmsTransferHandler(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_client(self):
        pass

    @abc.abstractmethod
    def get_action(self):
        pass

    def handler_dkms_request_with_options(self, request, runtime_options):
        dkms_request = self.build_dkms_request(request, runtime_options)
        try:
            return self.transfer_response(self.call_dkms(dkms_request, runtime_options))
        except UnretryableException as e:
            if isinstance(e.inner_exception, TeaException):
                status, exception = transfer_tea_exception(e.inner_exception)
                body = {"HttpStatus": status, "Code": exception.error_code, "Message": exception.message}
                return status, None, dict_to_body(body), exception
            raise ClientException("", e.message)
        except TeaException as e:
            status, exception = transfer_tea_exception(e)
            body = {"HttpStatus": status, "Code": exception.error_code, "Message": exception.message}
            return status, None, dict_to_body(body), exception
        except ClientException as e:
            raise e
        except Exception as e:
            raise ClientException("", str(e))

    @abc.abstractmethod
    def build_dkms_request(self, request, runtime_options):
        pass

    @abc.abstractmethod
    def transfer_response(self, response):
        pass

    @abc.abstractmethod
    def call_dkms(self, dkms_request, runtime_options):
        pass
