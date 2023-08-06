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




from .fetchers import NUL2DomainsFetcher


from .fetchers import NUAddressRangesFetcher


from .fetchers import NURedirectionTargetTemplatesFetcher


from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUPGExpressionTemplatesFetcher


from .fetchers import NUEgressACLTemplatesFetcher


from .fetchers import NUEgressAdvFwdTemplatesFetcher


from .fetchers import NUVirtualFirewallPoliciesFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUIngressACLTemplatesFetcher


from .fetchers import NUIngressAdvFwdTemplatesFetcher


from .fetchers import NUJobsFetcher


from .fetchers import NUPolicyGroupTemplatesFetcher


from .fetchers import NUQOSsFetcher


from .fetchers import NUGroupsFetcher


from .fetchers import NUEventLogsFetcher


from .fetchers import NUOverlayMirrorDestinationTemplatesFetcher

from bambou import NURESTObject


class NUL2DomainTemplate(NURESTObject):
    """ Represents a L2DomainTemplate in the VSD

        Notes:
            An L2 Domain is a distributed logical switch that enables L2 communication. An L2 Domain template is a model that can be instantiated as often as required, thereby creating real, functioning L2 Domains.
    """

    __rest_name__ = "l2domaintemplate"
    __resource_name__ = "l2domaintemplates"

    
    ## Constants
    
    CONST_USE_GLOBAL_MAC_DISABLED = "DISABLED"
    
    CONST_USE_GLOBAL_MAC_ENABLED = "ENABLED"
    
    CONST_MULTICAST_DISABLED = "DISABLED"
    
    CONST_POLICY_CHANGE_STATUS_STARTED = "STARTED"
    
    CONST_ENCRYPTION_ENABLED = "ENABLED"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENCRYPTION_DISABLED = "DISABLED"
    
    CONST_POLICY_CHANGE_STATUS_DISCARDED = "DISCARDED"
    
    CONST_DPI_ENABLED = "ENABLED"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_DPI_INHERITED = "INHERITED"
    
    CONST_IP_TYPE_IPV4 = "IPV4"
    
    CONST_MULTICAST_ENABLED = "ENABLED"
    
    CONST_MULTICAST_INHERITED = "INHERITED"
    
    CONST_DPI_DISABLED = "DISABLED"
    
    CONST_IP_TYPE_DUALSTACK = "DUALSTACK"
    
    CONST_ENTITY_STATE_MARKED_FOR_DELETION = "MARKED_FOR_DELETION"
    
    CONST_POLICY_CHANGE_STATUS_APPLIED = "APPLIED"
    
    CONST_ENTITY_STATE_UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"
    
    

    def __init__(self, **kwargs):
        """ Initializes a L2DomainTemplate instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> l2domaintemplate = NUL2DomainTemplate(id=u'xxxx-xxx-xxx-xxx', name=u'L2DomainTemplate')
                >>> l2domaintemplate = NUL2DomainTemplate(data=my_dict)
        """

        super(NUL2DomainTemplate, self).__init__()

        # Read/Write Attributes
        
        self._dhcp_managed = None
        self._dpi = None
        self._ip_type = None
        self._ipv6_address = None
        self._ipv6_gateway = None
        self._name = None
        self._last_updated_by = None
        self._gateway = None
        self._address = None
        self._description = None
        self._netmask = None
        self._encryption = None
        self._entity_scope = None
        self._entity_state = None
        self._policy_change_status = None
        self._use_global_mac = None
        self._associated_multicast_channel_map_id = None
        self._multicast = None
        self._external_id = None
        self._dynamic_ipv6_address = None
        
        self.expose_attribute(local_name="dhcp_managed", remote_name="DHCPManaged", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="dpi", remote_name="DPI", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'INHERITED'])
        self.expose_attribute(local_name="ip_type", remote_name="IPType", attribute_type=str, is_required=False, is_unique=False, choices=[u'DUALSTACK', u'IPV4'])
        self.expose_attribute(local_name="ipv6_address", remote_name="IPv6Address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ipv6_gateway", remote_name="IPv6Gateway", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="gateway", remote_name="gateway", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="netmask", remote_name="netmask", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="encryption", remote_name="encryption", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED'])
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="entity_state", remote_name="entityState", attribute_type=str, is_required=False, is_unique=False, choices=[u'MARKED_FOR_DELETION', u'UNDER_CONSTRUCTION'])
        self.expose_attribute(local_name="policy_change_status", remote_name="policyChangeStatus", attribute_type=str, is_required=False, is_unique=False, choices=[u'APPLIED', u'DISCARDED', u'STARTED'])
        self.expose_attribute(local_name="use_global_mac", remote_name="useGlobalMAC", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED'])
        self.expose_attribute(local_name="associated_multicast_channel_map_id", remote_name="associatedMulticastChannelMapID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="multicast", remote_name="multicast", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED', u'INHERITED'])
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="dynamic_ipv6_address", remote_name="dynamicIpv6Address", attribute_type=bool, is_required=False, is_unique=False)
        

        # Fetchers
        
        
        self.l2_domains = NUL2DomainsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.address_ranges = NUAddressRangesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.redirection_target_templates = NURedirectionTargetTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.pg_expression_templates = NUPGExpressionTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.egress_acl_templates = NUEgressACLTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.egress_adv_fwd_templates = NUEgressAdvFwdTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.virtual_firewall_policies = NUVirtualFirewallPoliciesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ingress_acl_templates = NUIngressACLTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ingress_adv_fwd_templates = NUIngressAdvFwdTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.jobs = NUJobsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.policy_group_templates = NUPolicyGroupTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.qoss = NUQOSsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.groups = NUGroupsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.overlay_mirror_destination_templates = NUOverlayMirrorDestinationTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def dhcp_managed(self):
        """ Get dhcp_managed value.

            Notes:
                decides whether L2Domain / L2Domain template DHCP is managed by VSD

                
                This attribute is named `DHCPManaged` in VSD API.
                
        """
        return self._dhcp_managed

    @dhcp_managed.setter
    def dhcp_managed(self, value):
        """ Set dhcp_managed value.

            Notes:
                decides whether L2Domain / L2Domain template DHCP is managed by VSD

                
                This attribute is named `DHCPManaged` in VSD API.
                
        """
        self._dhcp_managed = value

    
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
                IPv4 or DUALSTACK

                
                This attribute is named `IPType` in VSD API.
                
        """
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value):
        """ Set ip_type value.

            Notes:
                IPv4 or DUALSTACK

                
                This attribute is named `IPType` in VSD API.
                
        """
        self._ip_type = value

    
    @property
    def ipv6_address(self):
        """ Get ipv6_address value.

            Notes:
                IPV6 address of the route - Optional

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        return self._ipv6_address

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ Set ipv6_address value.

            Notes:
                IPV6 address of the route - Optional

                
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
                Name of the L2Domain / L2Domain template,has to be unique within a Enterprise. Valid characters are alphabets, numbers, space and hyphen( - ).

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the L2Domain / L2Domain template,has to be unique within a Enterprise. Valid characters are alphabets, numbers, space and hyphen( - ).

                
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
    def gateway(self):
        """ Get gateway value.

            Notes:
                The IP address of the gateway of this l2 domain

                
        """
        return self._gateway

    @gateway.setter
    def gateway(self, value):
        """ Set gateway value.

            Notes:
                The IP address of the gateway of this l2 domain

                
        """
        self._gateway = value

    
    @property
    def address(self):
        """ Get address value.

            Notes:
                Network address of the L2Domain / L2Domain template defined. 

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                Network address of the L2Domain / L2Domain template defined. 

                
        """
        self._address = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description field provided by the user that identifies the L2Domain / L2Domain template.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description field provided by the user that identifies the L2Domain / L2Domain template.

                
        """
        self._description = value

    
    @property
    def netmask(self):
        """ Get netmask value.

            Notes:
                Netmask of the L2Domain / L2Domain template defined

                
        """
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        """ Set netmask value.

            Notes:
                Netmask of the L2Domain / L2Domain template defined

                
        """
        self._netmask = value

    
    @property
    def encryption(self):
        """ Get encryption value.

            Notes:
                Determines whether IPSEC is enabled Possible values are ENABLED, DISABLED, .

                
        """
        return self._encryption

    @encryption.setter
    def encryption(self, value):
        """ Set encryption value.

            Notes:
                Determines whether IPSEC is enabled Possible values are ENABLED, DISABLED, .

                
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
    def entity_state(self):
        """ Get entity_state value.

            Notes:
                Intermediate State of L2 Domain.

                
                This attribute is named `entityState` in VSD API.
                
        """
        return self._entity_state

    @entity_state.setter
    def entity_state(self, value):
        """ Set entity_state value.

            Notes:
                Intermediate State of L2 Domain.

                
                This attribute is named `entityState` in VSD API.
                
        """
        self._entity_state = value

    
    @property
    def policy_change_status(self):
        """ Get policy_change_status value.

            Notes:
                None

                
                This attribute is named `policyChangeStatus` in VSD API.
                
        """
        return self._policy_change_status

    @policy_change_status.setter
    def policy_change_status(self, value):
        """ Set policy_change_status value.

            Notes:
                None

                
                This attribute is named `policyChangeStatus` in VSD API.
                
        """
        self._policy_change_status = value

    
    @property
    def use_global_mac(self):
        """ Get use_global_mac value.

            Notes:
                Enable this flag to use system configured globalMACAddress as the gateway mac address for managed l2 domains

                
                This attribute is named `useGlobalMAC` in VSD API.
                
        """
        return self._use_global_mac

    @use_global_mac.setter
    def use_global_mac(self, value):
        """ Set use_global_mac value.

            Notes:
                Enable this flag to use system configured globalMACAddress as the gateway mac address for managed l2 domains

                
                This attribute is named `useGlobalMAC` in VSD API.
                
        """
        self._use_global_mac = value

    
    @property
    def associated_multicast_channel_map_id(self):
        """ Get associated_multicast_channel_map_id value.

            Notes:
                The ID of the Multi Cast Channel Map this L2Domain / L2Domain template template is associated with. This has to be set when  enableMultiCast is set to ENABLED

                
                This attribute is named `associatedMulticastChannelMapID` in VSD API.
                
        """
        return self._associated_multicast_channel_map_id

    @associated_multicast_channel_map_id.setter
    def associated_multicast_channel_map_id(self, value):
        """ Set associated_multicast_channel_map_id value.

            Notes:
                The ID of the Multi Cast Channel Map this L2Domain / L2Domain template template is associated with. This has to be set when  enableMultiCast is set to ENABLED

                
                This attribute is named `associatedMulticastChannelMapID` in VSD API.
                
        """
        self._associated_multicast_channel_map_id = value

    
    @property
    def multicast(self):
        """ Get multicast value.

            Notes:
                Indicates multicast policy on L2Domain template.

                
        """
        return self._multicast

    @multicast.setter
    def multicast(self, value):
        """ Set multicast value.

            Notes:
                Indicates multicast policy on L2Domain template.

                
        """
        self._multicast = value

    
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

    
    @property
    def dynamic_ipv6_address(self):
        """ Get dynamic_ipv6_address value.

            Notes:
                Turn on or off dynamic allocation of IPV6 address

                
                This attribute is named `dynamicIpv6Address` in VSD API.
                
        """
        return self._dynamic_ipv6_address

    @dynamic_ipv6_address.setter
    def dynamic_ipv6_address(self, value):
        """ Set dynamic_ipv6_address value.

            Notes:
                Turn on or off dynamic allocation of IPV6 address

                
                This attribute is named `dynamicIpv6Address` in VSD API.
                
        """
        self._dynamic_ipv6_address = value

    

    
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
    