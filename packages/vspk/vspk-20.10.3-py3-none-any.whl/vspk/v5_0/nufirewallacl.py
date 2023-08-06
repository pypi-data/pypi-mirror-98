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


from .fetchers import NUFirewallRulesFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUDomainsFetcher

from bambou import NURESTObject


class NUFirewallAcl(NURESTObject):
    """ Represents a FirewallAcl in the VSD

        Notes:
            None
    """

    __rest_name__ = "firewallacl"
    __resource_name__ = "firewallacls"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a FirewallAcl instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> firewallacl = NUFirewallAcl(id=u'xxxx-xxx-xxx-xxx', name=u'FirewallAcl')
                >>> firewallacl = NUFirewallAcl(data=my_dict)
        """

        super(NUFirewallAcl, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._last_updated_by = None
        self._active = None
        self._default_allow_ip = None
        self._default_allow_non_ip = None
        self._description = None
        self._entity_scope = None
        self._rule_ids = None
        self._auto_generate_priority = None
        self._external_id = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="active", remote_name="active", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="default_allow_ip", remote_name="defaultAllowIP", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="default_allow_non_ip", remote_name="defaultAllowNonIP", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="rule_ids", remote_name="ruleIds", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="auto_generate_priority", remote_name="autoGeneratePriority", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.firewall_rules = NUFirewallRulesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.domains = NUDomainsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def name(self):
        """ Get name value.

            Notes:
                The name of the entity

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                The name of the entity

                
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
                If enabled a default ACL of Allow All is added as the last entry in thelist of ACL entries 

                
                This attribute is named `defaultAllowIP` in VSD API.
                
        """
        return self._default_allow_ip

    @default_allow_ip.setter
    def default_allow_ip(self, value):
        """ Set default_allow_ip value.

            Notes:
                If enabled a default ACL of Allow All is added as the last entry in thelist of ACL entries 

                
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
    def rule_ids(self):
        """ Get rule_ids value.

            Notes:
                Firewall rules associated with this firewall acl.

                
                This attribute is named `ruleIds` in VSD API.
                
        """
        return self._rule_ids

    @rule_ids.setter
    def rule_ids(self, value):
        """ Set rule_ids value.

            Notes:
                Firewall rules associated with this firewall acl.

                
                This attribute is named `ruleIds` in VSD API.
                
        """
        self._rule_ids = value

    
    @property
    def auto_generate_priority(self):
        """ Get auto_generate_priority value.

            Notes:
                If enabled, entries priority will be randomly generated between allowed range.

                
                This attribute is named `autoGeneratePriority` in VSD API.
                
        """
        return self._auto_generate_priority

    @auto_generate_priority.setter
    def auto_generate_priority(self, value):
        """ Set auto_generate_priority value.

            Notes:
                If enabled, entries priority will be randomly generated between allowed range.

                
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

    

    