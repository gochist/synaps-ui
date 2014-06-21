from django.utils.translation import ugettext_lazy as _

import horizon

from synapsdashboard import dashboard


class Overview(horizon.Panel):
    name = _("Overview")
    slug = "overview"


dashboard.SynapsDashboard.register(Overview)
