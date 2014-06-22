from django.utils.translation import ugettext_lazy as _

import horizon


class SynapsDashboard(horizon.Dashboard):
    name = _("Synaps")
    slug = "synapsdashboard"
    panels = ('overview', 'alarms', 'metrics', 'projects', )  # Add your panels here.
    default_panel = 'overview'  # Specify the slug of the dashboard's default panel.


horizon.register(SynapsDashboard)