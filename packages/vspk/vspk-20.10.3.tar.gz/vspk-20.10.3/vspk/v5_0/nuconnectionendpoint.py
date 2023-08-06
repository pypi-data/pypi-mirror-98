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




from .fetchers import NUMetadatasFetcher


from .fetchers import NUGlobalMetadatasFetcher

from bambou import NURESTObject


class NUConnectionendpoint(NURESTObject):
    """ Represents a Connectionendpoint in the VSD

        Notes:
            SSH (Secure Shell) is used to provide secure remote console access to NSGs deployed in branch locations. For additional security, you may restrict SSH access from specific host(s) by providing a list of source IP addresses.
    """

    __rest_name__ = "connectionendpoint"
    __resource_name__ = "connectionendpoints"

    
    ## Constants
    
    CONST_IP_TYPE_IPV6 = "IPV6"
    
    CONST_IP_TYPE_IPV4 = "IPV4"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_END_POINT_TYPE_SOURCE = "SOURCE"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a Connectionendpoint instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> connectionendpoint = NUConnectionendpoint(id=u'xxxx-xxx-xxx-xxx', name=u'Connectionendpoint')
                >>> connectionendpoint = NUConnectionendpoint(data=my_dict)
        """

        super(NUConnectionendpoint, self).__init__()

        # Read/Write Attributes
        
        self._ip_address = None
        self._ip_type = None
        self._ipv6_address = None
        self._name = None
        self._last_updated_by = None
        self._description = None
        self._end_point_type = None
        self._entity_scope = None
        self._external_id = None
        
        self.expose_attribute(local_name="ip_address", remote_name="IPAddress", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ip_type", remote_name="IPType", attribute_type=str, is_required=False, is_unique=False, choices=[u'IPV4', u'IPV6'])
        self.expose_attribute(local_name="ipv6_address", remote_name="IPv6Address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="end_point_type", remote_name="endPointType", attribute_type=str, is_required=False, is_unique=False, choices=[u'SOURCE'])
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def ip_address(self):
        """ Get ip_address value.

            Notes:
                IP Address of the end point.

                
                This attribute is named `IPAddress` in VSD API.
                
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value):
        """ Set ip_address value.

            Notes:
                IP Address of the end point.

                
                This attribute is named `IPAddress` in VSD API.
                
        """
        self._ip_address = value

    
    @property
    def ip_type(self):
        """ Get ip_type value.

            Notes:
                IPv4 or IPv6.

                
                This attribute is named `IPType` in VSD API.
                
        """
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value):
        """ Set ip_type value.

            Notes:
                IPv4 or IPv6.

                
                This attribute is named `IPType` in VSD API.
                
        """
        self._ip_type = value

    
    @property
    def ipv6_address(self):
        """ Get ipv6_address value.

            Notes:
                IPv6 address of the end point.

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        return self._ipv6_address

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ Set ipv6_address value.

            Notes:
                IPv6 address of the end point.

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        self._ipv6_address = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the connection endpoint.

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the connection endpoint.

                
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
    def description(self):
        """ Get description value.

            Notes:
                A description of the connection endpoint.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the connection endpoint.

                
        """
        self._description = value

    
    @property
    def end_point_type(self):
        """ Get end_point_type value.

            Notes:
                Indicates if this endpoint is the source/destination of a network connection.

                
                This attribute is named `endPointType` in VSD API.
                
        """
        return self._end_point_type

    @end_point_type.setter
    def end_point_type(self, value):
        """ Set end_point_type value.

            Notes:
                Indicates if this endpoint is the source/destination of a network connection.

                
                This attribute is named `endPointType` in VSD API.
                
        """
        self._end_point_type = value

    
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

    

    