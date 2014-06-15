from django.utils.translation import ugettext_lazy as _

import horizon

from synapsdashboard import dashboard


class Projects(horizon.Panel):
    name = _("Projects")
    slug = "projects"


dashboard.SynapsDashboard.register(Projects)
