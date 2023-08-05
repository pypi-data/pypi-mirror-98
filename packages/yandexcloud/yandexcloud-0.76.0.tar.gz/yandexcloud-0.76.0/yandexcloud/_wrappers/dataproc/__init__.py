# -*- coding: utf-8 -*-

import logging
import random
from six import string_types

from google.protobuf.field_mask_pb2 import FieldMask

import yandex.cloud.dataproc.v1.cluster_pb2 as cluster_pb
import yandex.cloud.dataproc.v1.cluster_service_pb2 as cluster_service_pb
import yandex.cloud.dataproc.v1.cluster_service_pb2_grpc as cluster_service_grpc_pb
import yandex.cloud.dataproc.v1.common_pb2 as common_pb
import yandex.cloud.dataproc.v1.job_pb2 as job_pb
import yandex.cloud.dataproc.v1.job_service_pb2 as job_service_pb
import yandex.cloud.dataproc.v1.job_service_pb2_grpc as job_service_grpc_pb
import yandex.cloud.dataproc.v1.subcluster_pb2 as subcluster_pb
import yandex.cloud.dataproc.v1.subcluster_service_pb2 as subcluster_service_pb
import yandex.cloud.dataproc.v1.subcluster_service_pb2_grpc as subcluster_service_grpc_pb


class Dataproc(object):
    """
    A base hook for Yandex.Cloud Data Proc.

    :param default_folder_id: ID of the Yandex.Cloud folder that will be used by default for nodes and clusters creation
    :type default_folder_id: Optional[str]
    :param default_public_ssh_key: SSH public key that will be placed to created Compute nodes, providing a root shell
    :type default_public_ssh_key: Optional[str]
    :param logger: Logger object
    :type logger: Optional[logging.Logger]
    :param sdk: SDK object. Normally is being set by Wrappers constructor
    :type sdk: yandexcloud.SDK
    """

    def __init__(self, default_folder_id=None, default_public_ssh_key=None, logger=None, sdk=None):
        self.sdk = sdk or self.sdk
        self.log = logger
        if not self.log:
            self.log = logging.getLogger()
            self.log.addHandler(logging.NullHandler())
        self.cluster_id = None
        self.default_folder_id = default_folder_id
        self.default_public_ssh_key = default_public_ssh_key

    def create_cluster(
            self,
            s3_bucket,
            folder_id=None,
            cluster_name=None,
            cluster_description='',
            cluster_image_version='1.1',
            ssh_public_keys=None,
            subnet_id=None,
            services=('HDFS', 'YARN', 'MAPREDUCE', 'HIVE', 'SPARK'),
            zone='ru-central1-b',
            service_account_id=None,
            masternode_resource_preset='s2.small',
            masternode_disk_size=15,
            masternode_disk_type='network-ssd',
            datanode_resource_preset='s2.small',
            datanode_disk_size=15,
            datanode_disk_type='network-ssd',
            datanode_count=2,
            computenode_resource_preset='s2.small',
            computenode_disk_size=15,
            computenode_disk_type='network-ssd',
            computenode_count=0,
    ):
        """
        Create Yandex.Cloud Data Proc cluster.

        :param s3_bucket: Yandex.Cloud S3 bucket to store cluster logs.
                          Jobs will not work if the bicket is not specified.
        :type s3_bucket: str
        :param folder_id: ID of the folder in which cluster should be created.
        :type folder_id: str
        :param cluster_name: Cluster name. Must be unique inside the folder.
        :type folder_id: str
        :param cluster_description: Cluster description.
        :type cluster_description: str
        :param cluster_image_version: Cluster image version. Use default.
        :type cluster_image_version: str
        :param ssh_public_keys: List of SSH public keys that will be deployed to created compute instances.
        :type ssh_public_keys: List[str]
        :param subnet_id: ID of the subnetwork. All Data Proc cluster nodes will use one subnetwork.
        :type subnet_id: str
        :param services: List of services that will be installed to the cluster. Possible options:
            HDFS, YARN, MAPREDUCE, HIVE, TEZ, ZOOKEEPER, HBASE, SQOOP, FLUME, SPARK, SPARK, ZEPPELIN, OOZIE
        :type services: List[str]
        :param zone: Availability zone to create cluster in.
                     Currently there are ru-central1-a, ru-central1-b and ru-central1-c.
        :type zone: str
        :param service_account_id: Service account id for the cluster.
                                   Service account can be created inside the folder.
        :type service_account_id: str
        :param masternode_resource_preset: Resources preset (CPU+RAM configuration)
                                           for the master node of the cluster.
        :type masternode_resource_preset: str
        :param masternode_disk_size: Masternode storage size in GiB.
        :type masternode_disk_size: int
        :param masternode_disk_type: Masternode storage type. Possible options: network-ssd, network-hdd.
        :type masternode_disk_type: str
        :param datanode_resource_preset: Resources preset (CPU+RAM configuration)
                                         for the data nodes of the cluster.
        :type datanode_resource_preset: str
        :param datanode_disk_size: Datanodes storage size in GiB.
        :type datanode_disk_size: int
        :param datanode_disk_type: Datanodes storage type. Possible options: network-ssd, network-hdd.
        :type datanode_disk_type: str
        :param computenode_resource_preset: Resources preset (CPU+RAM configuration)
                                            for the compute nodes of the cluster.
        :type computenode_resource_preset: str
        :param computenode_disk_size: Computenodes storage size in GiB.
        :type computenode_disk_size: int
        :param computenode_disk_type: Computenodes storage type. Possible options: network-ssd, network-hdd.
        :type computenode_disk_type: str

        :return: Cluster ID
        :rtype: str
        """

        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-locals

        folder_id = folder_id or self.default_folder_id
        if not folder_id:
            raise RuntimeError('Folder ID must be specified to create cluster.')

        if not cluster_name:
            random_int = random.randint(0, 999)
            cluster_name = 'dataproc-{random_int}'.format(random_int=random_int)

        if not subnet_id:
            network_id = self.sdk.helpers.find_network_id(folder_id)
            subnet_id = self.sdk.helpers.find_subnet_id(folder_id, zone, network_id)

        if not service_account_id:
            service_account_id = self.sdk.helpers.find_service_account_id(folder_id)

        if not ssh_public_keys:
            if self.default_public_ssh_key:
                ssh_public_keys = (self.default_public_ssh_key,)
            else:
                raise RuntimeError('Public ssh keys must be specified.')
        elif isinstance(ssh_public_keys, string_types):
            ssh_public_keys = [ssh_public_keys]

        if not s3_bucket:
            raise RuntimeError('Object storage (S3) bucket must be specified.')

        subclusters = [
            cluster_service_pb.CreateSubclusterConfigSpec(
                name='master',
                role=subcluster_pb.Role.MASTERNODE,
                resources=common_pb.Resources(
                    resource_preset_id=masternode_resource_preset,
                    disk_size=masternode_disk_size * (1024 ** 3),
                    disk_type_id=masternode_disk_type,
                ),
                subnet_id=subnet_id,
                hosts_count=1,
            ),
            cluster_service_pb.CreateSubclusterConfigSpec(
                name='data',
                role=subcluster_pb.Role.DATANODE,
                resources=common_pb.Resources(
                    resource_preset_id=datanode_resource_preset,
                    disk_size=datanode_disk_size * (1024 ** 3),
                    disk_type_id=datanode_disk_type,
                ),
                subnet_id=subnet_id,
                hosts_count=datanode_count,
            ),
        ]

        if computenode_count:
            subclusters.append(
                cluster_service_pb.CreateSubclusterConfigSpec(
                    name='compute',
                    role=subcluster_pb.Role.DATANODE,
                    resources=common_pb.Resources(
                        resource_preset_id=computenode_resource_preset,
                        disk_size=computenode_disk_size * (1024 ** 3),
                        disk_type_id=computenode_disk_type,
                    ),
                    subnet_id=subnet_id,
                    hosts_count=computenode_count,
                )
            )

        request = cluster_service_pb.CreateClusterRequest(
            folder_id=folder_id,
            name=cluster_name,
            description=cluster_description,
            config_spec=cluster_service_pb.CreateClusterConfigSpec(
                version_id=cluster_image_version,
                hadoop=cluster_pb.HadoopConfig(
                    services=services,
                    ssh_public_keys=ssh_public_keys,
                ),
                subclusters_spec=subclusters,
            ),
            zone_id=zone,
            service_account_id=service_account_id,
            bucket=s3_bucket,
        )
        result = self.sdk.create_operation_and_get_result(
            request,
            service=cluster_service_grpc_pb.ClusterServiceStub,
            method_name='Create',
            response_type=cluster_pb.Cluster,
            meta_type=cluster_service_pb.CreateClusterMetadata,
        )
        self.cluster_id = result.response.id
        self.subnet_id = subnet_id
        return result

    def create_subcluster(
        self,
        subcluster_type,
        name,
        resource_preset='s2.small',
        disk_size=15,
        disk_type='network-ssd',
        hosts_count=5,
        subnet_id=None,
        cluster_id=None,
    ):
        """
        Create subcluster to Yandex.Cloud Data Proc cluster.

        :param name: Name of the subcluster. Must be unique in the cluster
        :type name: str
        :param subcluster_type: Type of the subcluster. Either "data" or "compute".
        :type subcluster_type: str
        :param resource_preset: Resources preset (CPU+RAM configuration) for the nodes of the cluster.
        :type resource_preset: str
        :param disk_size: Storage size in GiB.
        :type disk_size: int
        :param disk_type: Storage type. Possible options: network-ssd, network-hdd.
        :type disk_type: str
        :param hosts_count: Number of nodes in subcluster.
        :type hosts_count: int
        :param subnet_id: Subnet ID of the cluster.
        :type subnet_id: str
        :param cluster_id: ID of the cluster.
        :type cluster_id: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')
        subnet_id = subnet_id or self.subnet_id
        if not subnet_id:
            raise RuntimeError('Subnet ID id must be specified.')

        types = {
            'compute': subcluster_pb.Role.COMPUTENODE,
            'data': subcluster_pb.Role.DATANODE,
        }
        resources = common_pb.Resources(
            resource_preset_id=resource_preset,
            disk_size=disk_size * (1024 ** 3),
            disk_type_id=disk_type,
        )

        self.log.info('Adding subcluster to cluster {cluster_id}'.format(cluster_id=cluster_id))
        request = subcluster_service_pb.CreateSubclusterRequest(
            cluster_id=cluster_id,
            name=name,
            role=types[subcluster_type],
            resources=resources,
            subnet_id=subnet_id,
            hosts_count=hosts_count,
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=subcluster_service_grpc_pb.SubclusterServiceStub,
            method_name='Create',
            response_type=subcluster_pb.Subcluster,
            meta_type=subcluster_service_pb.CreateSubclusterMetadata,
        )

    def update_cluster_description(self, description, cluster_id=None):
        """
        Changes Yandex.Cloud Data Proc cluster description.

        :param description: Description of the cluster.
        :type description: str
        :param cluster_id: ID of the cluster.
        :type cluster_id: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')

        self.log.info('Updating cluster {cluster_id}'.format(cluster_id=cluster_id))
        mask = FieldMask(paths=['description'])
        request = cluster_service_pb.UpdateClusterRequest(
            cluster_id=cluster_id,
            update_mask=mask,
            description=description,
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=cluster_service_grpc_pb.ClusterServiceStub,
            method_name='Update',
            response_type=cluster_pb.Cluster,
            meta_type=cluster_service_pb.UpdateClusterMetadata,
        )

    def delete_cluster(self, cluster_id=None):
        """
        Delete Yandex.Cloud Data Proc cluster.
        :param cluster_id: ID of the cluster to remove.
        :type cluster_id: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')

        self.log.info('Deleting cluster {cluster_id}'.format(cluster_id=cluster_id))
        request = cluster_service_pb.DeleteClusterRequest(cluster_id=cluster_id)
        return self.sdk.create_operation_and_get_result(
            request,
            service=cluster_service_grpc_pb.ClusterServiceStub,
            method_name='Delete',
            meta_type=cluster_service_pb.DeleteClusterMetadata,
        )

    def create_hive_job(
        self,
        query=None,
        query_file_uri=None,
        script_variables=None,
        continue_on_failure=False,
        properties=None,
        cluster_id=None,
        name='Hive job',
    ):
        """
        Run Hive job in Yandex.Cloud Data Proc cluster.

        :param query: Hive query.
        :type query: str
        :param query_file_uri: URI of the script that contains Hive queries. Can be placed in HDFS or S3.
        :type query_file_uri: str
        :param properties: A mapping of property names to values, used to configure Hive.
        :type properties: Dist[str, str]
        :param script_variables: Mapping of query variable names to values.
        :type script_variables: Dist[str, str]
        :param continue_on_failure: Whether to continue executing queries if a query fails.
        :type continue_on_failure: boole
        :param cluster_id: ID of the cluster to run job in.
                           Will try to take the ID from Dataproc Hook object if ot specified.
        :type cluster_id: str
        :param name: Name of the job. Used for labeling.
        :type name: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')
        if (query and query_file_uri) or not (query or query_file_uri):
            raise RuntimeError('Either query or query_file_uri must be specified.')
        self.log.info('Running Hive job. Cluster ID: {cluster_id}'.format(cluster_id=cluster_id))

        hive_job = job_pb.HiveJob(
            query_file_uri=query_file_uri,
            script_variables=script_variables,
            continue_on_failure=continue_on_failure,
            properties=properties,
        )
        if query:
            hive_job = job_pb.HiveJob(
                query_list=job_pb.QueryList(queries=query.split('\n')),
                script_variables=script_variables,
                continue_on_failure=continue_on_failure,
                properties=properties,
            )
        request = job_service_pb.CreateJobRequest(
            cluster_id=cluster_id,
            name=name,
            hive_job=hive_job,
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=job_service_grpc_pb.JobServiceStub,
            method_name='Create',
            response_type=job_pb.Job,
            meta_type=job_service_pb.CreateJobMetadata,
        )

    def create_mapreduce_job(
        self,
        main_class=None,
        main_jar_file_uri=None,
        jar_file_uris=None,
        archive_uris=None,
        file_uris=None,
        args=None,
        properties=None,
        cluster_id=None,
        name='Mapreduce job'
    ):
        """
        Run Mapreduce job in Yandex.Cloud Data Proc cluster.

        :param main_jar_file_uri: URI of jar file with job.
                                  Can be placed in HDFS or S3. Can be specified instead of main_class.
        :type main_class: str
        :param main_class: Name of the main class of the job. Can be specified instead of main_jar_file_uri.
        :type main_class: str
        :param file_uris: URIs of files used in the job. Can be placed in HDFS or S3.
        :type file_uris: List[str]
        :param archive_uris: URIs of archive files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param jar_file_uris: URIs of JAR files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param properties: Properties for the job.
        :type properties: Dist[str, str]
        :param args: Arguments to be passed to the job.
        :type args: List[str]
        :param cluster_id: ID of the cluster to run job in.
                           Will try to take the ID from Dataproc Hook object if ot specified.
        :type cluster_id: str
        :param name: Name of the job. Used for labeling.
        :type name: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')
        self.log.info('Running Mapreduce job. Cluster ID: {cluster_id}'.format(cluster_id=cluster_id))

        request = job_service_pb.CreateJobRequest(
            cluster_id=cluster_id,
            name=name,
            mapreduce_job=job_pb.MapreduceJob(
                main_class=main_class,
                main_jar_file_uri=main_jar_file_uri,
                jar_file_uris=jar_file_uris,
                archive_uris=archive_uris,
                file_uris=file_uris,
                args=args,
                properties=properties,
            )
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=job_service_grpc_pb.JobServiceStub,
            method_name='Create',
            response_type=job_pb.Job,
            meta_type=job_service_pb.CreateJobMetadata,
        )

    def create_spark_job(
        self,
        main_jar_file_uri=None,
        main_class=None,
        file_uris=None,
        archive_uris=None,
        jar_file_uris=None,
        args=None,
        properties=None,
        cluster_id=None,
        name='Spark job',
    ):
        """
        Run Spark job in Yandex.Cloud Data Proc cluster.

        :param main_jar_file_uri: URI of jar file with job. Can be placed in HDFS or S3.
        :type main_class: str
        :param main_class: Name of the main class of the job.
        :type main_class: str
        :param file_uris: URIs of files used in the job. Can be placed in HDFS or S3.
        :type file_uris: List[str]
        :param archive_uris: URIs of archive files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param jar_file_uris: URIs of JAR files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param properties: Properties for the job.
        :type properties: Dist[str, str]
        :param args: Arguments to be passed to the job.
        :type args: List[str]
        :param cluster_id: ID of the cluster to run job in.
                           Will try to take the ID from Dataproc Hook object if ot specified.
        :type cluster_id: str
        :param name: Name of the job. Used for labeling.
        :type name: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')
        self.log.info('Running Spark job. Cluster ID: {cluster_id}'.format(cluster_id=cluster_id))

        request = job_service_pb.CreateJobRequest(
            cluster_id=cluster_id,
            name=name,
            spark_job=job_pb.SparkJob(
                main_jar_file_uri=main_jar_file_uri,
                main_class=main_class,
                file_uris=file_uris,
                archive_uris=archive_uris,
                jar_file_uris=jar_file_uris,
                args=args,
                properties=properties,
            )
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=job_service_grpc_pb.JobServiceStub,
            method_name='Create',
            response_type=job_pb.Job,
            meta_type=job_service_pb.CreateJobMetadata,
        )

    def create_pyspark_job(
        self,
        main_python_file_uri=None,
        python_file_uris=None,
        file_uris=None,
        archive_uris=None,
        jar_file_uris=None,
        args=None,
        properties=None,
        cluster_id=None,
        name='Pyspark job',
    ):
        """
        Run Pyspark job in Yandex.Cloud Data Proc cluster.
        
        :param main_python_file_uri: URI of python file with job. Can be placed in HDFS or S3.
        :type main_python_file_uri: str
        :param python_file_uris: URIs of python files used in the job. Can be placed in HDFS or S3.
        :type python_file_uris: List[str]
        :param file_uris: URIs of files used in the job. Can be placed in HDFS or S3.
        :type file_uris: List[str]
        :param archive_uris: URIs of archive files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param jar_file_uris: URIs of JAR files used in the job. Can be placed in HDFS or S3.
        :type archive_uris: List[str]
        :param properties: Properties for the job.
        :type properties: Dist[str, str]
        :param args: Arguments to be passed to the job.
        :type args: List[str]
        :param cluster_id: ID of the cluster to run job in.
                           Will try to take the ID from Dataproc Hook object if ot specified.
        :type cluster_id: str        
        :param name: Name of the job. Used for labeling.
        :type name: str
        """
        cluster_id = cluster_id or self.cluster_id
        if not cluster_id:
            raise RuntimeError('Cluster id must be specified.')
        self.log.info('Running Pyspark job. Cluster ID: {cluster_id}'.format(cluster_id=cluster_id))
        request = job_service_pb.CreateJobRequest(
            cluster_id=cluster_id,
            name=name,
            pyspark_job=job_pb.PysparkJob(
                main_python_file_uri=main_python_file_uri,
                python_file_uris=python_file_uris,
                file_uris=file_uris,
                archive_uris=archive_uris,
                jar_file_uris=jar_file_uris,
                args=args,
                properties=properties,
            )
        )
        return self.sdk.create_operation_and_get_result(
            request,
            service=job_service_grpc_pb.JobServiceStub,
            method_name='Create',
            response_type=job_pb.Job,
            meta_type=job_service_pb.CreateJobMetadata,
        )
