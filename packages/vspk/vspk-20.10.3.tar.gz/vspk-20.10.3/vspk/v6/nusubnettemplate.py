# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc, 2017 Nokia
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.




from .fetchers import NUAddressRangesFetcher


from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUQOSsFetcher


from .fetchers import NUSubnetsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUSubnetTemplate(NURESTObject):
    """ Represents a SubnetTemplate in the VSD

        Notes:
            As domain and zone objects, subnet objects are created in VSD as derived by templates. This object describes the subnet template.
    """

    __rest_name__ = "subnettemplate"
    __resource_name__ = "subnettemplates"

    
    ## Constants
    
    CONST_USE_GLOBAL_MAC_DISABLED = "DISABLED"
    
    CONST_USE_GLOBAL_MAC_ENABLED = "ENABLED"
    
    CONST_MULTICAST_DISABLED = "DISABLED"
    
    CONST_ENCRYPTION_ENABLED = "ENABLED"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENCRYPTION_DISABLED = "DISABLED"
    
    CONST_USE_GLOBAL_MAC_ENTERPRISE_DEFAULT = "ENTERPRISE_DEFAULT"
    
    CONST_DPI_ENABLED = "ENABLED"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_IP_TYPE_IPV6 = "IPV6"
    
    CONST_DPI_INHERITED = "INHERITED"
    
    CONST_IP_TYPE_IPV4 = "IPV4"
    
    CONST_MULTICAST_ENABLED = "ENABLED"
    
    CONST_MULTICAST_INHERITED = "INHERITED"
    
    CONST_DPI_DISABLED = "DISABLED"
    
    CONST_ENCRYPTION_INHERITED = "INHERITED"
    
    CONST_IP_TYPE_DUALSTACK = "DUALSTACK"
    
    

    def __init__(self, **kwargs):
        """ Initializes a SubnetTemplate instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> subnettemplate = NUSubnetTemplate(id=u'xxxx-xxx-xxx-xxx', name=u'SubnetTemplate')
                >>> subnettemplate = NUSubnetTemplate(data=my_dict)
        """

        super(NUSubnetTemplate, self).__init__()

        # Read/Write Attributes
        
        self._dpi = None
        self._ip_type = None
        self._ipv6_address = None
        self._ipv6_gateway = None
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._gateway = None
        self._address = None
        self._description = None
        self._netmask = None
        self._embedded_metadata = None
        self._encryption = None
        self._entity_scope = None
        self._split_subnet = None
        self._creation_date = None
        self._proxy_arp = None
        self._use_global_mac = None
        self._associated_multicast_channel_map_id = None
        self._dual_stack_dynamic_ip_allocation = None
        self._multicast = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="dpi", remote_name="DPI", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'INHERITED'])
        self.expose_attribute(local_name="ip_type", remote_name="IPType", attribute_type=str, is_required=False, is_unique=False, choices=[u'DUALSTACK', u'IPV4', u'IPV6'])
        self.expose_attribute(local_name="ipv6_address", remote_name="IPv6Address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ipv6_gateway", remote_name="IPv6Gateway", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="gateway", remote_name="gateway", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="netmask", remote_name="netmask", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="encryption", remote_name="encryption", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'INHERITED'])
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="split_subnet", remote_name="splitSubnet", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="proxy_arp", remote_name="proxyARP", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="use_global_mac", remote_name="useGlobalMAC", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'ENTERPRISE_DEFAULT'])
        self.expose_attribute(local_name="associated_multicast_channel_map_id", remote_name="associatedMulticastChannelMapID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="dual_stack_dynamic_ip_allocation", remote_name="dualStackDynamicIPAllocation", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="multicast", remote_name="multicast", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'INHERITED'])
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.address_ranges = NUAddressRangesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.qoss = NUQOSsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.subnets = NUSubnetsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def dpi(self):
        """ Get dpi value.

            Notes:
                determines whether or not Deep packet inspection is enabled

                
                This attribute is named `DPI` in VSD API.
                
        """
        return self._dpi

    @dpi.setter
    def dpi(self, value):
        """ Set dpi value.

            Notes:
                determines whether or not Deep packet inspection is enabled

                
                This attribute is named `DPI` in VSD API.
                
        """
        self._dpi = value

    
    @property
    def ip_type(self):
        """ Get ip_type value.

            Notes:
                IPv4, DUALSTACK or IPv6

                
                This attribute is named `IPType` in VSD API.
                
        """
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value):
        """ Set ip_type value.

            Notes:
                IPv4, DUALSTACK or IPv6

                
                This attribute is named `IPType` in VSD API.
                
        """
        self._ip_type = value

    
    @property
    def ipv6_address(self):
        """ Get ipv6_address value.

            Notes:
                IPv6 range of the subnet. In case of zone, this is an optional field for and allows users to allocate an IP address range to a zone. The VSD will auto-assign IP addresses to subnets from this range if a specific IP address is not defined for the subnet

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        return self._ipv6_address

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ Set ipv6_address value.

            Notes:
                IPv6 range of the subnet. In case of zone, this is an optional field for and allows users to allocate an IP address range to a zone. The VSD will auto-assign IP addresses to subnets from this range if a specific IP address is not defined for the subnet

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        self._ipv6_address = value

    
    @property
    def ipv6_gateway(self):
        """ Get ipv6_gateway value.

            Notes:
                The IPv6 address of the gateway of this subnet

                
                This attribute is named `IPv6Gateway` in VSD API.
                
        """
        return self._ipv6_gateway

    @ipv6_gateway.setter
    def ipv6_gateway(self, value):
        """ Set ipv6_gateway value.

            Notes:
                The IPv6 address of the gateway of this subnet

                
                This attribute is named `IPv6Gateway` in VSD API.
                
        """
        self._ipv6_gateway = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the current entity(Zone or zone template or subnet etc..) Valid characters are alphabets, numbers, space and hyphen( - ).

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the current entity(Zone or zone template or subnet etc..) Valid characters are alphabets, numbers, space and hyphen( - ).

                
        """
        self._name = value

    
    @property
    def last_updated_by(self):
        """ Get last_updated_by value.

            Notes:
                ID of the user who last updated the object.

                
                This attribute is named `lastUpdatedBy` in VSD API.
                
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, value):
        """ Set last_updated_by value.

            Notes:
                ID of the user who last updated the object.

                
                This attribute is named `lastUpdatedBy` in VSD API.
                
        """
        self._last_updated_by = value

    
    @property
    def last_updated_date(self):
        """ Get last_updated_date value.

            Notes:
                Time stamp when this object was last updated.

                
                This attribute is named `lastUpdatedDate` in VSD API.
                
        """
        return self._last_updated_date

    @last_updated_date.setter
    def last_updated_date(self, value):
        """ Set last_updated_date value.

            Notes:
                Time stamp when this object was last updated.

                
                This attribute is named `lastUpdatedDate` in VSD API.
                
        """
        self._last_updated_date = value

    
    @property
    def gateway(self):
        """ Get gateway value.

            Notes:
                The IP address of the gateway of this subnet

                
        """
        return self._gateway

    @gateway.setter
    def gateway(self, value):
        """ Set gateway value.

            Notes:
                The IP address of the gateway of this subnet

                
        """
        self._gateway = value

    
    @property
    def address(self):
        """ Get address value.

            Notes:
                IP address of the subnet defined. In case of zone, this is an optional field for and allows users to allocate an IP address range to a zone. The VSD will auto-assign IP addresses to subnets from this range if a specific IP address is not defined for the subnet

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                IP address of the subnet defined. In case of zone, this is an optional field for and allows users to allocate an IP address range to a zone. The VSD will auto-assign IP addresses to subnets from this range if a specific IP address is not defined for the subnet

                
        """
        self._address = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description field provided by the user that identifies the subnet

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description field provided by the user that identifies the subnet

                
        """
        self._description = value

    
    @property
    def netmask(self):
        """ Get netmask value.

            Notes:
                Netmask of the subnet defined

                
        """
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        """ Set netmask value.

            Notes:
                Netmask of the subnet defined

                
        """
        self._netmask = value

    
    @property
    def embedded_metadata(self):
        """ Get embedded_metadata value.

            Notes:
                Metadata objects associated with this entity. This will contain a list of Metadata objects if the API request is made using the special flag to enable the embedded Metadata feature. Only a maximum of Metadata objects is returned based on the value set in the system configuration.

                
                This attribute is named `embeddedMetadata` in VSD API.
                
        """
        return self._embedded_metadata

    @embedded_metadata.setter
    def embedded_metadata(self, value):
        """ Set embedded_metadata value.

            Notes:
                Metadata objects associated with this entity. This will contain a list of Metadata objects if the API request is made using the special flag to enable the embedded Metadata feature. Only a maximum of Metadata objects is returned based on the value set in the system configuration.

                
                This attribute is named `embeddedMetadata` in VSD API.
                
        """
        self._embedded_metadata = value

    
    @property
    def encryption(self):
        """ Get encryption value.

            Notes:
                Determines whether or not IPSEC is enabled. Possible values are INHERITED, ENABLED, DISABLED, .

                
        """
        return self._encryption

    @encryption.setter
    def encryption(self, value):
        """ Set encryption value.

            Notes:
                Determines whether or not IPSEC is enabled. Possible values are INHERITED, ENABLED, DISABLED, .

                
        """
        self._encryption = value

    
    @property
    def entity_scope(self):
        """ Get entity_scope value.

            Notes:
                Specify if scope of entity is Data center or Enterprise level

                
                This attribute is named `entityScope` in VSD API.
                
        """
        return self._entity_scope

    @entity_scope.setter
    def entity_scope(self, value):
        """ Set entity_scope value.

            Notes:
                Specify if scope of entity is Data center or Enterprise level

                
                This attribute is named `entityScope` in VSD API.
                
        """
        self._entity_scope = value

    
    @property
    def split_subnet(self):
        """ Get split_subnet value.

            Notes:
                Block subnet routes

                
                This attribute is named `splitSubnet` in VSD API.
                
        """
        return self._split_subnet

    @split_subnet.setter
    def split_subnet(self, value):
        """ Set split_subnet value.

            Notes:
                Block subnet routes

                
                This attribute is named `splitSubnet` in VSD API.
                
        """
        self._split_subnet = value

    
    @property
    def creation_date(self):
        """ Get creation_date value.

            Notes:
                Time stamp when this object was created.

                
                This attribute is named `creationDate` in VSD API.
                
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value):
        """ Set creation_date value.

            Notes:
                Time stamp when this object was created.

                
                This attribute is named `creationDate` in VSD API.
                
        """
        self._creation_date = value

    
    @property
    def proxy_arp(self):
        """ Get proxy_arp value.

            Notes:
                 When set, VRS will act as  ARP Proxy

                
                This attribute is named `proxyARP` in VSD API.
                
        """
        return self._proxy_arp

    @proxy_arp.setter
    def proxy_arp(self, value):
        """ Set proxy_arp value.

            Notes:
                 When set, VRS will act as  ARP Proxy

                
                This attribute is named `proxyARP` in VSD API.
                
        """
        self._proxy_arp = value

    
    @property
    def use_global_mac(self):
        """ Get use_global_mac value.

            Notes:
                if this flag is enabled, the system configured globalMACAddress will be used as the gateway mac address

                
                This attribute is named `useGlobalMAC` in VSD API.
                
        """
        return self._use_global_mac

    @use_global_mac.setter
    def use_global_mac(self, value):
        """ Set use_global_mac value.

            Notes:
                if this flag is enabled, the system configured globalMACAddress will be used as the gateway mac address

                
                This attribute is named `useGlobalMAC` in VSD API.
                
        """
        self._use_global_mac = value

    
    @property
    def associated_multicast_channel_map_id(self):
        """ Get associated_multicast_channel_map_id value.

            Notes:
                The ID of the Multi Cast Channel Map  this Subnet/Subnet Template is associated with. This has to be set when enableMultiCast is set to ENABLED

                
                This attribute is named `associatedMulticastChannelMapID` in VSD API.
                
        """
        return self._associated_multicast_channel_map_id

    @associated_multicast_channel_map_id.setter
    def associated_multicast_channel_map_id(self, value):
        """ Set associated_multicast_channel_map_id value.

            Notes:
                The ID of the Multi Cast Channel Map  this Subnet/Subnet Template is associated with. This has to be set when enableMultiCast is set to ENABLED

                
                This attribute is named `associatedMulticastChannelMapID` in VSD API.
                
        """
        self._associated_multicast_channel_map_id = value

    
    @property
    def dual_stack_dynamic_ip_allocation(self):
        """ Get dual_stack_dynamic_ip_allocation value.

            Notes:
                This value indicates whether dynamic address allocation is enabled or not. This will be applicable when subnet template is in dual stack mode

                
                This attribute is named `dualStackDynamicIPAllocation` in VSD API.
                
        """
        return self._dual_stack_dynamic_ip_allocation

    @dual_stack_dynamic_ip_allocation.setter
    def dual_stack_dynamic_ip_allocation(self, value):
        """ Set dual_stack_dynamic_ip_allocation value.

            Notes:
                This value indicates whether dynamic address allocation is enabled or not. This will be applicable when subnet template is in dual stack mode

                
                This attribute is named `dualStackDynamicIPAllocation` in VSD API.
                
        """
        self._dual_stack_dynamic_ip_allocation = value

    
    @property
    def multicast(self):
        """ Get multicast value.

            Notes:
                Indicates multicast policy on Subnet/Subnet Template.

                
        """
        return self._multicast

    @multicast.setter
    def multicast(self, value):
        """ Set multicast value.

            Notes:
                Indicates multicast policy on Subnet/Subnet Template.

                
        """
        self._multicast = value

    
    @property
    def owner(self):
        """ Get owner value.

            Notes:
                Identifies the user that has created this object.

                
        """
        return self._owner

    @owner.setter
    def owner(self, value):
        """ Set owner value.

            Notes:
                Identifies the user that has created this object.

                
        """
        self._owner = value

    
    @property
    def external_id(self):
        """ Get external_id value.

            Notes:
                External object ID. Used for integration with third party systems

                
                This attribute is named `externalID` in VSD API.
                
        """
        return self._external_id

    @external_id.setter
    def external_id(self, value):
        """ Set external_id value.

            Notes:
                External object ID. Used for integration with third party systems

                
                This attribute is named `externalID` in VSD API.
                
        """
        self._external_id = value

    

    
    ## Custom methods
    def is_template(self):
        """ Verify that the object is a template
    
            Returns:
                (bool): True if the object is a template
        """
        return True
    
    def is_from_template(self):
        """ Verify if the object has been instantiated from a template
    
            Note:
                The object has to be fetched. Otherwise, it does not
                have information from its parent
    
            Returns:
                (bool): True if the object is a template
        """
        return False
    