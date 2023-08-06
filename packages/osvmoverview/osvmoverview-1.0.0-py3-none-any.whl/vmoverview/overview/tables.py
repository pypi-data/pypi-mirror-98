from django.utils.translation import ugettext_lazy as _

from horizon import tables
from horizon.templatetags import sizeformat

class AdminFlavorHypervisorsTable(tables.DataTable):
    name = tables.WrappingColumn("name",
                                     verbose_name=_("Flavor"))

    count = tables.Column("count",
                                    verbose_name=_("Count"))

    def get_object_id(self, flavor):
        return flavor.name

    class Meta(object):
        name = "hypervisorsflavor"
        verbose_name = _("Flavors")



class AdminHypervisorsTable(tables.DataTable):
    hostname = tables.WrappingColumn("hypervisor_hostname",
                                     verbose_name=_("Hostname"))

    hypervisor_type = tables.Column("hypervisor_type",
                                    verbose_name=_("Type"))

    vcpus_used = tables.Column("vcpus_used",
                               verbose_name=_("VCPUs (used)"))

    vcpus = tables.Column("vcpus",
                          verbose_name=_("VCPUs (total)"))

    memory_used = tables.Column('memory_mb_used',
                                verbose_name=_("RAM (used)"),
                                attrs={'data-type': 'size'},
                                filters=(sizeformat.mb_float_format,))

    memory = tables.Column('memory_mb',
                           verbose_name=_("RAM (total)"),
                           attrs={'data-type': 'size'},
                           filters=(sizeformat.mb_float_format,))

    local_used = tables.Column('local_gb_used',
                               verbose_name=_("Local Storage (used)"),
                               attrs={'data-type': 'size'},
                               filters=(sizeformat.diskgbformat,))

    local = tables.Column('local_gb',
                          verbose_name=_("Local Storage (total)"),
                          attrs={'data-type': 'size'},
                          filters=(sizeformat.diskgbformat,))

    running_vms = tables.Column("running_vms",
                                verbose_name=_("Instances"))

    def get_object_id(self, hypervisor):
        return "%s_%s" % (hypervisor.id,
                          hypervisor.hypervisor_hostname)

    class Meta(object):
        name = "hypervisors"
        verbose_name = _("Hypervisors")


class AdminHypervisorInstancesTable(tables.DataTable):
    name = tables.WrappingColumn("name",
                                 verbose_name=_("Instance Name"))

    instance_id = tables.Column("uuid",
                                verbose_name=_("Instance ID"))

    def get_object_id(self, server):
        return server['uuid']

    class Meta(object):
        name = "hypervisor_instances"
        verbose_name = _("Hypervisor Instances")
