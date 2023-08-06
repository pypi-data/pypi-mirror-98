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


class NURoleentry(NURESTObject):
    """ Represents a Roleentry in the VSD

        Notes:
            Entry for each end point with assoicatiated permissions.
    """

    __rest_name__ = "roleentry"
    __resource_name__ = "roleentries"

    
    ## Constants
    
    CONST_ROLE_ACCESS_TYPE_LIST_NO_ACCESS = "NO_ACCESS"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ROLE_ACCESS_TYPE_LIST_CUD_CHILDREN = "CUD_CHILDREN"
    
    CONST_ROLE_ACCESS_TYPE_LIST_NO_ACCESS_CHILDREN = "NO_ACCESS_CHILDREN"
    
    CONST_ROLE_ACCESS_TYPE_LIST_DELETE = "DELETE"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_ROLE_ACCESS_TYPE_LIST_CREATE = "CREATE"
    
    CONST_ROLE_ACCESS_TYPE_LIST_READ_CHILDREN = "READ_CHILDREN"
    
    CONST_ROLE_ACCESS_TYPE_LIST_MODIFY = "MODIFY"
    
    CONST_ROLE_ACCESS_TYPE_LIST_READ = "READ"
    
    

    def __init__(self, **kwargs):
        """ Initializes a Roleentry instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> roleentry = NURoleentry(id=u'xxxx-xxx-xxx-xxx', name=u'Roleentry')
                >>> roleentry = NURoleentry(data=my_dict)
        """

        super(NURoleentry, self).__init__()

        # Read/Write Attributes
        
        self._embedded_metadata = None
        self._end_point_type = None
        self._entity_scope = None
        self._role_access_type_list = None
        self._external_id = None
        
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="end_point_type", remote_name="endPointType", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="role_access_type_list", remote_name="roleAccessTypeList", attribute_type=list, is_required=True, is_unique=False, choices=[u'CREATE', u'CUD_CHILDREN', u'DELETE', u'MODIFY', u'NO_ACCESS', u'NO_ACCESS_CHILDREN', u'READ', u'READ_CHILDREN'])
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
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
    def end_point_type(self):
        """ Get end_point_type value.

            Notes:
                Managed Object Type or end point

                
                This attribute is named `endPointType` in VSD API.
                
        """
        return self._end_point_type

    @end_point_type.setter
    def end_point_type(self, value):
        """ Set end_point_type value.

            Notes:
                Managed Object Type or end point

                
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
    def role_access_type_list(self):
        """ Get role_access_type_list value.

            Notes:
                List of Access like READ, READ_CHILDREN, CREATE, MODIFY, DELETE, CUD_CHILDREN, NO_ACCESS, NO_ACCESS_CHILDREN

                
                This attribute is named `roleAccessTypeList` in VSD API.
                
        """
        return self._role_access_type_list

    @role_access_type_list.setter
    def role_access_type_list(self, value):
        """ Set role_access_type_list value.

            Notes:
                List of Access like READ, READ_CHILDREN, CREATE, MODIFY, DELETE, CUD_CHILDREN, NO_ACCESS, NO_ACCESS_CHILDREN

                
                This attribute is named `roleAccessTypeList` in VSD API.
                
        """
        self._role_access_type_list = value

    
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

    

    