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




from .fetchers import NUPerformanceMonitorsFetcher


from .fetchers import NUPermissionsFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUAlarmsFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUJobsFetcher


from .fetchers import NUSubnetsFetcher

from bambou import NURESTObject


class NUIKEGatewayConnection(NURESTObject):
    """ Represents a IKEGatewayConnection in the VSD

        Notes:
            Set the attributes like NSG role, authentication method etc for establishing IKE security association with remote gateway.
    """

    __rest_name__ = "ikegatewayconnection"
    __resource_name__ = "ikegatewayconnections"

    
    ## Constants
    
    CONST_CONFIGURATION_STATUS_IN_PROGRESS = "IN_PROGRESS"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_ASSOCIATED_CLOUD_TYPE_AZURECLOUD = "AZURECLOUD"
    
    CONST_NSG_IDENTIFIER_TYPE_ID_IPV4_ADDR = "ID_IPV4_ADDR"
    
    CONST_NSG_ROLE_RESPONDER = "RESPONDER"
    
    CONST_CONFIGURATION_STATUS_WAITING_FOR_RESOURCES = "WAITING_FOR_RESOURCES"
    
    CONST_NSG_IDENTIFIER_TYPE_ID_KEY_ID = "ID_KEY_ID"
    
    CONST_CONFIGURATION_STATUS_SUCCESS = "SUCCESS"
    
    CONST_NSG_IDENTIFIER_TYPE_ID_FQDN = "ID_FQDN"
    
    CONST_NSG_IDENTIFIER_TYPE_ID_RFC822_ADDR = "ID_RFC822_ADDR"
    
    CONST_CONFIGURATION_STATUS_UNKNOWN = "UNKNOWN"
    
    CONST_ASSOCIATED_IKE_AUTHENTICATION_TYPE_IKE_CERTIFICATE = "IKE_CERTIFICATE"
    
    CONST_CONFIGURATION_STATUS_CANCELLED = "CANCELLED"
    
    CONST_CONFIGURATION_STATUS_WAITING = "WAITING"
    
    CONST_ASSOCIATED_IKE_AUTHENTICATION_TYPE_IKE_PSK = "IKE_PSK"
    
    CONST_NSG_ROLE_INITIATOR = "INITIATOR"
    
    CONST_CONFIGURATION_STATUS_NOT_APPLICABLE = "NOT_APPLICABLE"
    
    CONST_CONFIGURATION_STATUS_SYNCED_FROM_CLOUD = "SYNCED_FROM_CLOUD"
    
    CONST_NSG_IDENTIFIER_TYPE_ID_DER_ASN1_DN = "ID_DER_ASN1_DN"
    
    CONST_CONFIGURATION_STATUS_PAUSING = "PAUSING"
    
    CONST_CONFIGURATION_STATUS_FAILED = "FAILED"
    
    CONST_CONFIGURATION_STATUS_CLOUD_CONFIGURATION_REMOVED = "CLOUD_CONFIGURATION_REMOVED"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_CONFIGURATION_STATUS_CANCELING = "CANCELING"
    
    

    def __init__(self, **kwargs):
        """ Initializes a IKEGatewayConnection instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> ikegatewayconnection = NUIKEGatewayConnection(id=u'xxxx-xxx-xxx-xxx', name=u'IKEGatewayConnection')
                >>> ikegatewayconnection = NUIKEGatewayConnection(data=my_dict)
        """

        super(NUIKEGatewayConnection, self).__init__()

        # Read/Write Attributes
        
        self._nsg_identifier = None
        self._nsg_identifier_type = None
        self._nsg_role = None
        self._name = None
        self._mark = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._sequence = None
        self._mirrored_connection = None
        self._allow_any_subnet = None
        self._embedded_metadata = None
        self._unencrypted_psk = None
        self._entity_scope = None
        self._configuration_status = None
        self._port_vlan_name = None
        self._creation_date = None
        self._priority = None
        self._associated_cloud_id = None
        self._associated_cloud_type = None
        self._associated_ike_authentication_id = None
        self._associated_ike_authentication_type = None
        self._associated_ike_encryption_profile_id = None
        self._associated_ike_gateway_profile_id = None
        self._associated_vlanid = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="nsg_identifier", remote_name="NSGIdentifier", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="nsg_identifier_type", remote_name="NSGIdentifierType", attribute_type=str, is_required=False, is_unique=False, choices=[u'ID_DER_ASN1_DN', u'ID_FQDN', u'ID_IPV4_ADDR', u'ID_KEY_ID', u'ID_RFC822_ADDR'])
        self.expose_attribute(local_name="nsg_role", remote_name="NSGRole", attribute_type=str, is_required=False, is_unique=False, choices=[u'INITIATOR', u'RESPONDER'])
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="mark", remote_name="mark", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="sequence", remote_name="sequence", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="mirrored_connection", remote_name="mirroredConnection", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="allow_any_subnet", remote_name="allowAnySubnet", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="unencrypted_psk", remote_name="unencryptedPSK", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="configuration_status", remote_name="configurationStatus", attribute_type=str, is_required=False, is_unique=False, choices=[u'CANCELING', u'CANCELLED', u'CLOUD_CONFIGURATION_REMOVED', u'FAILED', u'IN_PROGRESS', u'NOT_APPLICABLE', u'PAUSING', u'SUCCESS', u'SYNCED_FROM_CLOUD', u'UNKNOWN', u'WAITING', u'WAITING_FOR_RESOURCES'])
        self.expose_attribute(local_name="port_vlan_name", remote_name="portVLANName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="priority", remote_name="priority", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_cloud_id", remote_name="associatedCloudID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_cloud_type", remote_name="associatedCloudType", attribute_type=str, is_required=False, is_unique=False, choices=[u'AZURECLOUD'])
        self.expose_attribute(local_name="associated_ike_authentication_id", remote_name="associatedIKEAuthenticationID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ike_authentication_type", remote_name="associatedIKEAuthenticationType", attribute_type=str, is_required=False, is_unique=False, choices=[u'IKE_CERTIFICATE', u'IKE_PSK'])
        self.expose_attribute(local_name="associated_ike_encryption_profile_id", remote_name="associatedIKEEncryptionProfileID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_ike_gateway_profile_id", remote_name="associatedIKEGatewayProfileID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_vlanid", remote_name="associatedVLANID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.performance_monitors = NUPerformanceMonitorsFetcher.fetcher_with_object(parent_object=self, relationship="member")
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.alarms = NUAlarmsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.jobs = NUJobsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.subnets = NUSubnetsFetcher.fetcher_with_object(parent_object=self, relationship="member")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def nsg_identifier(self):
        """ Get nsg_identifier value.

            Notes:
                NSG Identifier. Null to take on the default 'uuid'

                
                This attribute is named `NSGIdentifier` in VSD API.
                
        """
        return self._nsg_identifier

    @nsg_identifier.setter
    def nsg_identifier(self, value):
        """ Set nsg_identifier value.

            Notes:
                NSG Identifier. Null to take on the default 'uuid'

                
                This attribute is named `NSGIdentifier` in VSD API.
                
        """
        self._nsg_identifier = value

    
    @property
    def nsg_identifier_type(self):
        """ Get nsg_identifier_type value.

            Notes:
                NSG Identifier Type. 

                
                This attribute is named `NSGIdentifierType` in VSD API.
                
        """
        return self._nsg_identifier_type

    @nsg_identifier_type.setter
    def nsg_identifier_type(self, value):
        """ Set nsg_identifier_type value.

            Notes:
                NSG Identifier Type. 

                
                This attribute is named `NSGIdentifierType` in VSD API.
                
        """
        self._nsg_identifier_type = value

    
    @property
    def nsg_role(self):
        """ Get nsg_role value.

            Notes:
                NSG role

                
                This attribute is named `NSGRole` in VSD API.
                
        """
        return self._nsg_role

    @nsg_role.setter
    def nsg_role(self, value):
        """ Set nsg_role value.

            Notes:
                NSG role

                
                This attribute is named `NSGRole` in VSD API.
                
        """
        self._nsg_role = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Optional Name of the connection

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Optional Name of the connection

                
        """
        self._name = value

    
    @property
    def mark(self):
        """ Get mark value.

            Notes:
                skbMark, used by vrs for the ike monitor feature

                
        """
        return self._mark

    @mark.setter
    def mark(self, value):
        """ Set mark value.

            Notes:
                skbMark, used by vrs for the ike monitor feature

                
        """
        self._mark = value

    
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
    def sequence(self):
        """ Get sequence value.

            Notes:
                The sequence of the IKE Gateway Connection

                
        """
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        """ Set sequence value.

            Notes:
                The sequence of the IKE Gateway Connection

                
        """
        self._sequence = value

    
    @property
    def mirrored_connection(self):
        """ Get mirrored_connection value.

            Notes:
                Indicates if the IKEGatewayConnection is mirroring an equivalent one on Shunt VLAN or not.

                
                This attribute is named `mirroredConnection` in VSD API.
                
        """
        return self._mirrored_connection

    @mirrored_connection.setter
    def mirrored_connection(self, value):
        """ Set mirrored_connection value.

            Notes:
                Indicates if the IKEGatewayConnection is mirroring an equivalent one on Shunt VLAN or not.

                
                This attribute is named `mirroredConnection` in VSD API.
                
        """
        self._mirrored_connection = value

    
    @property
    def allow_any_subnet(self):
        """ Get allow_any_subnet value.

            Notes:
                Allow any local subnets to be used

                
                This attribute is named `allowAnySubnet` in VSD API.
                
        """
        return self._allow_any_subnet

    @allow_any_subnet.setter
    def allow_any_subnet(self, value):
        """ Set allow_any_subnet value.

            Notes:
                Allow any local subnets to be used

                
                This attribute is named `allowAnySubnet` in VSD API.
                
        """
        self._allow_any_subnet = value

    
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
    def unencrypted_psk(self):
        """ Get unencrypted_psk value.

            Notes:
                Unencrypted PSK

                
                This attribute is named `unencryptedPSK` in VSD API.
                
        """
        return self._unencrypted_psk

    @unencrypted_psk.setter
    def unencrypted_psk(self, value):
        """ Set unencrypted_psk value.

            Notes:
                Unencrypted PSK

                
                This attribute is named `unencryptedPSK` in VSD API.
                
        """
        self._unencrypted_psk = value

    
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
    def configuration_status(self):
        """ Get configuration_status value.

            Notes:
                Status of configuration on third-party cloud instance

                
                This attribute is named `configurationStatus` in VSD API.
                
        """
        return self._configuration_status

    @configuration_status.setter
    def configuration_status(self, value):
        """ Set configuration_status value.

            Notes:
                Status of configuration on third-party cloud instance

                
                This attribute is named `configurationStatus` in VSD API.
                
        """
        self._configuration_status = value

    
    @property
    def port_vlan_name(self):
        """ Get port_vlan_name value.

            Notes:
                The Name of the Port and Vlan the IKEv2 Connection is on

                
                This attribute is named `portVLANName` in VSD API.
                
        """
        return self._port_vlan_name

    @port_vlan_name.setter
    def port_vlan_name(self, value):
        """ Set port_vlan_name value.

            Notes:
                The Name of the Port and Vlan the IKEv2 Connection is on

                
                This attribute is named `portVLANName` in VSD API.
                
        """
        self._port_vlan_name = value

    
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
    def priority(self):
        """ Get priority value.

            Notes:
                Priority of the IKEv2 Gateway Connection

                
        """
        return self._priority

    @priority.setter
    def priority(self, value):
        """ Set priority value.

            Notes:
                Priority of the IKEv2 Gateway Connection

                
        """
        self._priority = value

    
    @property
    def associated_cloud_id(self):
        """ Get associated_cloud_id value.

            Notes:
                ID of the associated third-party cloud instance

                
                This attribute is named `associatedCloudID` in VSD API.
                
        """
        return self._associated_cloud_id

    @associated_cloud_id.setter
    def associated_cloud_id(self, value):
        """ Set associated_cloud_id value.

            Notes:
                ID of the associated third-party cloud instance

                
                This attribute is named `associatedCloudID` in VSD API.
                
        """
        self._associated_cloud_id = value

    
    @property
    def associated_cloud_type(self):
        """ Get associated_cloud_type value.

            Notes:
                Type of associated third-party cloud instance, ex. AZURECLOUD

                
                This attribute is named `associatedCloudType` in VSD API.
                
        """
        return self._associated_cloud_type

    @associated_cloud_type.setter
    def associated_cloud_type(self, value):
        """ Set associated_cloud_type value.

            Notes:
                Type of associated third-party cloud instance, ex. AZURECLOUD

                
                This attribute is named `associatedCloudType` in VSD API.
                
        """
        self._associated_cloud_type = value

    
    @property
    def associated_ike_authentication_id(self):
        """ Get associated_ike_authentication_id value.

            Notes:
                Associated Authentication ID

                
                This attribute is named `associatedIKEAuthenticationID` in VSD API.
                
        """
        return self._associated_ike_authentication_id

    @associated_ike_authentication_id.setter
    def associated_ike_authentication_id(self, value):
        """ Set associated_ike_authentication_id value.

            Notes:
                Associated Authentication ID

                
                This attribute is named `associatedIKEAuthenticationID` in VSD API.
                
        """
        self._associated_ike_authentication_id = value

    
    @property
    def associated_ike_authentication_type(self):
        """ Get associated_ike_authentication_type value.

            Notes:
                Associated Authentication Type

                
                This attribute is named `associatedIKEAuthenticationType` in VSD API.
                
        """
        return self._associated_ike_authentication_type

    @associated_ike_authentication_type.setter
    def associated_ike_authentication_type(self, value):
        """ Set associated_ike_authentication_type value.

            Notes:
                Associated Authentication Type

                
                This attribute is named `associatedIKEAuthenticationType` in VSD API.
                
        """
        self._associated_ike_authentication_type = value

    
    @property
    def associated_ike_encryption_profile_id(self):
        """ Get associated_ike_encryption_profile_id value.

            Notes:
                The ID of the associated IKEEncryptionProfile

                
                This attribute is named `associatedIKEEncryptionProfileID` in VSD API.
                
        """
        return self._associated_ike_encryption_profile_id

    @associated_ike_encryption_profile_id.setter
    def associated_ike_encryption_profile_id(self, value):
        """ Set associated_ike_encryption_profile_id value.

            Notes:
                The ID of the associated IKEEncryptionProfile

                
                This attribute is named `associatedIKEEncryptionProfileID` in VSD API.
                
        """
        self._associated_ike_encryption_profile_id = value

    
    @property
    def associated_ike_gateway_profile_id(self):
        """ Get associated_ike_gateway_profile_id value.

            Notes:
                The ID of the associated IKEGatewayProfile

                
                This attribute is named `associatedIKEGatewayProfileID` in VSD API.
                
        """
        return self._associated_ike_gateway_profile_id

    @associated_ike_gateway_profile_id.setter
    def associated_ike_gateway_profile_id(self, value):
        """ Set associated_ike_gateway_profile_id value.

            Notes:
                The ID of the associated IKEGatewayProfile

                
                This attribute is named `associatedIKEGatewayProfileID` in VSD API.
                
        """
        self._associated_ike_gateway_profile_id = value

    
    @property
    def associated_vlanid(self):
        """ Get associated_vlanid value.

            Notes:
                The ID of the associated Vlan

                
                This attribute is named `associatedVLANID` in VSD API.
                
        """
        return self._associated_vlanid

    @associated_vlanid.setter
    def associated_vlanid(self, value):
        """ Set associated_vlanid value.

            Notes:
                The ID of the associated Vlan

                
                This attribute is named `associatedVLANID` in VSD API.
                
        """
        self._associated_vlanid = value

    
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

    

    