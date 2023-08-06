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


class NUVSDComponent(NURESTObject):
    """ Represents a VSDComponent in the VSD

        Notes:
            System Monitoring details for components of VSD system.
    """

    __rest_name__ = "component"
    __resource_name__ = "components"

    
    ## Constants
    
    CONST_STATUS_DOWN = "DOWN"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_TYPE_JBOSS = "JBOSS"
    
    CONST_TYPE_EJABBERD = "EJABBERD"
    
    CONST_STATUS_UP = "UP"
    
    CONST_TYPE_MEDIATOR = "MEDIATOR"
    
    CONST_TYPE_TCA = "TCA"
    
    CONST_STATUS_ADMIN_DOWN = "ADMIN_DOWN"
    
    CONST_TYPE_STATSSERVER = "STATSSERVER"
    
    CONST_TYPE_STATSCOLLECTOR = "STATSCOLLECTOR"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_TYPE_PERCONA = "PERCONA"
    
    

    def __init__(self, **kwargs):
        """ Initializes a VSDComponent instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> vsdcomponent = NUVSDComponent(id=u'xxxx-xxx-xxx-xxx', name=u'VSDComponent')
                >>> vsdcomponent = NUVSDComponent(data=my_dict)
        """

        super(NUVSDComponent, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._management_ip = None
        self._address = None
        self._description = None
        self._entity_scope = None
        self._location = None
        self._product_version = None
        self._status = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="management_ip", remote_name="managementIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="location", remote_name="location", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="product_version", remote_name="productVersion", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="status", remote_name="status", attribute_type=str, is_required=False, is_unique=False, choices=[u'ADMIN_DOWN', u'DOWN', u'UP'])
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=False, is_unique=False, choices=[u'EJABBERD', u'JBOSS', u'MEDIATOR', u'PERCONA', u'STATSCOLLECTOR', u'STATSSERVER', u'TCA'])
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Identifies the entity with a name.

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Identifies the entity with a name.

                
        """
        self._name = value

    
    @property
    def management_ip(self):
        """ Get management_ip value.

            Notes:
                An optional management IP to log into this component.

                
                This attribute is named `managementIP` in VSD API.
                
        """
        return self._management_ip

    @management_ip.setter
    def management_ip(self, value):
        """ Set management_ip value.

            Notes:
                An optional management IP to log into this component.

                
                This attribute is named `managementIP` in VSD API.
                
        """
        self._management_ip = value

    
    @property
    def address(self):
        """ Get address value.

            Notes:
                An optional IP to access this component.

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                An optional IP to access this component.

                
        """
        self._address = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Description of the entity.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Description of the entity.

                
        """
        self._description = value

    
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
    def location(self):
        """ Get location value.

            Notes:
                Identifies the entity to be associated with a location.

                
        """
        return self._location

    @location.setter
    def location(self, value):
        """ Set location value.

            Notes:
                Identifies the entity to be associated with a location.

                
        """
        self._location = value

    
    @property
    def product_version(self):
        """ Get product_version value.

            Notes:
                Product version supported by this entity.

                
                This attribute is named `productVersion` in VSD API.
                
        """
        return self._product_version

    @product_version.setter
    def product_version(self, value):
        """ Set product_version value.

            Notes:
                Product version supported by this entity.

                
                This attribute is named `productVersion` in VSD API.
                
        """
        self._product_version = value

    
    @property
    def status(self):
        """ Get status value.

            Notes:
                Current status of the entity. Possible values are UP, DOWN, ADMIN_DOWN, .

                
        """
        return self._status

    @status.setter
    def status(self, value):
        """ Set status value.

            Notes:
                Current status of the entity. Possible values are UP, DOWN, ADMIN_DOWN, .

                
        """
        self._status = value

    
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
                Type of the component.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                Type of the component.

                
        """
        self._type = value

    

    