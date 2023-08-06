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


from .fetchers import NUConnectionendpointsFetcher


from .fetchers import NUNSGatewayTemplatesFetcher


from .fetchers import NUSSHKeysFetcher

from bambou import NURESTObject


class NUInfrastructureAccessProfile(NURESTObject):
    """ Represents a InfrastructureAccessProfile in the VSD

        Notes:
            Infrastructure Access Profiles identify a set of NSG template level platform attributes specifically related to user and access control, inherited by gateways as they are instantiated.
    """

    __rest_name__ = "infrastructureaccessprofile"
    __resource_name__ = "infrastructureaccessprofiles"

    
    ## Constants
    
    CONST_SSH_AUTH_MODE_KEY_BASED = "KEY_BASED"
    
    CONST_SSH_AUTH_MODE_PASSWORD_AND_KEY_BASED = "PASSWORD_AND_KEY_BASED"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_SOURCE_IP_FILTER_ENABLED = "ENABLED"
    
    CONST_SOURCE_IP_FILTER_DISABLED = "DISABLED"
    
    CONST_SSH_AUTH_MODE_PASSWORD_BASED = "PASSWORD_BASED"
    
    

    def __init__(self, **kwargs):
        """ Initializes a InfrastructureAccessProfile instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> infrastructureaccessprofile = NUInfrastructureAccessProfile(id=u'xxxx-xxx-xxx-xxx', name=u'InfrastructureAccessProfile')
                >>> infrastructureaccessprofile = NUInfrastructureAccessProfile(data=my_dict)
        """

        super(NUInfrastructureAccessProfile, self).__init__()

        # Read/Write Attributes
        
        self._ssh_auth_mode = None
        self._name = None
        self._password = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._description = None
        self._embedded_metadata = None
        self._enterprise_id = None
        self._entity_scope = None
        self._source_ip_filter = None
        self._creation_date = None
        self._user_name = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="ssh_auth_mode", remote_name="SSHAuthMode", attribute_type=str, is_required=False, is_unique=False, choices=[u'KEY_BASED', u'PASSWORD_AND_KEY_BASED', u'PASSWORD_BASED'])
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=True)
        self.expose_attribute(local_name="password", remote_name="password", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enterprise_id", remote_name="enterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="source_ip_filter", remote_name="sourceIPFilter", attribute_type=str, is_required=False, is_unique=False, choices=[u'DISABLED', u'ENABLED'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="user_name", remote_name="userName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.connectionendpoints = NUConnectionendpointsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ns_gateway_templates = NUNSGatewayTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.ssh_keys = NUSSHKeysFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def ssh_auth_mode(self):
        """ Get ssh_auth_mode value.

            Notes:
                Indicates the authentication method used during an SSH session.

                
                This attribute is named `SSHAuthMode` in VSD API.
                
        """
        return self._ssh_auth_mode

    @ssh_auth_mode.setter
    def ssh_auth_mode(self, value):
        """ Set ssh_auth_mode value.

            Notes:
                Indicates the authentication method used during an SSH session.

                
                This attribute is named `SSHAuthMode` in VSD API.
                
        """
        self._ssh_auth_mode = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the Infrastructure Access Profile

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the Infrastructure Access Profile

                
        """
        self._name = value

    
    @property
    def password(self):
        """ Get password value.

            Notes:
                Password of the default user associated to the access profile.

                
        """
        return self._password

    @password.setter
    def password(self, value):
        """ Set password value.

            Notes:
                Password of the default user associated to the access profile.

                
        """
        self._password = value

    
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
    def description(self):
        """ Get description value.

            Notes:
                A description of the Profile instance created.

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the Profile instance created.

                
        """
        self._description = value

    
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
    def enterprise_id(self):
        """ Get enterprise_id value.

            Notes:
                Enterprise/Organisation associated with this Profile instance.

                
                This attribute is named `enterpriseID` in VSD API.
                
        """
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, value):
        """ Set enterprise_id value.

            Notes:
                Enterprise/Organisation associated with this Profile instance.

                
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
    def source_ip_filter(self):
        """ Get source_ip_filter value.

            Notes:
                Indicates if source based IP filtering is enabled for this access profile.

                
                This attribute is named `sourceIPFilter` in VSD API.
                
        """
        return self._source_ip_filter

    @source_ip_filter.setter
    def source_ip_filter(self, value):
        """ Set source_ip_filter value.

            Notes:
                Indicates if source based IP filtering is enabled for this access profile.

                
                This attribute is named `sourceIPFilter` in VSD API.
                
        """
        self._source_ip_filter = value

    
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
    def user_name(self):
        """ Get user_name value.

            Notes:
                Default user name which is associated to the access profile.

                
                This attribute is named `userName` in VSD API.
                
        """
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        """ Set user_name value.

            Notes:
                Default user name which is associated to the access profile.

                
                This attribute is named `userName` in VSD API.
                
        """
        self._user_name = value

    
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

    

    