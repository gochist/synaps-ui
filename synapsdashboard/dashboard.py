from django.utils.translation import ugettext_lazy as _

import horizon

class ProjectPanels(horizon.PanelGroup):
    name = _("Project Panel")
    slug = "project"
    panels = ("alarms", "metrics", "reports",)

class AdminPanels(horizon.PanelGroup):
    name = _("Admin Panel")
    slug = "admin"
    panels = ('projects',)

class SynapsDashboard(horizon.Dashboard):
    name = _("Synaps")
    slug = "synapsdashboard"
    panels = (ProjectPanels, AdminPanels,)  # Add your panels here.
    default_panel = 'alarms'  # Specify the slug of the dashboard's default panel.


horizon.register(SynapsDashboard)
