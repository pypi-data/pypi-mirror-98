"""
memballoon device support class(es)

http://libvirt.org/formatdomain.html#elementsMemBalloon
"""

from virttest.libvirt_xml import accessors
from virttest.libvirt_xml.devices import base


class Memballoon(base.UntypedDeviceBase):

    __slots__ = ('model', 'stats_period', 'address', 'driver_packed')

    def __init__(self, virsh_instance=base.base.virsh):
        accessors.XMLAttribute('model', self, parent_xpath='/',
                               tag_name='memballoon', attribute='model')
        accessors.XMLAttribute('stats_period', self, parent_xpath='/',
                               tag_name='stats', attribute='period')
        accessors.XMLElementDict('address', self, parent_xpath='/',
                                 tag_name='address')
        accessors.XMLAttribute('driver_packed', self, parent_xpath='/',
                               tag_name='driver', attribute='packed')
        super(Memballoon, self).__init__(device_tag='memballoon',
                                         virsh_instance=virsh_instance)
