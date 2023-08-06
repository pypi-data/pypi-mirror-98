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


from .fetchers import NUVPortsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUFloatingIp(NURESTObject):
    """ Represents a FloatingIp in the VSD

        Notes:
            Floating IP that is associated to a Domain. This floating IP could be used in the VM interface for NAT functionality.
    """

    __rest_name__ = "floatingip"
    __resource_name__ = "floatingips"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a FloatingIp instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> floatingip = NUFloatingIp(id=u'xxxx-xxx-xxx-xxx', name=u'FloatingIp')
                >>> floatingip = NUFloatingIp(data=my_dict)
        """

        super(NUFloatingIp, self).__init__()

        # Read/Write Attributes
        
        self._last_updated_by = None
        self._last_updated_date = None
        self._access_control = None
        self._address = None
        self._egress_rate_limiter_id = None
        self._embedded_metadata = None
        self._ingress_rate_limiter_id = None
        self._entity_scope = None
        self._creation_date = None
        self._assigned = None
        self._assigned_to_object_type = None
        self._associated_shared_network_resource_id = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="access_control", remote_name="accessControl", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="egress_rate_limiter_id", remote_name="egressRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ingress_rate_limiter_id", remote_name="ingressRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="assigned", remote_name="assigned", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="assigned_to_object_type", remote_name="assignedToObjectType", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_shared_network_resource_id", remote_name="associatedSharedNetworkResourceID", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.vports = NUVPortsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
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
    def access_control(self):
        """ Get access_control value.

            Notes:
                If access control is enabled this FIP is part of the Internet PG.

                
                This attribute is named `accessControl` in VSD API.
                
        """
        return self._access_control

    @access_control.setter
    def access_control(self, value):
        """ Set access_control value.

            Notes:
                If access control is enabled this FIP is part of the Internet PG.

                
                This attribute is named `accessControl` in VSD API.
                
        """
        self._access_control = value

    
    @property
    def address(self):
        """ Get address value.

            Notes:
                Floating IP address assigned to the Domain

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                Floating IP address assigned to the Domain

                
        """
        self._address = value

    
    @property
    def egress_rate_limiter_id(self):
        """ Get egress_rate_limiter_id value.

            Notes:
                ID of the Egress Rate Limiter for this FloatingIP.

                
                This attribute is named `egressRateLimiterID` in VSD API.
                
        """
        return self._egress_rate_limiter_id

    @egress_rate_limiter_id.setter
    def egress_rate_limiter_id(self, value):
        """ Set egress_rate_limiter_id value.

            Notes:
                ID of the Egress Rate Limiter for this FloatingIP.

                
                This attribute is named `egressRateLimiterID` in VSD API.
                
        """
        self._egress_rate_limiter_id = value

    
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
    def ingress_rate_limiter_id(self):
        """ Get ingress_rate_limiter_id value.

            Notes:
                ID of the Ingress Rate Limiter for this FloatingIP.

                
                This attribute is named `ingressRateLimiterID` in VSD API.
                
        """
        return self._ingress_rate_limiter_id

    @ingress_rate_limiter_id.setter
    def ingress_rate_limiter_id(self, value):
        """ Set ingress_rate_limiter_id value.

            Notes:
                ID of the Ingress Rate Limiter for this FloatingIP.

                
                This attribute is named `ingressRateLimiterID` in VSD API.
                
        """
        self._ingress_rate_limiter_id = value

    
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
    def assigned(self):
        """ Get assigned value.

            Notes:
                True if this floating IP is assigned to a network interface else the value is false

                
        """
        return self._assigned

    @assigned.setter
    def assigned(self, value):
        """ Set assigned value.

            Notes:
                True if this floating IP is assigned to a network interface else the value is false

                
        """
        self._assigned = value

    
    @property
    def assigned_to_object_type(self):
        """ Get assigned_to_object_type value.

            Notes:
                The object type to which this floating ip is assigned. Eg. vport or virtualip

                
                This attribute is named `assignedToObjectType` in VSD API.
                
        """
        return self._assigned_to_object_type

    @assigned_to_object_type.setter
    def assigned_to_object_type(self, value):
        """ Set assigned_to_object_type value.

            Notes:
                The object type to which this floating ip is assigned. Eg. vport or virtualip

                
                This attribute is named `assignedToObjectType` in VSD API.
                
        """
        self._assigned_to_object_type = value

    
    @property
    def associated_shared_network_resource_id(self):
        """ Get associated_shared_network_resource_id value.

            Notes:
                Id of the shared network resource subnet which was used to get this floating IP address

                
                This attribute is named `associatedSharedNetworkResourceID` in VSD API.
                
        """
        return self._associated_shared_network_resource_id

    @associated_shared_network_resource_id.setter
    def associated_shared_network_resource_id(self, value):
        """ Set associated_shared_network_resource_id value.

            Notes:
                Id of the shared network resource subnet which was used to get this floating IP address

                
                This attribute is named `associatedSharedNetworkResourceID` in VSD API.
                
        """
        self._associated_shared_network_resource_id = value

    
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

    

    