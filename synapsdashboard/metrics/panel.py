from django.utils.translation import ugettext_lazy as _

import horizon

from synapsdashboard import dashboard


class Metrics(horizon.Panel):
    name = _("Metrics")
    slug = "metrics"


dashboard.SynapsDashboard.register(Metrics)
