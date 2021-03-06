# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import fields
from horizon.utils import validators

from openstack_dashboard import api



class GraphForm(forms.SelfHandlingForm):

    instance_id = forms.CharField(widget=forms.HiddenInput())
#     image = forms.ChoiceField(label=_("Select Image"),
#             widget=fields.SelectWidget(attrs={'class': 'image-selector'},
#                                        data_attrs=('size', 'display-name'),
#                                        transform=_image_choice_title))
#     password = forms.RegexField(label=_("Rebuild Password"),
#             required=False,
#             widget=forms.PasswordInput(render_value=False),
#             regex=validators.password_validator(),
#             error_messages={'invalid': validators.password_validator_msg()})
#     confirm_password = forms.CharField(label=_("Confirm Rebuild Password"),
#             required=False,
#             widget=forms.PasswordInput(render_value=False))
#     disk_config = forms.ChoiceField(label=_("Disk Partition"),
#                                     required=False)

    def __init__(self, request, *args, **kwargs):
        super(GraphForm, self).__init__(request, *args, **kwargs)
#         instance_id = kwargs.get('initial', {}).get('instance_id')
#         self.fields['instance_id'].initial = instance_id
# 
#         images = utils.get_available_images(request, request.user.tenant_id)
#         choices = [(image.id, image) for image in images]
#         if choices:
#             choices.insert(0, ("", _("Select Image")))
#         else:
#             choices.insert(0, ("", _("No images available")))
#         self.fields['image'].choices = choices
# 
#         if not api.nova.can_set_server_password():
#             del self.fields['password']
#             del self.fields['confirm_password']
# 
#         # Set our disk_config choices
#         config_choices = [("AUTO", _("Automatic")), ("MANUAL", _("Manual"))]
#         self.fields['disk_config'].choices = config_choices
# 
#     def clean(self):
#         cleaned_data = super(GraphForm, self).clean()
#         if 'password' in cleaned_data:
#             passwd = cleaned_data.get('password')
#             confirm = cleaned_data.get('confirm_password')
#             if passwd is not None and confirm is not None:
#                 if passwd != confirm:
#                     raise forms.ValidationError(_("Passwords do not match."))
#         return cleaned_data
# 
    
    # We have to protect the entire "data" dict because it contains the
    # password and confirm_password strings.
#     @sensitive_variables('data', 'password')
    def handle(self, request, data):
#         instance = data.get('instance_id')
#         image = data.get('image')
#         password = data.get('password') or None
#         disk_config = data.get('disk_config', None)
#         try:
#             api.nova.server_rebuild(request, instance, image, password,
#                                     disk_config)
#             messages.success(request, _('Rebuilding instance %s.') % instance)
#         except Exception:
#             redirect = reverse('horizon:project:instances:index')
#             exceptions.handle(request, _("Unable to rebuild instance."),
#                               redirect=redirect)
        return True

