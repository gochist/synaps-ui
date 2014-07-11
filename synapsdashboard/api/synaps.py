import logging
import boto
from boto.regioninfo import RegionInfo

from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from openstack_dashboard.api import keystone

from django.conf import settings


LOG = logging.getLogger(__name__)

REGION_NAME = getattr(settings, "SYNAPS_REGION_NAME", "SPCS")
REGION_ENDPOINT = getattr(settings, "SYNAPS_REGION_ENDPOINT", "synapsapi")
SSL = getattr(settings, "SYNAPS_SSL", False)
PORT = getattr(settings, "SYNAPS_PORT", 3776)
ACCESS_KEY = getattr(settings, "SYNAPS_ADMIN_AWS_ACCESS_KEY_ID", "accesskey")
SECRET_KEY = getattr(settings, "SYNAPS_ADMIN_AWS_SECRET_ACCESS_KEY", 
                     "secretkey")
AUTH_BACKEND = getattr(settings, "SYNAPS_AUTH", "KEYSTONE")


def _get_ec2_credentials(request):
    tenant_id = request.user.tenant_id
    
    try:
        all_keys = keystone.list_ec2_credentials(request,
                                                 request.user.id)
        keys = None
        for key in all_keys:
            if key.tenant_id == tenant_id:
                keys = key
        if keys is None:
            keys = keystone.create_ec2_credentials(request,
                                                   request.user.id,
                                                   tenant_id)
    except Exception:
        exceptions.handle(request,
                          _('Unable to fetch EC2 credentials.'),
                          redirect=request.build_absolute_url())
    
    return keys


def _get_ec2_credentials_from_ldap(request):
    pass


if AUTH_BACKEND == "LDAP":
    _get_ec2_credentials = _get_ec2_credentials_from_ldap


def get_cw_client(request):
    region = RegionInfo(name=REGION_NAME, endpoint=REGION_ENDPOINT)

    keys = _get_ec2_credentials(request)
    cw = boto.connect_cloudwatch(aws_access_key_id=keys.access,
                                 aws_secret_access_key=keys.secret,
                                 is_secure=SSL, port=PORT, region=region)
    return cw

