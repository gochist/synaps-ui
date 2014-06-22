from django.utils.translation import ugettext_lazy as _

import horizon

from synapsdashboard import dashboard


class Alarms(horizon.Panel):
    name = _("Alarms")
    slug = "alarms"


dashboard.SynapsDashboard.register(Alarms)
