import logging
import boto

from django.utils.translation import ugettext_lazy as _
from horizon import exceptions
from openstack_dashboard.api import keystone

LOG = logging.getLogger(__name__)

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

def get_cw_client(request):
    keys = _get_ec2_credentials(request)
    cw = boto.connect_cloudwatch(aws_access_key_id=keys.access, 
                                 aws_secret_access_key=keys.secret)
    LOG.info("cloudwatch connection: %s", cw)
    return cw