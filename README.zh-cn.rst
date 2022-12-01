阿里云专属KMS适配Python2 SDK
============================

|image0|

阿里云专属KMS适配Python2
SDK可以帮助Python开发者快速完成由KMS密钥向专属KMS密钥迁移适配工作。

*其他语言版本:*\ `English <README.rst>`__\ *,*\ `简体中文 <README.zh-cn.rst>`__

-  `阿里云专属KMS主页 <https://help.aliyun.com/document_detail/311016.html>`__
-  `代码示例 </examples>`__
-  `Issues <https://github.com/aliyun/alibabacloud-dkms-transfer-python2-sdk/issues>`__
-  `Release <https://github.com/aliyun/alibabacloud-dkms-transfer-python2-sdk/releases>`__

许可证
------

`Apache License
2.0 <https://www.apache.org/licenses/LICENSE-2.0.html>`__

优势
----

-  专属KMS提供租户独享的服务实例，并部署到租户的VPC内，满足私有网络接入需求。
-  专属KMS使用租户独享的密码资源池（HSM集群），实现资源隔离和密码学隔离，以获得更高的安全性。
-  专属KMS可以降低使用HSM的复杂度，为您的HSM提供稳定、易用的上层密钥管理途径和密码计算服务。
-  专属KMS可以将您的HSM与云服务无缝集成，为云服务加密提供更高的安全性和可控制性。更多信息，请参见\ `支持服务端集成加密的云服务 <https://help.aliyun.com/document_detail/141499.htm?#concept-2318937>`__\ 。
-  减低用户从共享KMS密钥移专属KMS密钥的成本

软件要求
--------

-  Python 2.7.15 or later

安装
----

::

   pip install alibabacloud-dkms-transfer-python2


客户端机制
----------

阿里云专属KMS适配Python SDK默认将下面列表方法请求转发给专属KMS VPC网关。

-  Encrypt
-  Decrypt
-  GenerateDataKey
-  GenerateDataKeyWithoutPlaintext
-  GetPublicKey
-  AsymmetricEncrypt
-  AsymmetricDecrypt
-  AsymmetricSign
-  AsymmetricVerify
-  GetSecretValue

.. _许可证-1:

许可证
------

`Apache-2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__

版权所有 2009-present, 阿里巴巴集团.

.. |image0| image:: https://aliyunsdk-pages.alicdn.com/icons/AlibabaCloud.svg
