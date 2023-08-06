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


from .fetchers import NUPortTemplatesFetcher

from bambou import NURESTObject


class NUGatewayTemplate(NURESTObject):
    """ Represents a GatewayTemplate in the VSD

        Notes:
            A gateway is your point of exit to an external network. It can be a physical or a virtual device. Gateways are templatable. You can attach gateway's VLANs to any existing host or bridge VPorts.
    """

    __rest_name__ = "gatewaytemplate"
    __resource_name__ = "gatewaytemplates"

    
    ## Constants
    
    CONST_PERSONALITY_HARDWARE_VTEP = "HARDWARE_VTEP"
    
    CONST_PERSONALITY_EVDFB = "EVDFB"
    
    CONST_PERSONALITY_VSA = "VSA"
    
    CONST_PERSONALITY_VSG = "VSG"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_PERSONALITY_OTHER = "OTHER"
    
    CONST_PERSONALITY_UNMANAGED_GATEWAY = "UNMANAGED_GATEWAY"
    
    CONST_PERSONALITY_EVDF = "EVDF"
    
    CONST_PERSONALITY_VDFG = "VDFG"
    
    CONST_PERSONALITY_VRSB = "VRSB"
    
    CONST_PERSONALITY_NETCONF_7X50 = "NETCONF_7X50"
    
    CONST_PERSONALITY_NUAGE_210_WBX_48_S = "NUAGE_210_WBX_48_S"
    
    CONST_PERSONALITY_NUAGE_210_WBX_32_Q = "NUAGE_210_WBX_32_Q"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_PERSONALITY_SR_LINUX = "SR_LINUX"
    
    CONST_PERSONALITY_DC7X50 = "DC7X50"
    
    CONST_PERSONALITY_VRSG = "VRSG"
    
    CONST_PERSONALITY_NETCONF_THIRDPARTY_HW_VTEP = "NETCONF_THIRDPARTY_HW_VTEP"
    
    

    def __init__(self, **kwargs):
        """ Initializes a GatewayTemplate instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> gatewaytemplate = NUGatewayTemplate(id=u'xxxx-xxx-xxx-xxx', name=u'GatewayTemplate')
                >>> gatewaytemplate = NUGatewayTemplate(data=my_dict)
        """

        super(NUGatewayTemplate, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._native_vlan = None
        self._personality = None
        self._description = None
        self._embedded_metadata = None
        self._infrastructure_profile_id = None
        self._enterprise_id = None
        self._entity_scope = None
        self._creation_date = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="native_vlan", remote_name="nativeVLAN", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="personality", remote_name="personality", attribute_type=str, is_required=True, is_unique=False, choices=[u'DC7X50', u'EVDF', u'EVDFB', u'HARDWARE_VTEP', u'NETCONF_7X50', u'NETCONF_THIRDPARTY_HW_VTEP', u'NUAGE_210_WBX_32_Q', u'NUAGE_210_WBX_48_S', u'OTHER', u'SR_LINUX', u'UNMANAGED_GATEWAY', u'VDFG', u'VRSB', u'VRSG', u'VSA', u'VSG'])
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="infrastructure_profile_id", remote_name="infrastructureProfileID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enterprise_id", remote_name="enterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.port_templates = NUPortTemplatesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the Gateway

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the Gateway

                
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
    def native_vlan(self):
        """ Get native_vlan value.

            Notes:
                Default Native VLAN to carry untagged traffic on the ports of the gateways using this template. Applicable for Cisco 9K only. Possible values are 1-3967.

                
                This attribute is named `nativeVLAN` in VSD API.
                
        """
        return self._native_vlan

    @native_vlan.setter
    def native_vlan(self, value):
        """ Set native_vlan value.

            Notes:
                Default Native VLAN to carry untagged traffic on the ports of the gateways using this template. Applicable for Cisco 9K only. Possible values are 1-3967.

                
                This attribute is named `nativeVLAN` in VSD API.
                
        """
        self._native_vlan = value

    
    @property
    def personality(self):
        """ Get personality value.

            Notes:
                Personality of the Gateway, cannot be changed after creation.

                
        """
        return self._personality

    @personality.setter
    def personality(self, value):
        """ Set personality value.

            Notes:
                Personality of the Gateway, cannot be changed after creation.

                
        """
        self._personality = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                A description of the Gateway

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the Gateway

                
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
    def infrastructure_profile_id(self):
        """ Get infrastructure_profile_id value.

            Notes:
                The ID of the associated Infrastructure Gateway Profile tied to this instance of a Gateway Template.

                
                This attribute is named `infrastructureProfileID` in VSD API.
                
        """
        return self._infrastructure_profile_id

    @infrastructure_profile_id.setter
    def infrastructure_profile_id(self, value):
        """ Set infrastructure_profile_id value.

            Notes:
                The ID of the associated Infrastructure Gateway Profile tied to this instance of a Gateway Template.

                
                This attribute is named `infrastructureProfileID` in VSD API.
                
        """
        self._infrastructure_profile_id = value

    
    @property
    def enterprise_id(self):
        """ Get enterprise_id value.

            Notes:
                The enterprise associated with this Gateway. This is a read only attribute

                
                This attribute is named `enterpriseID` in VSD API.
                
        """
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, value):
        """ Set enterprise_id value.

            Notes:
                The enterprise associated with this Gateway. This is a read only attribute

                
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

    

    
    ## Custom methods
    def is_template(self):
        """ Verify that the object is a template
    
            Returns:
                (bool): True if the object is a template
        """
        return True
    
    def is_from_template(self):
        """ Verify if the object has been instantiated from a template
    
            Note:
                The object has to be fetched. Otherwise, it does not
                have information from its parent
    
            Returns:
                (bool): True if the object is a template
        """
        return False
    