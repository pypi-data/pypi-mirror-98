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




from .fetchers import NUPATNATPoolsFetcher


from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUBGPNeighborsFetcher


from .fetchers import NUIKEGatewayConnectionsFetcher


from .fetchers import NUAlarmsFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUEnterprisePermissionsFetcher


from .fetchers import NUUplinkConnectionsFetcher


from .fetchers import NUBRConnectionsFetcher


from .fetchers import NUStatisticsFetcher


from .fetchers import NULtestatisticsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUVLAN(NURESTObject):
    """ Represents a VLAN in the VSD

        Notes:
            VLANs are Virtual Local Area Networks. They allow to differentiate several traffic flows inside a single Port. A VLAN with a value set to 0 can be used to tell the system to not use any tagging.
    """

    __rest_name__ = "vlan"
    __resource_name__ = "vlans"

    
    ## Constants
    
    CONST_PERMITTED_ACTION_USE = "USE"
    
    CONST_ASSOCIATED_CONNECTION_TYPE_UPLINK_CONNECTION = "UPLINK_CONNECTION"
    
    CONST_PERMITTED_ACTION_READ = "READ"
    
    CONST_STATUS_ORPHAN = "ORPHAN"
    
    CONST_PERMITTED_ACTION_ALL = "ALL"
    
    CONST_PERMITTED_ACTION_DEPLOY = "DEPLOY"
    
    CONST_PERMITTED_ACTION_EXTEND = "EXTEND"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_PERMITTED_ACTION_INSTANTIATE = "INSTANTIATE"
    
    CONST_STATUS_INITIALIZED = "INITIALIZED"
    
    CONST_TYPE_DUC = "DUC"
    
    CONST_STATUS_MISMATCH = "MISMATCH"
    
    CONST_STATUS_READY = "READY"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_TYPE_ACCESS = "ACCESS"
    
    CONST_ASSOCIATED_CONNECTION_TYPE_BR_CONNECTION = "BR_CONNECTION"
    
    CONST_TYPE_BR = "BR"
    
    CONST_TYPE_UPLINK = "UPLINK"
    
    

    def __init__(self, **kwargs):
        """ Initializes a VLAN instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> vlan = NUVLAN(id=u'xxxx-xxx-xxx-xxx', name=u'VLAN')
                >>> vlan = NUVLAN(data=my_dict)
        """

        super(NUVLAN, self).__init__()

        # Read/Write Attributes
        
        self._value = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._gateway_id = None
        self._readonly = None
        self._template_id = None
        self._permitted_action = None
        self._description = None
        self._restricted = None
        self._shunt_vlan = None
        self._embedded_metadata = None
        self._enable_nat_probes = None
        self._inherited_port_properties_diverged = None
        self._entity_scope = None
        self._vport_id = None
        self._traffic_through_ubr_only = None
        self._creation_date = None
        self._is_uplink = None
        self._use_user_mnemonic = None
        self._user_mnemonic = None
        self._associated_bgp_profile_id = None
        self._associated_connection_type = None
        self._associated_egress_qos_policy_id = None
        self._associated_ingress_overlay_qo_s_policer_id = None
        self._associated_ingress_qos_policy_id = None
        self._associated_ingress_underlay_qo_s_policer_id = None
        self._associated_uplink_connection_id = None
        self._associated_vsc_profile_id = None
        self._status = None
        self._mtu = None
        self._duc_vlan = None
        self._owner = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="value", remote_name="value", attribute_type=int, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="gateway_id", remote_name="gatewayID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="readonly", remote_name="readonly", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="template_id", remote_name="templateID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="permitted_action", remote_name="permittedAction", attribute_type=str, is_required=False, is_unique=False, choices=[u'ALL', u'DEPLOY', u'EXTEND', u'INSTANTIATE', u'READ', u'USE'])
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="restricted", remote_name="restricted", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="shunt_vlan", remote_name="shuntVLAN", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enable_nat_probes", remote_name="enableNATProbes", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="inherited_port_properties_diverged", remote_name="inheritedPortPropertiesDiverged", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="vport_id", remote_name="vportID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="traffic_through_ubr_only", remote_name="TrafficThroughUBROnly", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="is_uplink", remote_name="isUplink", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="use_user_mnemonic", remote_name="useUserMnemonic", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="user_mnemonic", remote_name="userMnemonic", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_bgp_profile_id", remote_name="associatedBGPProfileID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_connection_type", remote_name="associatedConnectionType", attribute_type=str, is_required=False, is_unique=False, choices=[u'BR_CONNECTION', u'UPLINK_CONNECTION'])
        self.expose_attribute(local_name="associated_egress_qos_policy_id", remote_name="associatedEgressQOSPolicyID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ingress_overlay_qo_s_policer_id", remote_name="associatedIngressOverlayQoSPolicerID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ingress_qos_policy_id", remote_name="associatedIngressQOSPolicyID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ingress_underlay_qo_s_policer_id", remote_name="associatedIngressUnderlayQoSPolicerID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_uplink_connection_id", remote_name="associatedUplinkConnectionID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_vsc_profile_id", remote_name="associatedVSCProfileID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="status", remote_name="status", attribute_type=str, is_required=False, is_unique=False, choices=[u'INITIALIZED', u'MISMATCH', u'ORPHAN', u'READY'])
        self.expose_attribute(local_name="mtu", remote_name="mtu", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="duc_vlan", remote_name="ducVlan", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=False, is_unique=False, choices=[u'ACCESS', u'BR', u'DUC', u'UPLINK'])
        

        # Fetchers
        
        
        self.patnat_pools = NUPATNATPoolsFetcher.fetcher_with_object(parent_object=self, relationship="member")
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.bgp_neighbors = NUBGPNeighborsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ike_gateway_connections = NUIKEGatewayConnectionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.alarms = NUAlarmsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.enterprise_permissions = NUEnterprisePermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.uplink_connections = NUUplinkConnectionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.br_connections = NUBRConnectionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.statistics = NUStatisticsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ltestatistics = NULtestatisticsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def value(self):
        """ Get value value.

            Notes:
                value of VLAN

                
        """
        return self._value

    @value.setter
    def value(self, value):
        """ Set value value.

            Notes:
                value of VLAN

                
        """
        self._value = value

    
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
    def gateway_id(self):
        """ Get gateway_id value.

            Notes:
                The Gateway associated with this  VLAN. This is a read only attribute

                
                This attribute is named `gatewayID` in VSD API.
                
        """
        return self._gateway_id

    @gateway_id.setter
    def gateway_id(self, value):
        """ Set gateway_id value.

            Notes:
                The Gateway associated with this  VLAN. This is a read only attribute

                
                This attribute is named `gatewayID` in VSD API.
                
        """
        self._gateway_id = value

    
    @property
    def readonly(self):
        """ Get readonly value.

            Notes:
                Determines whether this entity is read only.  Read only objects cannot be modified or deleted.

                
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        """ Set readonly value.

            Notes:
                Determines whether this entity is read only.  Read only objects cannot be modified or deleted.

                
        """
        self._readonly = value

    
    @property
    def template_id(self):
        """ Get template_id value.

            Notes:
                The ID of the template that this Port was created from

                
                This attribute is named `templateID` in VSD API.
                
        """
        return self._template_id

    @template_id.setter
    def template_id(self, value):
        """ Set template_id value.

            Notes:
                The ID of the template that this Port was created from

                
                This attribute is named `templateID` in VSD API.
                
        """
        self._template_id = value

    
    @property
    def permitted_action(self):
        """ Get permitted_action value.

            Notes:
                The permitted  action to USE/EXTEND  this Gateway.

                
                This attribute is named `permittedAction` in VSD API.
                
        """
        return self._permitted_action

    @permitted_action.setter
    def permitted_action(self, value):
        """ Set permitted_action value.

            Notes:
                The permitted  action to USE/EXTEND  this Gateway.

                
                This attribute is named `permittedAction` in VSD API.
                
        """
        self._permitted_action = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description of the VLAN instance.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the VLAN instance.

                
        """
        self._description = value

    
    @property
    def restricted(self):
        """ Get restricted value.

            Notes:
                Determines whether this entity can be used in associations with other properties.

                
        """
        return self._restricted

    @restricted.setter
    def restricted(self, value):
        """ Set restricted value.

            Notes:
                Determines whether this entity can be used in associations with other properties.

                
        """
        self._restricted = value

    
    @property
    def shunt_vlan(self):
        """ Get shunt_vlan value.

            Notes:
                A flag to mark this instance of a VLAN as a candidate to be a termination point of a Shunt Link.  Only VLANs residing on a Network Port can have this attribute set to true.

                
                This attribute is named `shuntVLAN` in VSD API.
                
        """
        return self._shunt_vlan

    @shunt_vlan.setter
    def shunt_vlan(self, value):
        """ Set shunt_vlan value.

            Notes:
                A flag to mark this instance of a VLAN as a candidate to be a termination point of a Shunt Link.  Only VLANs residing on a Network Port can have this attribute set to true.

                
                This attribute is named `shuntVLAN` in VSD API.
                
        """
        self._shunt_vlan = value

    
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
    def enable_nat_probes(self):
        """ Get enable_nat_probes value.

            Notes:
                If enabled, probes will be sent to other NSGs and DTLS sessions for IPSEC and VXLAN will be set up to the VSCs. If disabled, no NAT probes are sent on that uplink and no DTLS sessions are set up to the VSCs.

                
                This attribute is named `enableNATProbes` in VSD API.
                
        """
        return self._enable_nat_probes

    @enable_nat_probes.setter
    def enable_nat_probes(self, value):
        """ Set enable_nat_probes value.

            Notes:
                If enabled, probes will be sent to other NSGs and DTLS sessions for IPSEC and VXLAN will be set up to the VSCs. If disabled, no NAT probes are sent on that uplink and no DTLS sessions are set up to the VSCs.

                
                This attribute is named `enableNATProbes` in VSD API.
                
        """
        self._enable_nat_probes = value

    
    @property
    def inherited_port_properties_diverged(self):
        """ Get inherited_port_properties_diverged value.

            Notes:
                Indicates if the value of any of the properties - MTU, NAT Probes Enabled or Traffic Through DUC Only Enabled, on this instance is different from the values of these properties at NSPort. True if they were different at any point. False if no attempt was made to change them from the values at NSPort.

                
                This attribute is named `inheritedPortPropertiesDiverged` in VSD API.
                
        """
        return self._inherited_port_properties_diverged

    @inherited_port_properties_diverged.setter
    def inherited_port_properties_diverged(self, value):
        """ Set inherited_port_properties_diverged value.

            Notes:
                Indicates if the value of any of the properties - MTU, NAT Probes Enabled or Traffic Through DUC Only Enabled, on this instance is different from the values of these properties at NSPort. True if they were different at any point. False if no attempt was made to change them from the values at NSPort.

                
                This attribute is named `inheritedPortPropertiesDiverged` in VSD API.
                
        """
        self._inherited_port_properties_diverged = value

    
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
    def vport_id(self):
        """ Get vport_id value.

            Notes:
                The Vport associated with this VLAN. This is a read only attribute

                
                This attribute is named `vportID` in VSD API.
                
        """
        return self._vport_id

    @vport_id.setter
    def vport_id(self, value):
        """ Set vport_id value.

            Notes:
                The Vport associated with this VLAN. This is a read only attribute

                
                This attribute is named `vportID` in VSD API.
                
        """
        self._vport_id = value

    
    @property
    def traffic_through_ubr_only(self):
        """ Get traffic_through_ubr_only value.

            Notes:
                If enabled, cuts down the number of probes to just the number of provisioned DUCs.

                
                This attribute is named `TrafficThroughUBROnly` in VSD API.
                
        """
        return self._traffic_through_ubr_only

    @traffic_through_ubr_only.setter
    def traffic_through_ubr_only(self, value):
        """ Set traffic_through_ubr_only value.

            Notes:
                If enabled, cuts down the number of probes to just the number of provisioned DUCs.

                
                This attribute is named `TrafficThroughUBROnly` in VSD API.
                
        """
        self._traffic_through_ubr_only = value

    
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
    def is_uplink(self):
        """ Get is_uplink value.

            Notes:
                Indicates if the VLAN is used as an uplink.

                
                This attribute is named `isUplink` in VSD API.
                
        """
        return self._is_uplink

    @is_uplink.setter
    def is_uplink(self, value):
        """ Set is_uplink value.

            Notes:
                Indicates if the VLAN is used as an uplink.

                
                This attribute is named `isUplink` in VSD API.
                
        """
        self._is_uplink = value

    
    @property
    def use_user_mnemonic(self):
        """ Get use_user_mnemonic value.

            Notes:
                Determines whether to use the defined mnemonic for this VLAN instance.

                
                This attribute is named `useUserMnemonic` in VSD API.
                
        """
        return self._use_user_mnemonic

    @use_user_mnemonic.setter
    def use_user_mnemonic(self, value):
        """ Set use_user_mnemonic value.

            Notes:
                Determines whether to use the defined mnemonic for this VLAN instance.

                
                This attribute is named `useUserMnemonic` in VSD API.
                
        """
        self._use_user_mnemonic = value

    
    @property
    def user_mnemonic(self):
        """ Get user_mnemonic value.

            Notes:
                User mnemonic of the VLAN instance.

                
                This attribute is named `userMnemonic` in VSD API.
                
        """
        return self._user_mnemonic

    @user_mnemonic.setter
    def user_mnemonic(self, value):
        """ Set user_mnemonic value.

            Notes:
                User mnemonic of the VLAN instance.

                
                This attribute is named `userMnemonic` in VSD API.
                
        """
        self._user_mnemonic = value

    
    @property
    def associated_bgp_profile_id(self):
        """ Get associated_bgp_profile_id value.

            Notes:
                The ID of the associated BGP profile

                
                This attribute is named `associatedBGPProfileID` in VSD API.
                
        """
        return self._associated_bgp_profile_id

    @associated_bgp_profile_id.setter
    def associated_bgp_profile_id(self, value):
        """ Set associated_bgp_profile_id value.

            Notes:
                The ID of the associated BGP profile

                
                This attribute is named `associatedBGPProfileID` in VSD API.
                
        """
        self._associated_bgp_profile_id = value

    
    @property
    def associated_connection_type(self):
        """ Get associated_connection_type value.

            Notes:
                Specifies the type of Connection (uplink, BR) associated to this VLAN instance.

                
                This attribute is named `associatedConnectionType` in VSD API.
                
        """
        return self._associated_connection_type

    @associated_connection_type.setter
    def associated_connection_type(self, value):
        """ Set associated_connection_type value.

            Notes:
                Specifies the type of Connection (uplink, BR) associated to this VLAN instance.

                
                This attribute is named `associatedConnectionType` in VSD API.
                
        """
        self._associated_connection_type = value

    
    @property
    def associated_egress_qos_policy_id(self):
        """ Get associated_egress_qos_policy_id value.

            Notes:
                ID of the Egress QOS Policy associated with this VLAN.

                
                This attribute is named `associatedEgressQOSPolicyID` in VSD API.
                
        """
        return self._associated_egress_qos_policy_id

    @associated_egress_qos_policy_id.setter
    def associated_egress_qos_policy_id(self, value):
        """ Set associated_egress_qos_policy_id value.

            Notes:
                ID of the Egress QOS Policy associated with this VLAN.

                
                This attribute is named `associatedEgressQOSPolicyID` in VSD API.
                
        """
        self._associated_egress_qos_policy_id = value

    
    @property
    def associated_ingress_overlay_qo_s_policer_id(self):
        """ Get associated_ingress_overlay_qo_s_policer_id value.

            Notes:
                ID of the Ingress Overlay QoS Policer associated with this VLAN.

                
                This attribute is named `associatedIngressOverlayQoSPolicerID` in VSD API.
                
        """
        return self._associated_ingress_overlay_qo_s_policer_id

    @associated_ingress_overlay_qo_s_policer_id.setter
    def associated_ingress_overlay_qo_s_policer_id(self, value):
        """ Set associated_ingress_overlay_qo_s_policer_id value.

            Notes:
                ID of the Ingress Overlay QoS Policer associated with this VLAN.

                
                This attribute is named `associatedIngressOverlayQoSPolicerID` in VSD API.
                
        """
        self._associated_ingress_overlay_qo_s_policer_id = value

    
    @property
    def associated_ingress_qos_policy_id(self):
        """ Get associated_ingress_qos_policy_id value.

            Notes:
                ID of the Ingress QoS Policy / Tunnel Shaper associated with this VLAN.

                
                This attribute is named `associatedIngressQOSPolicyID` in VSD API.
                
        """
        return self._associated_ingress_qos_policy_id

    @associated_ingress_qos_policy_id.setter
    def associated_ingress_qos_policy_id(self, value):
        """ Set associated_ingress_qos_policy_id value.

            Notes:
                ID of the Ingress QoS Policy / Tunnel Shaper associated with this VLAN.

                
                This attribute is named `associatedIngressQOSPolicyID` in VSD API.
                
        """
        self._associated_ingress_qos_policy_id = value

    
    @property
    def associated_ingress_underlay_qo_s_policer_id(self):
        """ Get associated_ingress_underlay_qo_s_policer_id value.

            Notes:
                ID of the Ingress Underlay QoS Policer associated with this VLAN.

                
                This attribute is named `associatedIngressUnderlayQoSPolicerID` in VSD API.
                
        """
        return self._associated_ingress_underlay_qo_s_policer_id

    @associated_ingress_underlay_qo_s_policer_id.setter
    def associated_ingress_underlay_qo_s_policer_id(self, value):
        """ Set associated_ingress_underlay_qo_s_policer_id value.

            Notes:
                ID of the Ingress Underlay QoS Policer associated with this VLAN.

                
                This attribute is named `associatedIngressUnderlayQoSPolicerID` in VSD API.
                
        """
        self._associated_ingress_underlay_qo_s_policer_id = value

    
    @property
    def associated_uplink_connection_id(self):
        """ Get associated_uplink_connection_id value.

            Notes:
                Associated uplink connection ID

                
                This attribute is named `associatedUplinkConnectionID` in VSD API.
                
        """
        return self._associated_uplink_connection_id

    @associated_uplink_connection_id.setter
    def associated_uplink_connection_id(self, value):
        """ Set associated_uplink_connection_id value.

            Notes:
                Associated uplink connection ID

                
                This attribute is named `associatedUplinkConnectionID` in VSD API.
                
        """
        self._associated_uplink_connection_id = value

    
    @property
    def associated_vsc_profile_id(self):
        """ Get associated_vsc_profile_id value.

            Notes:
                The associated VSC profile for the uplink VLANS. This should be only be valid for the uplinks

                
                This attribute is named `associatedVSCProfileID` in VSD API.
                
        """
        return self._associated_vsc_profile_id

    @associated_vsc_profile_id.setter
    def associated_vsc_profile_id(self, value):
        """ Set associated_vsc_profile_id value.

            Notes:
                The associated VSC profile for the uplink VLANS. This should be only be valid for the uplinks

                
                This attribute is named `associatedVSCProfileID` in VSD API.
                
        """
        self._associated_vsc_profile_id = value

    
    @property
    def status(self):
        """ Get status value.

            Notes:
                Status of the VLAN.

                
        """
        return self._status

    @status.setter
    def status(self, value):
        """ Set status value.

            Notes:
                Status of the VLAN.

                
        """
        self._status = value

    
    @property
    def mtu(self):
        """ Get mtu value.

            Notes:
                Port MTU (Maximum Transmission Unit) :  The size in octets of the largest protocol data unit (PDU) that the layer can pass on.  The default value is normally 1500 octets for Ethernet v2 and can go up to 9198 for Jumbo Frames.

                
        """
        return self._mtu

    @mtu.setter
    def mtu(self, value):
        """ Set mtu value.

            Notes:
                Port MTU (Maximum Transmission Unit) :  The size in octets of the largest protocol data unit (PDU) that the layer can pass on.  The default value is normally 1500 octets for Ethernet v2 and can go up to 9198 for Jumbo Frames.

                
        """
        self._mtu = value

    
    @property
    def duc_vlan(self):
        """ Get duc_vlan value.

            Notes:
                When set to true, this specifies that this VLAN instance serves as an underlay connection endpoint on an NSG-UBR gateway.

                
                This attribute is named `ducVlan` in VSD API.
                
        """
        return self._duc_vlan

    @duc_vlan.setter
    def duc_vlan(self, value):
        """ Set duc_vlan value.

            Notes:
                When set to true, this specifies that this VLAN instance serves as an underlay connection endpoint on an NSG-UBR gateway.

                
                This attribute is named `ducVlan` in VSD API.
                
        """
        self._duc_vlan = value

    
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
    def type(self):
        """ Get type value.

            Notes:
                This type marks a VLAN for its utility.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                This type marks a VLAN for its utility.

                
        """
        self._type = value

    

    
    ## Custom methods
    def is_template(self):
        """ Verify that the object is a template
    
            Returns:
                (bool): True if the object is a template
        """
        return False
    
    def is_from_template(self):
        """ Verify if the object has been instantiated from a template
    
            Note:
                The object has to be fetched. Otherwise, it does not
                have information from its parent
    
            Returns:
                (bool): True if the object is a template
        """
        return self.template_id
    