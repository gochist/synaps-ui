from django.utils.translation import ugettext_lazy as _

import horizon

from synapsdashboard import dashboard


class Reports(horizon.Panel):
    name = _("Reports")
    slug = "reports"


dashboard.SynapsDashboard.register(Reports)
