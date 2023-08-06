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

from bambou import NURESTObject


class NUDemarcationService(NURESTObject):
    """ Represents a DemarcationService in the VSD

        Notes:
            Demarcation services provide the interconnection between the datacenter networks and the Wide Area Network.
    """

    __rest_name__ = "demarcationservice"
    __resource_name__ = "demarcationservices"

    
    ## Constants
    
    CONST_TYPE_GATEWAY = "GATEWAY"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_TYPE_BR_PORT = "BR_PORT"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a DemarcationService instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> demarcationservice = NUDemarcationService(id=u'xxxx-xxx-xxx-xxx', name=u'DemarcationService')
                >>> demarcationservice = NUDemarcationService(data=my_dict)
        """

        super(NUDemarcationService, self).__init__()

        # Read/Write Attributes
        
        self._last_updated_by = None
        self._last_updated_date = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._route_distinguisher = None
        self._creation_date = None
        self._priority = None
        self._associated_gateway_id = None
        self._associated_vlanid = None
        self._owner = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="route_distinguisher", remote_name="routeDistinguisher", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="priority", remote_name="priority", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_gateway_id", remote_name="associatedGatewayID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_vlanid", remote_name="associatedVLANID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=False, is_unique=False, choices=[u'BR_PORT', u'GATEWAY'])
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

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
    def route_distinguisher(self):
        """ Get route_distinguisher value.

            Notes:
                The route distinguisher associated with the next hop. This is a read only property automatically created by VSD.

                
                This attribute is named `routeDistinguisher` in VSD API.
                
        """
        return self._route_distinguisher

    @route_distinguisher.setter
    def route_distinguisher(self, value):
        """ Set route_distinguisher value.

            Notes:
                The route distinguisher associated with the next hop. This is a read only property automatically created by VSD.

                
                This attribute is named `routeDistinguisher` in VSD API.
                
        """
        self._route_distinguisher = value

    
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
                Next hop priority assigned by the user.

                
        """
        return self._priority

    @priority.setter
    def priority(self, value):
        """ Set priority value.

            Notes:
                Next hop priority assigned by the user.

                
        """
        self._priority = value

    
    @property
    def associated_gateway_id(self):
        """ Get associated_gateway_id value.

            Notes:
                The ID of the NSGBR Gateway used as next hop in the untrusted domain.

                
                This attribute is named `associatedGatewayID` in VSD API.
                
        """
        return self._associated_gateway_id

    @associated_gateway_id.setter
    def associated_gateway_id(self, value):
        """ Set associated_gateway_id value.

            Notes:
                The ID of the NSGBR Gateway used as next hop in the untrusted domain.

                
                This attribute is named `associatedGatewayID` in VSD API.
                
        """
        self._associated_gateway_id = value

    
    @property
    def associated_vlanid(self):
        """ Get associated_vlanid value.

            Notes:
                The VLAN ID of the BR VLAN used as next hop in the trusted domain.

                
                This attribute is named `associatedVLANID` in VSD API.
                
        """
        return self._associated_vlanid

    @associated_vlanid.setter
    def associated_vlanid(self, value):
        """ Set associated_vlanid value.

            Notes:
                The VLAN ID of the BR VLAN used as next hop in the trusted domain.

                
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

    
    @property
    def type(self):
        """ Get type value.

            Notes:
                The type of next hop determines linking direction for a demarcation service, possible values: BR_PORT, GATEWAY 

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                The type of next hop determines linking direction for a demarcation service, possible values: BR_PORT, GATEWAY 

                
        """
        self._type = value

    

    