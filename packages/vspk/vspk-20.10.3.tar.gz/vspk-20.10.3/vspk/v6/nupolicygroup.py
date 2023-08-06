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


from .fetchers import NUPolicyGroupCategoriesFetcher


from .fetchers import NUVPortsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUPolicyGroup(NURESTObject):
    """ Represents a PolicyGroup in the VSD

        Notes:
            Policy groups are collections of VPorts that are used as building blocks for security policies encompassing multiple end-points. One or more vports can be added to a policy group using this interface.
    """

    __rest_name__ = "policygroup"
    __resource_name__ = "policygroups"

    
    ## Constants
    
    CONST_TYPE_HARDWARE = "HARDWARE"
    
    CONST_ENTITY_STATE_UNDER_CONSTRUCTION = "UNDER_CONSTRUCTION"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_ENTITY_STATE_MARKED_FOR_DELETION = "MARKED_FOR_DELETION"
    
    CONST_TYPE_SOFTWARE = "SOFTWARE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a PolicyGroup instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> policygroup = NUPolicyGroup(id=u'xxxx-xxx-xxx-xxx', name=u'PolicyGroup')
                >>> policygroup = NUPolicyGroup(data=my_dict)
        """

        super(NUPolicyGroup, self).__init__()

        # Read/Write Attributes
        
        self._evpn_community_tag = None
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._template_id = None
        self._description = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._entity_state = None
        self._policy_group_id = None
        self._creation_date = None
        self._assoc_policy_group_category_id = None
        self._assoc_policy_group_category_name = None
        self._owner = None
        self._external = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="evpn_community_tag", remote_name="EVPNCommunityTag", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="template_id", remote_name="templateID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="entity_state", remote_name="entityState", attribute_type=str, is_required=False, is_unique=False, choices=[u'MARKED_FOR_DELETION', u'UNDER_CONSTRUCTION'])
        self.expose_attribute(local_name="policy_group_id", remote_name="policyGroupID", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="assoc_policy_group_category_id", remote_name="assocPolicyGroupCategoryID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="assoc_policy_group_category_name", remote_name="assocPolicyGroupCategoryName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external", remote_name="external", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=True, is_unique=False, choices=[u'HARDWARE', u'SOFTWARE'])
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.policy_group_categories = NUPolicyGroupCategoriesFetcher.fetcher_with_object(parent_object=self, relationship="member")
        
        
        self.vports = NUVPortsFetcher.fetcher_with_object(parent_object=self, relationship="member")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def evpn_community_tag(self):
        """ Get evpn_community_tag value.

            Notes:
                Assigned by VSD. An extended community or other similar BGP attribute to the specific EVPN / IP-VPN NLRI where the VM or network macro is being advertised.

                
                This attribute is named `EVPNCommunityTag` in VSD API.
                
        """
        return self._evpn_community_tag

    @evpn_community_tag.setter
    def evpn_community_tag(self, value):
        """ Set evpn_community_tag value.

            Notes:
                Assigned by VSD. An extended community or other similar BGP attribute to the specific EVPN / IP-VPN NLRI where the VM or network macro is being advertised.

                
                This attribute is named `EVPNCommunityTag` in VSD API.
                
        """
        self._evpn_community_tag = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the policy group

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the policy group

                
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
    def template_id(self):
        """ Get template_id value.

            Notes:
                Determines which template ID this policy group belongs to.

                
                This attribute is named `templateID` in VSD API.
                
        """
        return self._template_id

    @template_id.setter
    def template_id(self, value):
        """ Set template_id value.

            Notes:
                Determines which template ID this policy group belongs to.

                
                This attribute is named `templateID` in VSD API.
                
        """
        self._template_id = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Describes this policy group

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Describes this policy group

                
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
    def entity_state(self):
        """ Get entity_state value.

            Notes:
                Intermediate State of L2 Domain.

                
                This attribute is named `entityState` in VSD API.
                
        """
        return self._entity_state

    @entity_state.setter
    def entity_state(self, value):
        """ Set entity_state value.

            Notes:
                Intermediate State of L2 Domain.

                
                This attribute is named `entityState` in VSD API.
                
        """
        self._entity_state = value

    
    @property
    def policy_group_id(self):
        """ Get policy_group_id value.

            Notes:
                PG ID for the subnet. This is unique per domain and will be in the range 1-4095

                
                This attribute is named `policyGroupID` in VSD API.
                
        """
        return self._policy_group_id

    @policy_group_id.setter
    def policy_group_id(self, value):
        """ Set policy_group_id value.

            Notes:
                PG ID for the subnet. This is unique per domain and will be in the range 1-4095

                
                This attribute is named `policyGroupID` in VSD API.
                
        """
        self._policy_group_id = value

    
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
    def assoc_policy_group_category_id(self):
        """ Get assoc_policy_group_category_id value.

            Notes:
                UUID of the associated Policy Group Category for contextual filtering of policy groups.

                
                This attribute is named `assocPolicyGroupCategoryID` in VSD API.
                
        """
        return self._assoc_policy_group_category_id

    @assoc_policy_group_category_id.setter
    def assoc_policy_group_category_id(self, value):
        """ Set assoc_policy_group_category_id value.

            Notes:
                UUID of the associated Policy Group Category for contextual filtering of policy groups.

                
                This attribute is named `assocPolicyGroupCategoryID` in VSD API.
                
        """
        self._assoc_policy_group_category_id = value

    
    @property
    def assoc_policy_group_category_name(self):
        """ Get assoc_policy_group_category_name value.

            Notes:
                Name of the Policy Group Category used for contextual filtering of policy groups.

                
                This attribute is named `assocPolicyGroupCategoryName` in VSD API.
                
        """
        return self._assoc_policy_group_category_name

    @assoc_policy_group_category_name.setter
    def assoc_policy_group_category_name(self, value):
        """ Set assoc_policy_group_category_name value.

            Notes:
                Name of the Policy Group Category used for contextual filtering of policy groups.

                
                This attribute is named `assocPolicyGroupCategoryName` in VSD API.
                
        """
        self._assoc_policy_group_category_name = value

    
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
    def external(self):
        """ Get external value.

            Notes:
                Indicates whether this PG is internal to VSP or not.

                
        """
        return self._external

    @external.setter
    def external(self, value):
        """ Set external value.

            Notes:
                Indicates whether this PG is internal to VSP or not.

                
        """
        self._external = value

    
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
                Type of policy group.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                Type of policy group.

                
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
    