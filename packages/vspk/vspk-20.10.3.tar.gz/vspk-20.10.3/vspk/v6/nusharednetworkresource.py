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




from .fetchers import NUPATIPEntriesFetcher


from .fetchers import NUAddressRangesFetcher


from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUDHCPOptionsFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUEnterprisePermissionsFetcher


from .fetchers import NUVPNConnectionsFetcher


from .fetchers import NUStaticRoutesFetcher

from bambou import NURESTObject


class NUSharedNetworkResource(NURESTObject):
    """ Represents a SharedNetworkResource in the VSD

        Notes:
            This defines shared infrastructure resources that are created by user with CSPROOT role. These resources can be used by all the enterprises in the data center for various purposes. Examples of  shared resources are public subnet, floating subnet, public L2 domain.
    """

    __rest_name__ = "sharednetworkresource"
    __resource_name__ = "sharednetworkresources"

    
    ## Constants
    
    CONST_PERMITTED_ACTION_TYPE_EXTEND = "EXTEND"
    
    CONST_PERMITTED_ACTION_TYPE_ALL = "ALL"
    
    CONST_TYPE_FLOATING = "FLOATING"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_TYPE_UPLINK_SUBNET = "UPLINK_SUBNET"
    
    CONST_USE_GLOBAL_MAC_ENABLED = "ENABLED"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_USE_GLOBAL_MAC_DISABLED = "DISABLED"
    
    CONST_PERMITTED_ACTION_TYPE_USE = "USE"
    
    CONST_PERMITTED_ACTION_TYPE_READ = "READ"
    
    CONST_PERMITTED_ACTION_TYPE_DEPLOY = "DEPLOY"
    
    CONST_TYPE_L2DOMAIN = "L2DOMAIN"
    
    CONST_TYPE_PUBLIC = "PUBLIC"
    
    CONST_PERMITTED_ACTION_TYPE_INSTANTIATE = "INSTANTIATE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a SharedNetworkResource instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> sharednetworkresource = NUSharedNetworkResource(id=u'xxxx-xxx-xxx-xxx', name=u'SharedNetworkResource')
                >>> sharednetworkresource = NUSharedNetworkResource(data=my_dict)
        """

        super(NUSharedNetworkResource, self).__init__()

        # Read/Write Attributes
        
        self._ecmp_count = None
        self._dhcp_managed = None
        self._back_haul_route_distinguisher = None
        self._back_haul_route_target = None
        self._back_haul_vnid = None
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._gateway = None
        self._gateway_mac_address = None
        self._access_restriction_enabled = None
        self._address = None
        self._permitted_action_type = None
        self._description = None
        self._netmask = None
        self._shared_resource_parent_id = None
        self._embedded_metadata = None
        self._vn_id = None
        self._underlay = None
        self._enterprise_id = None
        self._entity_scope = None
        self._domain_route_distinguisher = None
        self._domain_route_target = None
        self._uplink_gw_vlan_attachment_id = None
        self._uplink_interface_ip = None
        self._uplink_interface_mac = None
        self._uplink_vport_name = None
        self._creation_date = None
        self._use_global_mac = None
        self._associated_pat_mapper_id = None
        self._subnet_route_distinguisher = None
        self._subnet_route_target = None
        self._owner = None
        self._external_id = None
        self._dynamic_pat_allocation_enabled = None
        self._type = None
        
        self.expose_attribute(local_name="ecmp_count", remote_name="ECMPCount", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="dhcp_managed", remote_name="DHCPManaged", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="back_haul_route_distinguisher", remote_name="backHaulRouteDistinguisher", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="back_haul_route_target", remote_name="backHaulRouteTarget", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="back_haul_vnid", remote_name="backHaulVNID", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="gateway", remote_name="gateway", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="gateway_mac_address", remote_name="gatewayMACAddress", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="access_restriction_enabled", remote_name="accessRestrictionEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="permitted_action_type", remote_name="permittedActionType", attribute_type=str, is_required=False, is_unique=False, choices=[u'ALL', u'DEPLOY', u'EXTEND', u'INSTANTIATE', u'READ', u'USE'])
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="netmask", remote_name="netmask", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="shared_resource_parent_id", remote_name="sharedResourceParentID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="vn_id", remote_name="vnID", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="underlay", remote_name="underlay", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enterprise_id", remote_name="enterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="domain_route_distinguisher", remote_name="domainRouteDistinguisher", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="domain_route_target", remote_name="domainRouteTarget", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="uplink_gw_vlan_attachment_id", remote_name="uplinkGWVlanAttachmentID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="uplink_interface_ip", remote_name="uplinkInterfaceIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="uplink_interface_mac", remote_name="uplinkInterfaceMAC", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="uplink_vport_name", remote_name="uplinkVPortName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="use_global_mac", remote_name="useGlobalMAC", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED'])
        self.expose_attribute(local_name="associated_pat_mapper_id", remote_name="associatedPATMapperID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="subnet_route_distinguisher", remote_name="subnetRouteDistinguisher", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="subnet_route_target", remote_name="subnetRouteTarget", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="dynamic_pat_allocation_enabled", remote_name="dynamicPATAllocationEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=True, is_unique=False, choices=[u'FLOATING', u'L2DOMAIN', u'PUBLIC', u'UPLINK_SUBNET'])
        

        # Fetchers
        
        
        self.patip_entries = NUPATIPEntriesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.address_ranges = NUAddressRangesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.dhcp_options = NUDHCPOptionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.enterprise_permissions = NUEnterprisePermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.vpn_connections = NUVPNConnectionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.static_routes = NUStaticRoutesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def ecmp_count(self):
        """ Get ecmp_count value.

            Notes:
                Domain specific Equal-cost multi-path routing count, ECMPCount = 1 means no ECMP

                
                This attribute is named `ECMPCount` in VSD API.
                
        """
        return self._ecmp_count

    @ecmp_count.setter
    def ecmp_count(self, value):
        """ Set ecmp_count value.

            Notes:
                Domain specific Equal-cost multi-path routing count, ECMPCount = 1 means no ECMP

                
                This attribute is named `ECMPCount` in VSD API.
                
        """
        self._ecmp_count = value

    
    @property
    def dhcp_managed(self):
        """ Get dhcp_managed value.

            Notes:
                true if DHCP is enabled else it is false. This value is always true for network resource of type PUBLIC or FLOATING.

                
                This attribute is named `DHCPManaged` in VSD API.
                
        """
        return self._dhcp_managed

    @dhcp_managed.setter
    def dhcp_managed(self, value):
        """ Set dhcp_managed value.

            Notes:
                true if DHCP is enabled else it is false. This value is always true for network resource of type PUBLIC or FLOATING.

                
                This attribute is named `DHCPManaged` in VSD API.
                
        """
        self._dhcp_managed = value

    
    @property
    def back_haul_route_distinguisher(self):
        """ Get back_haul_route_distinguisher value.

            Notes:
                Backhaul route distinguisher of the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `backHaulRouteDistinguisher` in VSD API.
                
        """
        return self._back_haul_route_distinguisher

    @back_haul_route_distinguisher.setter
    def back_haul_route_distinguisher(self, value):
        """ Set back_haul_route_distinguisher value.

            Notes:
                Backhaul route distinguisher of the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `backHaulRouteDistinguisher` in VSD API.
                
        """
        self._back_haul_route_distinguisher = value

    
    @property
    def back_haul_route_target(self):
        """ Get back_haul_route_target value.

            Notes:
                Backhaul route target of the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `backHaulRouteTarget` in VSD API.
                
        """
        return self._back_haul_route_target

    @back_haul_route_target.setter
    def back_haul_route_target(self, value):
        """ Set back_haul_route_target value.

            Notes:
                Backhaul route target of the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `backHaulRouteTarget` in VSD API.
                
        """
        self._back_haul_route_target = value

    
    @property
    def back_haul_vnid(self):
        """ Get back_haul_vnid value.

            Notes:
                Backhaul virtual network ID of the shared resource

                
                This attribute is named `backHaulVNID` in VSD API.
                
        """
        return self._back_haul_vnid

    @back_haul_vnid.setter
    def back_haul_vnid(self, value):
        """ Set back_haul_vnid value.

            Notes:
                Backhaul virtual network ID of the shared resource

                
                This attribute is named `backHaulVNID` in VSD API.
                
        """
        self._back_haul_vnid = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the shared resource. Valid characters are alphabets, numbers, space and hyphen( - ).

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the shared resource. Valid characters are alphabets, numbers, space and hyphen( - ).

                
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
                Gatemask configured on the shared resource

                
        """
        return self._gateway

    @gateway.setter
    def gateway(self, value):
        """ Set gateway value.

            Notes:
                Gatemask configured on the shared resource

                
        """
        self._gateway = value

    
    @property
    def gateway_mac_address(self):
        """ Get gateway_mac_address value.

            Notes:
                MAC address for a public subnet or managed l2 domain

                
                This attribute is named `gatewayMACAddress` in VSD API.
                
        """
        return self._gateway_mac_address

    @gateway_mac_address.setter
    def gateway_mac_address(self, value):
        """ Set gateway_mac_address value.

            Notes:
                MAC address for a public subnet or managed l2 domain

                
                This attribute is named `gatewayMACAddress` in VSD API.
                
        """
        self._gateway_mac_address = value

    
    @property
    def access_restriction_enabled(self):
        """ Get access_restriction_enabled value.

            Notes:
                Boolean indicates that this shared network resource is avaiable to everyone by default or not

                
                This attribute is named `accessRestrictionEnabled` in VSD API.
                
        """
        return self._access_restriction_enabled

    @access_restriction_enabled.setter
    def access_restriction_enabled(self, value):
        """ Set access_restriction_enabled value.

            Notes:
                Boolean indicates that this shared network resource is avaiable to everyone by default or not

                
                This attribute is named `accessRestrictionEnabled` in VSD API.
                
        """
        self._access_restriction_enabled = value

    
    @property
    def address(self):
        """ Get address value.

            Notes:
                Address configured on the shared resource

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                Address configured on the shared resource

                
        """
        self._address = value

    
    @property
    def permitted_action_type(self):
        """ Get permitted_action_type value.

            Notes:
                Permitted action on this shared network resource

                
                This attribute is named `permittedActionType` in VSD API.
                
        """
        return self._permitted_action_type

    @permitted_action_type.setter
    def permitted_action_type(self, value):
        """ Set permitted_action_type value.

            Notes:
                Permitted action on this shared network resource

                
                This attribute is named `permittedActionType` in VSD API.
                
        """
        self._permitted_action_type = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Description of the shared resource

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Description of the shared resource

                
        """
        self._description = value

    
    @property
    def netmask(self):
        """ Get netmask value.

            Notes:
                Netmask configured on the shared resource

                
        """
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        """ Set netmask value.

            Notes:
                Netmask configured on the shared resource

                
        """
        self._netmask = value

    
    @property
    def shared_resource_parent_id(self):
        """ Get shared_resource_parent_id value.

            Notes:
                Parent ID of the floating IP subnet to which this FIP subnet must be attached. If empty it will be created in a new domain.

                
                This attribute is named `sharedResourceParentID` in VSD API.
                
        """
        return self._shared_resource_parent_id

    @shared_resource_parent_id.setter
    def shared_resource_parent_id(self, value):
        """ Set shared_resource_parent_id value.

            Notes:
                Parent ID of the floating IP subnet to which this FIP subnet must be attached. If empty it will be created in a new domain.

                
                This attribute is named `sharedResourceParentID` in VSD API.
                
        """
        self._shared_resource_parent_id = value

    
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
    def vn_id(self):
        """ Get vn_id value.

            Notes:
                Virtual network ID of the shared resource

                
                This attribute is named `vnID` in VSD API.
                
        """
        return self._vn_id

    @vn_id.setter
    def vn_id(self, value):
        """ Set vn_id value.

            Notes:
                Virtual network ID of the shared resource

                
                This attribute is named `vnID` in VSD API.
                
        """
        self._vn_id = value

    
    @property
    def underlay(self):
        """ Get underlay value.

            Notes:
                Indicates whether this shared subnet is in underlay or not.

                
        """
        return self._underlay

    @underlay.setter
    def underlay(self, value):
        """ Set underlay value.

            Notes:
                Indicates whether this shared subnet is in underlay or not.

                
        """
        self._underlay = value

    
    @property
    def enterprise_id(self):
        """ Get enterprise_id value.

            Notes:
                Enterprise that this subnet belongs to

                
                This attribute is named `enterpriseID` in VSD API.
                
        """
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, value):
        """ Set enterprise_id value.

            Notes:
                Enterprise that this subnet belongs to

                
                This attribute is named `enterpriseID` in VSD API.
                
        """
        self._enterprise_id = value

    
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
    def domain_route_distinguisher(self):
        """ Get domain_route_distinguisher value.

            Notes:
                Route distinguisher configured on the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `domainRouteDistinguisher` in VSD API.
                
        """
        return self._domain_route_distinguisher

    @domain_route_distinguisher.setter
    def domain_route_distinguisher(self, value):
        """ Set domain_route_distinguisher value.

            Notes:
                Route distinguisher configured on the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `domainRouteDistinguisher` in VSD API.
                
        """
        self._domain_route_distinguisher = value

    
    @property
    def domain_route_target(self):
        """ Get domain_route_target value.

            Notes:
                Route target configured on the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `domainRouteTarget` in VSD API.
                
        """
        return self._domain_route_target

    @domain_route_target.setter
    def domain_route_target(self, value):
        """ Set domain_route_target value.

            Notes:
                Route target configured on the shared resource. Supported formats are: [2-byte ASN]:[4-byte value] or [4-byte ASN]:[2-byte value]

                
                This attribute is named `domainRouteTarget` in VSD API.
                
        """
        self._domain_route_target = value

    
    @property
    def uplink_gw_vlan_attachment_id(self):
        """ Get uplink_gw_vlan_attachment_id value.

            Notes:
                VLAN ID to which this vport must be attached

                
                This attribute is named `uplinkGWVlanAttachmentID` in VSD API.
                
        """
        return self._uplink_gw_vlan_attachment_id

    @uplink_gw_vlan_attachment_id.setter
    def uplink_gw_vlan_attachment_id(self, value):
        """ Set uplink_gw_vlan_attachment_id value.

            Notes:
                VLAN ID to which this vport must be attached

                
                This attribute is named `uplinkGWVlanAttachmentID` in VSD API.
                
        """
        self._uplink_gw_vlan_attachment_id = value

    
    @property
    def uplink_interface_ip(self):
        """ Get uplink_interface_ip value.

            Notes:
                IP address of the host interface

                
                This attribute is named `uplinkInterfaceIP` in VSD API.
                
        """
        return self._uplink_interface_ip

    @uplink_interface_ip.setter
    def uplink_interface_ip(self, value):
        """ Set uplink_interface_ip value.

            Notes:
                IP address of the host interface

                
                This attribute is named `uplinkInterfaceIP` in VSD API.
                
        """
        self._uplink_interface_ip = value

    
    @property
    def uplink_interface_mac(self):
        """ Get uplink_interface_mac value.

            Notes:
                MAC address of the host interface

                
                This attribute is named `uplinkInterfaceMAC` in VSD API.
                
        """
        return self._uplink_interface_mac

    @uplink_interface_mac.setter
    def uplink_interface_mac(self, value):
        """ Set uplink_interface_mac value.

            Notes:
                MAC address of the host interface

                
                This attribute is named `uplinkInterfaceMAC` in VSD API.
                
        """
        self._uplink_interface_mac = value

    
    @property
    def uplink_vport_name(self):
        """ Get uplink_vport_name value.

            Notes:
                Name of the uplink vport

                
                This attribute is named `uplinkVPortName` in VSD API.
                
        """
        return self._uplink_vport_name

    @uplink_vport_name.setter
    def uplink_vport_name(self, value):
        """ Set uplink_vport_name value.

            Notes:
                Name of the uplink vport

                
                This attribute is named `uplinkVPortName` in VSD API.
                
        """
        self._uplink_vport_name = value

    
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
    def associated_pat_mapper_id(self):
        """ Get associated_pat_mapper_id value.

            Notes:
                The ID of the PatMapper entity to which this pool is associated to.

                
                This attribute is named `associatedPATMapperID` in VSD API.
                
        """
        return self._associated_pat_mapper_id

    @associated_pat_mapper_id.setter
    def associated_pat_mapper_id(self, value):
        """ Set associated_pat_mapper_id value.

            Notes:
                The ID of the PatMapper entity to which this pool is associated to.

                
                This attribute is named `associatedPATMapperID` in VSD API.
                
        """
        self._associated_pat_mapper_id = value

    
    @property
    def subnet_route_distinguisher(self):
        """ Get subnet_route_distinguisher value.

            Notes:
                Route distinguisher configured on the shared resource subnetwork

                
                This attribute is named `subnetRouteDistinguisher` in VSD API.
                
        """
        return self._subnet_route_distinguisher

    @subnet_route_distinguisher.setter
    def subnet_route_distinguisher(self, value):
        """ Set subnet_route_distinguisher value.

            Notes:
                Route distinguisher configured on the shared resource subnetwork

                
                This attribute is named `subnetRouteDistinguisher` in VSD API.
                
        """
        self._subnet_route_distinguisher = value

    
    @property
    def subnet_route_target(self):
        """ Get subnet_route_target value.

            Notes:
                Route target configured on the shared resource subnetwork

                
                This attribute is named `subnetRouteTarget` in VSD API.
                
        """
        return self._subnet_route_target

    @subnet_route_target.setter
    def subnet_route_target(self, value):
        """ Set subnet_route_target value.

            Notes:
                Route target configured on the shared resource subnetwork

                
                This attribute is named `subnetRouteTarget` in VSD API.
                
        """
        self._subnet_route_target = value

    
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

    
    @property
    def dynamic_pat_allocation_enabled(self):
        """ Get dynamic_pat_allocation_enabled value.

            Notes:
                Indicates if PAT Mapping is enabled for the SharedNetworkResource or not

                
                This attribute is named `dynamicPATAllocationEnabled` in VSD API.
                
        """
        return self._dynamic_pat_allocation_enabled

    @dynamic_pat_allocation_enabled.setter
    def dynamic_pat_allocation_enabled(self, value):
        """ Set dynamic_pat_allocation_enabled value.

            Notes:
                Indicates if PAT Mapping is enabled for the SharedNetworkResource or not

                
                This attribute is named `dynamicPATAllocationEnabled` in VSD API.
                
        """
        self._dynamic_pat_allocation_enabled = value

    
    @property
    def type(self):
        """ Get type value.

            Notes:
                Type of the shared resource.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                Type of the shared resource.

                
        """
        self._type = value

    

    