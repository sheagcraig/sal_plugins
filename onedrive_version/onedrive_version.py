from django.db.models import Count

import sal.plugin
from inventory.models import InventoryItem


class OneDriveVersion(sal.plugin.Widget):

    description = "Microsoft OneDrive Version"

    def get_context(self, queryset, **kwargs):
        context = self.super_get_context(queryset, **kwargs)
        context['data'] = (
             InventoryItem.objects.filter(
                 machine__in=queryset,
                 application__name="OneDrive",
                 application__bundleid__startswith="com.microsoft") 
             .values("version")
             .annotate(count=Count("version"))
             .order_by("version"))

        return context

    def filter_machines(self, machines, data):
        machines = machines.filter(inventoryitem__application__name="OneDrive",
                                   inventoryitem__version=data,
                                   inventoryitem__application__bundleid__startswith="com.microsoft")

        return machines, "Machines with version {} of Microsoft OneDrive".format(data)
