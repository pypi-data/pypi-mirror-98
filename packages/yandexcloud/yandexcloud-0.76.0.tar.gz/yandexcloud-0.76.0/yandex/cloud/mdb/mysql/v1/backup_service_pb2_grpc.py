# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from yandex.cloud.mdb.mysql.v1 import backup_pb2 as yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__pb2
from yandex.cloud.mdb.mysql.v1 import backup_service_pb2 as yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2


class BackupServiceStub(object):
    """A set of methods for managing MySQL backups.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/yandex.cloud.mdb.mysql.v1.BackupService/Get',
                request_serializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.GetBackupRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__pb2.Backup.FromString,
                )
        self.List = channel.unary_unary(
                '/yandex.cloud.mdb.mysql.v1.BackupService/List',
                request_serializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsResponse.FromString,
                )


class BackupServiceServicer(object):
    """A set of methods for managing MySQL backups.
    """

    def Get(self, request, context):
        """Returns the specified MySQL backup.

        To get the list of available MySQL backups, make a [List] request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Retrieves the list of MySQL backups available for the specified folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BackupServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.GetBackupRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__pb2.Backup.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.mdb.mysql.v1.BackupService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BackupService(object):
    """A set of methods for managing MySQL backups.
    """

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.mdb.mysql.v1.BackupService/Get',
            yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.GetBackupRequest.SerializeToString,
            yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__pb2.Backup.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.mdb.mysql.v1.BackupService/List',
            yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsRequest.SerializeToString,
            yandex_dot_cloud_dot_mdb_dot_mysql_dot_v1_dot_backup__service__pb2.ListBackupsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
