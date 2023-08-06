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




from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUEnterprisesFetcher


from .fetchers import NUMultiCastListsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUEnterpriseProfile(NURESTObject):
    """ Represents a EnterpriseProfile in the VSD

        Notes:
            Enterprise profile, used to store an enterprise's policies, quota etc.
    """

    __rest_name__ = "enterpriseprofile"
    __resource_name__ = "enterpriseprofiles"

    
    ## Constants
    
    CONST_ENCRYPTION_MANAGEMENT_MODE_MANAGED = "MANAGED"
    
    CONST_ALLOWED_FORWARDING_CLASSES_NONE = "NONE"
    
    CONST_ENCRYPTION_MANAGEMENT_MODE_DISABLED = "DISABLED"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_ALLOWED_FORWARDING_CLASSES_D = "D"
    
    CONST_ALLOWED_FORWARDING_CLASSES_E = "E"
    
    CONST_ALLOWED_FORWARDING_CLASSES_F = "F"
    
    CONST_ALLOWED_FORWARDING_CLASSES_G = "G"
    
    CONST_ALLOWED_FORWARDING_CLASSES_A = "A"
    
    CONST_ALLOWED_FORWARDING_CLASSES_B = "B"
    
    CONST_ALLOWED_FORWARDING_CLASSES_C = "C"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ALLOWED_FORWARDING_CLASSES_H = "H"
    
    

    def __init__(self, **kwargs):
        """ Initializes a EnterpriseProfile instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> enterpriseprofile = NUEnterpriseProfile(id=u'xxxx-xxx-xxx-xxx', name=u'EnterpriseProfile')
                >>> enterpriseprofile = NUEnterpriseProfile(data=my_dict)
        """

        super(NUEnterpriseProfile, self).__init__()

        # Read/Write Attributes
        
        self._bgp_enabled = None
        self._dhcp_lease_interval = None
        self._vnf_management_enabled = None
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._web_filter_enabled = None
        self._receive_multi_cast_list_id = None
        self._send_multi_cast_list_id = None
        self._description = None
        self._threat_prevention_management_enabled = None
        self._allow_advanced_qos_configuration = None
        self._allow_gateway_management = None
        self._allow_trusted_forwarding_class = None
        self._allowed_forwarding_classes = None
        self._floating_ips_quota = None
        self._embedded_metadata = None
        self._enable_application_performance_management = None
        self._encryption_management_mode = None
        self._entity_scope = None
        self._forwarding_class = None
        self._creation_date = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="bgp_enabled", remote_name="BGPEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="dhcp_lease_interval", remote_name="DHCPLeaseInterval", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="vnf_management_enabled", remote_name="VNFManagementEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="web_filter_enabled", remote_name="webFilterEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="receive_multi_cast_list_id", remote_name="receiveMultiCastListID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="send_multi_cast_list_id", remote_name="sendMultiCastListID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="threat_prevention_management_enabled", remote_name="threatPreventionManagementEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="allow_advanced_qos_configuration", remote_name="allowAdvancedQOSConfiguration", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="allow_gateway_management", remote_name="allowGatewayManagement", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="allow_trusted_forwarding_class", remote_name="allowTrustedForwardingClass", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="allowed_forwarding_classes", remote_name="allowedForwardingClasses", attribute_type=list, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name="floating_ips_quota", remote_name="floatingIPsQuota", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enable_application_performance_management", remote_name="enableApplicationPerformanceManagement", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="encryption_management_mode", remote_name="encryptionManagementMode", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'MANAGED'])
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="forwarding_class", remote_name="forwardingClass", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.enterprises = NUEnterprisesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.multi_cast_lists = NUMultiCastListsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def bgp_enabled(self):
        """ Get bgp_enabled value.

            Notes:
                Enable BGP for this enterprise profile

                
                This attribute is named `BGPEnabled` in VSD API.
                
        """
        return self._bgp_enabled

    @bgp_enabled.setter
    def bgp_enabled(self, value):
        """ Set bgp_enabled value.

            Notes:
                Enable BGP for this enterprise profile

                
                This attribute is named `BGPEnabled` in VSD API.
                
        """
        self._bgp_enabled = value

    
    @property
    def dhcp_lease_interval(self):
        """ Get dhcp_lease_interval value.

            Notes:
                DHCP Lease Interval (in hours) to be used by an enterprise.

                
                This attribute is named `DHCPLeaseInterval` in VSD API.
                
        """
        return self._dhcp_lease_interval

    @dhcp_lease_interval.setter
    def dhcp_lease_interval(self, value):
        """ Set dhcp_lease_interval value.

            Notes:
                DHCP Lease Interval (in hours) to be used by an enterprise.

                
                This attribute is named `DHCPLeaseInterval` in VSD API.
                
        """
        self._dhcp_lease_interval = value

    
    @property
    def vnf_management_enabled(self):
        """ Get vnf_management_enabled value.

            Notes:
                Enable VNF Management for this enterprise

                
                This attribute is named `VNFManagementEnabled` in VSD API.
                
        """
        return self._vnf_management_enabled

    @vnf_management_enabled.setter
    def vnf_management_enabled(self, value):
        """ Set vnf_management_enabled value.

            Notes:
                Enable VNF Management for this enterprise

                
                This attribute is named `VNFManagementEnabled` in VSD API.
                
        """
        self._vnf_management_enabled = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                The unique name of the enterprise. Valid characters are alphabets, numbers, space and hyphen( - ).

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                The unique name of the enterprise. Valid characters are alphabets, numbers, space and hyphen( - ).

                
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
    def web_filter_enabled(self):
        """ Get web_filter_enabled value.

            Notes:
                Enable Web Filtering for this enterprise profile

                
                This attribute is named `webFilterEnabled` in VSD API.
                
        """
        return self._web_filter_enabled

    @web_filter_enabled.setter
    def web_filter_enabled(self, value):
        """ Set web_filter_enabled value.

            Notes:
                Enable Web Filtering for this enterprise profile

                
                This attribute is named `webFilterEnabled` in VSD API.
                
        """
        self._web_filter_enabled = value

    
    @property
    def receive_multi_cast_list_id(self):
        """ Get receive_multi_cast_list_id value.

            Notes:
                Readonly ID of the auto generated receive multicast list associated with this enterprise profile

                
                This attribute is named `receiveMultiCastListID` in VSD API.
                
        """
        return self._receive_multi_cast_list_id

    @receive_multi_cast_list_id.setter
    def receive_multi_cast_list_id(self, value):
        """ Set receive_multi_cast_list_id value.

            Notes:
                Readonly ID of the auto generated receive multicast list associated with this enterprise profile

                
                This attribute is named `receiveMultiCastListID` in VSD API.
                
        """
        self._receive_multi_cast_list_id = value

    
    @property
    def send_multi_cast_list_id(self):
        """ Get send_multi_cast_list_id value.

            Notes:
                Readonly ID of the auto generated send multicast list associated with this enterprise profile

                
                This attribute is named `sendMultiCastListID` in VSD API.
                
        """
        return self._send_multi_cast_list_id

    @send_multi_cast_list_id.setter
    def send_multi_cast_list_id(self, value):
        """ Set send_multi_cast_list_id value.

            Notes:
                Readonly ID of the auto generated send multicast list associated with this enterprise profile

                
                This attribute is named `sendMultiCastListID` in VSD API.
                
        """
        self._send_multi_cast_list_id = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description of the enterprise/organisation profile.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the enterprise/organisation profile.

                
        """
        self._description = value

    
    @property
    def threat_prevention_management_enabled(self):
        """ Get threat_prevention_management_enabled value.

            Notes:
                Enable Threat Prevention Management for enterprise

                
                This attribute is named `threatPreventionManagementEnabled` in VSD API.
                
        """
        return self._threat_prevention_management_enabled

    @threat_prevention_management_enabled.setter
    def threat_prevention_management_enabled(self, value):
        """ Set threat_prevention_management_enabled value.

            Notes:
                Enable Threat Prevention Management for enterprise

                
                This attribute is named `threatPreventionManagementEnabled` in VSD API.
                
        """
        self._threat_prevention_management_enabled = value

    
    @property
    def allow_advanced_qos_configuration(self):
        """ Get allow_advanced_qos_configuration value.

            Notes:
                Controls whether this enterprise has access to advanced QoS settings.

                
                This attribute is named `allowAdvancedQOSConfiguration` in VSD API.
                
        """
        return self._allow_advanced_qos_configuration

    @allow_advanced_qos_configuration.setter
    def allow_advanced_qos_configuration(self, value):
        """ Set allow_advanced_qos_configuration value.

            Notes:
                Controls whether this enterprise has access to advanced QoS settings.

                
                This attribute is named `allowAdvancedQOSConfiguration` in VSD API.
                
        """
        self._allow_advanced_qos_configuration = value

    
    @property
    def allow_gateway_management(self):
        """ Get allow_gateway_management value.

            Notes:
                If set to true lets the enterprise admin create gateway templates and instances.

                
                This attribute is named `allowGatewayManagement` in VSD API.
                
        """
        return self._allow_gateway_management

    @allow_gateway_management.setter
    def allow_gateway_management(self, value):
        """ Set allow_gateway_management value.

            Notes:
                If set to true lets the enterprise admin create gateway templates and instances.

                
                This attribute is named `allowGatewayManagement` in VSD API.
                
        """
        self._allow_gateway_management = value

    
    @property
    def allow_trusted_forwarding_class(self):
        """ Get allow_trusted_forwarding_class value.

            Notes:
                Controls whether QoS policies and templates created under this enterprise set the trusted flag to true

                
                This attribute is named `allowTrustedForwardingClass` in VSD API.
                
        """
        return self._allow_trusted_forwarding_class

    @allow_trusted_forwarding_class.setter
    def allow_trusted_forwarding_class(self, value):
        """ Set allow_trusted_forwarding_class value.

            Notes:
                Controls whether QoS policies and templates created under this enterprise set the trusted flag to true

                
                This attribute is named `allowTrustedForwardingClass` in VSD API.
                
        """
        self._allow_trusted_forwarding_class = value

    
    @property
    def allowed_forwarding_classes(self):
        """ Get allowed_forwarding_classes value.

            Notes:
                Allowed Forwarding Classes for this enterprise. Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `allowedForwardingClasses` in VSD API.
                
        """
        return self._allowed_forwarding_classes

    @allowed_forwarding_classes.setter
    def allowed_forwarding_classes(self, value):
        """ Set allowed_forwarding_classes value.

            Notes:
                Allowed Forwarding Classes for this enterprise. Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `allowedForwardingClasses` in VSD API.
                
        """
        self._allowed_forwarding_classes = value

    
    @property
    def floating_ips_quota(self):
        """ Get floating_ips_quota value.

            Notes:
                Quota set for the number of floating IPs to be used by an enterprise.

                
                This attribute is named `floatingIPsQuota` in VSD API.
                
        """
        return self._floating_ips_quota

    @floating_ips_quota.setter
    def floating_ips_quota(self, value):
        """ Set floating_ips_quota value.

            Notes:
                Quota set for the number of floating IPs to be used by an enterprise.

                
                This attribute is named `floatingIPsQuota` in VSD API.
                
        """
        self._floating_ips_quota = value

    
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
    def enable_application_performance_management(self):
        """ Get enable_application_performance_management value.

            Notes:
                Enable DPI for this enterprise

                
                This attribute is named `enableApplicationPerformanceManagement` in VSD API.
                
        """
        return self._enable_application_performance_management

    @enable_application_performance_management.setter
    def enable_application_performance_management(self, value):
        """ Set enable_application_performance_management value.

            Notes:
                Enable DPI for this enterprise

                
                This attribute is named `enableApplicationPerformanceManagement` in VSD API.
                
        """
        self._enable_application_performance_management = value

    
    @property
    def encryption_management_mode(self):
        """ Get encryption_management_mode value.

            Notes:
                encryption management mode for this enterprise Possible values are DISABLED, MANAGED, .

                
                This attribute is named `encryptionManagementMode` in VSD API.
                
        """
        return self._encryption_management_mode

    @encryption_management_mode.setter
    def encryption_management_mode(self, value):
        """ Set encryption_management_mode value.

            Notes:
                encryption management mode for this enterprise Possible values are DISABLED, MANAGED, .

                
                This attribute is named `encryptionManagementMode` in VSD API.
                
        """
        self._encryption_management_mode = value

    
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
    def forwarding_class(self):
        """ Get forwarding_class value.

            Notes:
                Represents the List of forwarding classes and their load balancing capability.

                
                This attribute is named `forwardingClass` in VSD API.
                
        """
        return self._forwarding_class

    @forwarding_class.setter
    def forwarding_class(self, value):
        """ Set forwarding_class value.

            Notes:
                Represents the List of forwarding classes and their load balancing capability.

                
                This attribute is named `forwardingClass` in VSD API.
                
        """
        self._forwarding_class = value

    
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

    

    