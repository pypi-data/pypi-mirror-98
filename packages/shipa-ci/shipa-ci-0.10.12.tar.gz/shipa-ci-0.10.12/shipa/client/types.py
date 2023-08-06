from schematics import Model
from schematics.types import StringType, BooleanType, ListType, ModelType, IntType, DictType

from shipa.commands.constant import KUBERNETES_PROVISIONER

class AppExistsError(Exception):
    pass

class NodeMetadata(Model):
    address = StringType(required=True)
    driver = StringType(required=True)
    iaas = StringType(required=True, default='dockermachine')
    iaas_id = StringType(serialized_name='iaas-id', serialize_when_none=False)
    template = StringType(serialize_when_none=False)


class AddNodeRequest(Model):
    alternative_pools = ListType(StringType, serialized_name='alternativePools', default=tuple())
    ca_cert = StringType(serialized_name='caCert', serialize_when_none=False)
    client_cert = StringType(serialized_name='clientCert', serialize_when_none=False)
    client_key = StringType(serialized_name='clientKey', serialize_when_none=False)
    meta_data = ModelType(NodeMetadata, serialized_name='metaData', required=True)
    pool = StringType(serialized_name='pool', required=True)
    register = BooleanType()


class UpdateFrameworkRequest(Model):
    accept_drivers = ListType(StringType, serialized_name='acceptdriver', default=tuple())
    app_quota_limit = IntType(serialized_name='appquotalimit', serialize_when_none=False)
    default = BooleanType(serialize_when_none=False, default=False)
    force = BooleanType(default=True)
    plan = StringType(serialize_when_none=False)
    public = BooleanType(serialize_when_none=False, default=False)


class AddFrameworkRequest(Model):
    accept_drivers = ListType(StringType, serialized_name='acceptdriver', default=tuple())
    app_quota_limit = IntType(serialized_name='appquotalimit', serialize_when_none=False)
    default = BooleanType(serialize_when_none=False, default=False)
    force = BooleanType(default=True)
    kubernetes_namespace = StringType(serialized_name='kubernetesnamespace', serialize_when_none=False)
    name = StringType(required=True)
    plan = StringType(serialize_when_none=False)
    provisioner = StringType(serialize_when_none=False)
    public = BooleanType(serialize_when_none=False, default=False)
    router = StringType(serialize_when_none=False)
    teams = ListType(StringType, default=tuple())


class RemoveFrameworkRequest(Model):
    address = StringType(required=True)
    destroy = BooleanType(serialized_name='remove-iaas', default=False)
    no_rebalance = BooleanType(serialized_name='no-rebalance', default=False)


class AddAppRequest(Model):
    description = StringType(serialize_when_none=False)
    dependency_files = ListType(StringType, serialized_name='dependency_filenames', default=tuple(), serialize_when_none=False)
    name = StringType(required=True)
    plan = StringType(serialize_when_none=False)
    platform = StringType(serialize_when_none=False)
    pool = StringType(serialize_when_none=False)
    tags = ListType(StringType, default=tuple())
    team = StringType(serialized_name='teamOwner', required=True)


class DeployAppRequest(Model):
    image = StringType(serialize_when_none=False)
    kind = StringType(default='git')
    port_number = StringType(serialize_when_none=False, serialized_name='port-number')
    port_protocol = StringType(serialize_when_none=False, serialized_name='port-protocol')
    registry_secret = StringType(serialize_when_none=False, serialized_name='registry-secret')
    registry_user = StringType(serialize_when_none=False, serialized_name='registry-user')
    steps = IntType(default=1)
    step_weight = IntType(serialized_name='step-weight', default=100)
    step_interval = IntType(serialized_name='step-interval', default=1)


class MoveAppRequest(Model):
    pool = StringType(required=True)


class IngressControllerConfig(Model):
    ingress_ip = StringType(serialize_when_none=False)
    ingress_http_port = IntType(serialize_when_none=False)
    ingress_https_port = IntType(serialize_when_none=False)
    ingress_protected_port = IntType(serialize_when_none=False)
    ingress_service = StringType(serialized_name='ingress_service_type', serialize_when_none=False)


class AddClusterRequest(Model):
    address = ListType(StringType, serialized_name='addresses', default=tuple())
    ca_cert = StringType(serialized_name='caCert', serialize_when_none=False)
    client_cert = StringType(serialized_name='clientCert', serialize_when_none=False)
    client_key = StringType(serialized_name='clientKey', serialize_when_none=False)
    custom_data = DictType(StringType, default=dict())
    default = BooleanType(serialize_when_none=False, default=False)
    ingress_controllers = DictType(ModelType(IngressControllerConfig), serialize_when_none=False)
    install_cert_manager = BooleanType(serialize_when_none=False, default=False)
    name = StringType(required=True)
    pools = ListType(StringType, default=tuple())
    provisioner = StringType(default=KUBERNETES_PROVISIONER)
    teams = ListType(StringType, default=tuple())
    token = StringType(serialize_when_none=False)


class Env(Model):
    name = StringType(required=True)
    value = StringType(required=True)


class EnvSetRequest(Model):
    envs = ListType(ModelType(Env), default=tuple())
    no_restart = BooleanType(serialized_name='noRestart', default=False)
    private = BooleanType(serialized_name='private', default=False)


class EnvUnsetRequest(Model):
    envs = ListType(StringType, serialized_name='env', default=tuple())
    no_restart = BooleanType(serialized_name='noRestart', default=False)
