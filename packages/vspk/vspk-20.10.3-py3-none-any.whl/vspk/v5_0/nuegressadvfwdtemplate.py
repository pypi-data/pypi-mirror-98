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


from .fetchers import NUEgressAdvFwdEntryTemplatesFetcher


from .fetchers import NUGlobalMetadatasFetcher

from bambou import NURESTObject


class NUEgressAdvFwdTemplate(NURESTObject):
    """ Represents a EgressAdvFwdTemplate in the VSD

        Notes:
            Create a table for egress forwarding policy rules. These include flow redirect rules and forwarding class override rules.
    """

    __rest_name__ = "egressadvfwdtemplate"
    __resource_name__ = "egressadvfwdtemplates"

    
    ## Constants
    
    CONST_POLICY_STATE_DRAFT = "DRAFT"
    
    CONST_POLICY_STATE_LIVE = "LIVE"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_PRIORITY_TYPE_NONE = "NONE"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_PRIORITY_TYPE_TOP = "TOP"
    
    CONST_PRIORITY_TYPE_BOTTOM = "BOTTOM"
    
    

    def __init__(self, **kwargs):
        """ Initializes a EgressAdvFwdTemplate instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> egressadvfwdtemplate = NUEgressAdvFwdTemplate(id=u'xxxx-xxx-xxx-xxx', name=u'EgressAdvFwdTemplate')
                >>> egressadvfwdtemplate = NUEgressAdvFwdTemplate(data=my_dict)
        """

        super(NUEgressAdvFwdTemplate, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._last_updated_by = None
        self._active = None
        self._default_allow_ip = None
        self._default_allow_non_ip = None
        self._description = None
        self._entity_scope = None
        self._policy_state = None
        self._priority = None
        self._priority_type = None
        self._associated_live_entity_id = None
        self._auto_generate_priority = None
        self._external_id = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="active", remote_name="active", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="default_allow_ip", remote_name="defaultAllowIP", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="default_allow_non_ip", remote_name="defaultAllowNonIP", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="policy_state", remote_name="policyState", attribute_type=str, is_required=False, is_unique=False, choices=[u'DRAFT', u'LIVE'])
        self.expose_attribute(local_name="priority", remote_name="priority", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="priority_type", remote_name="priorityType", attribute_type=str, is_required=False, is_unique=False, choices=[u'BOTTOM', u'NONE', u'TOP'])
        self.expose_attribute(local_name="associated_live_entity_id", remote_name="associatedLiveEntityID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="auto_generate_priority", remote_name="autoGeneratePriority", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.egress_adv_fwd_entry_templates = NUEgressAdvFwdEntryTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def name(self):
        """ Get name value.

            Notes:
                The name of the template

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                The name of the template

                
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
    def active(self):
        """ Get active value.

            Notes:
                If enabled, it means that this ACL or QOS entry is active

                
        """
        return self._active

    @active.setter
    def active(self, value):
        """ Set active value.

            Notes:
                If enabled, it means that this ACL or QOS entry is active

                
        """
        self._active = value

    
    @property
    def default_allow_ip(self):
        """ Get default_allow_ip value.

            Notes:
                If enabled a default ACL of Allow All is added as the last entry in the list of ACL entries

                
                This attribute is named `defaultAllowIP` in VSD API.
                
        """
        return self._default_allow_ip

    @default_allow_ip.setter
    def default_allow_ip(self, value):
        """ Set default_allow_ip value.

            Notes:
                If enabled a default ACL of Allow All is added as the last entry in the list of ACL entries

                
                This attribute is named `defaultAllowIP` in VSD API.
                
        """
        self._default_allow_ip = value

    
    @property
    def default_allow_non_ip(self):
        """ Get default_allow_non_ip value.

            Notes:
                If enabled, non ip traffic will be dropped

                
                This attribute is named `defaultAllowNonIP` in VSD API.
                
        """
        return self._default_allow_non_ip

    @default_allow_non_ip.setter
    def default_allow_non_ip(self, value):
        """ Set default_allow_non_ip value.

            Notes:
                If enabled, non ip traffic will be dropped

                
                This attribute is named `defaultAllowNonIP` in VSD API.
                
        """
        self._default_allow_non_ip = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description of the entity

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the entity

                
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
    def policy_state(self):
        """ Get policy_state value.

            Notes:
                State of the policy.  Possible values are DRAFT, LIVE, .

                
                This attribute is named `policyState` in VSD API.
                
        """
        return self._policy_state

    @policy_state.setter
    def policy_state(self, value):
        """ Set policy_state value.

            Notes:
                State of the policy.  Possible values are DRAFT, LIVE, .

                
                This attribute is named `policyState` in VSD API.
                
        """
        self._policy_state = value

    
    @property
    def priority(self):
        """ Get priority value.

            Notes:
                The priority of the ACL entry that determines the order of entries

                
        """
        return self._priority

    @priority.setter
    def priority(self, value):
        """ Set priority value.

            Notes:
                The priority of the ACL entry that determines the order of entries

                
        """
        self._priority = value

    
    @property
    def priority_type(self):
        """ Get priority_type value.

            Notes:
                Possible values: TOP, BOTTOM or NONE. TOP and BOTTOM ACL policies can only be defined and managed on the template level, NONE can be used on both the template and instantiated level. These allow for careful control of ACL priority handling.

                
                This attribute is named `priorityType` in VSD API.
                
        """
        return self._priority_type

    @priority_type.setter
    def priority_type(self, value):
        """ Set priority_type value.

            Notes:
                Possible values: TOP, BOTTOM or NONE. TOP and BOTTOM ACL policies can only be defined and managed on the template level, NONE can be used on both the template and instantiated level. These allow for careful control of ACL priority handling.

                
                This attribute is named `priorityType` in VSD API.
                
        """
        self._priority_type = value

    
    @property
    def associated_live_entity_id(self):
        """ Get associated_live_entity_id value.

            Notes:
                In the draft mode, the ACL entry refers to this LiveEntity. In non-drafted mode, this is null.

                
                This attribute is named `associatedLiveEntityID` in VSD API.
                
        """
        return self._associated_live_entity_id

    @associated_live_entity_id.setter
    def associated_live_entity_id(self, value):
        """ Set associated_live_entity_id value.

            Notes:
                In the draft mode, the ACL entry refers to this LiveEntity. In non-drafted mode, this is null.

                
                This attribute is named `associatedLiveEntityID` in VSD API.
                
        """
        self._associated_live_entity_id = value

    
    @property
    def auto_generate_priority(self):
        """ Get auto_generate_priority value.

            Notes:
                This option affects how ACL entry priorities are generated when not specified. If 'false', the priority is generated by incrementing the current highest priority by 100. If 'true', a random priority will be generated, which is advised when creating many entries concurrently without specifying the priority. This will cause the ACL entry to be randomly placed in the existing list of ACL entries. Therefore it is advised to only enable this when allow rules are being created.

                
                This attribute is named `autoGeneratePriority` in VSD API.
                
        """
        return self._auto_generate_priority

    @auto_generate_priority.setter
    def auto_generate_priority(self, value):
        """ Set auto_generate_priority value.

            Notes:
                This option affects how ACL entry priorities are generated when not specified. If 'false', the priority is generated by incrementing the current highest priority by 100. If 'true', a random priority will be generated, which is advised when creating many entries concurrently without specifying the priority. This will cause the ACL entry to be randomly placed in the existing list of ACL entries. Therefore it is advised to only enable this when allow rules are being created.

                
                This attribute is named `autoGeneratePriority` in VSD API.
                
        """
        self._auto_generate_priority = value

    
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

    

    