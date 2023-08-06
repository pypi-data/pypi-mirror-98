import grpc
from pb.gen.auth_pb2_grpc import HwsAuthStub
from pb.gen.auth_pb2 import AuthRequest


class Auth(object):
    separators = ':'

    def __init__(self, host):
        """
        :param host: server host
        """
        self._channel = grpc.insecure_channel(host)
        self._stub = HwsAuthStub(self._channel)

    def auth(self,
             subject_type='user_id',
             subject_id=0,
             action='',
             recourse_type='',
             recourse_id=0,
             partner_id=0,
             domain=''):
        """
        权限验证
        :param subject_type: 访问对象类型, 普通用户为user_id
        :param subject_id: 访问对象id
        :param action: 请求action_code
        :param recourse_type: 资源对象类型, 即schema, 如门店为STORE
        :param recourse_id: 资源对象id
        :param partner_id: 租户id
        :param domain: 场景
        :return: e.g. {"status": {"code": 0, "message": "CHECK_AUTH_ERR"}}, code在./codes/codes.proto中定义, 非0即为失败
        """
        auth_request = AuthRequest()
        auth_request.subject = subject_type + self.separators + str(subject_id)
        auth_request.action = action
        auth_request.resource = recourse_type + self.separators + str(recourse_id)
        scope = auth_request.scope
        scope.partnerId = partner_id
        scope.domain = domain

        return self._stub.Auth(auth_request)

    def close(self):
        self._channel.close()
