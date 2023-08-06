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


class NUOverlayPATNATEntry(NURESTObject):
    """ Represents a OverlayPATNATEntry in the VSD

        Notes:
            Create a static NAT 1:1 IP mapping between a Pool IP and a host IP in the branch domain, to provide access to the branch resource.
    """

    __rest_name__ = "overlaypatnatentry"
    __resource_name__ = "overlaypatnatentries"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a OverlayPATNATEntry instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> overlaypatnatentry = NUOverlayPATNATEntry(id=u'xxxx-xxx-xxx-xxx', name=u'OverlayPATNATEntry')
                >>> overlaypatnatentry = NUOverlayPATNATEntry(data=my_dict)
        """

        super(NUOverlayPATNATEntry, self).__init__()

        # Read/Write Attributes
        
        self._nat_enabled = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._creation_date = None
        self._private_ip = None
        self._associated_domain_id = None
        self._associated_link_id = None
        self._public_ip = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="nat_enabled", remote_name="NATEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="private_ip", remote_name="privateIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_domain_id", remote_name="associatedDomainID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_link_id", remote_name="associatedLinkID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="public_ip", remote_name="publicIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def nat_enabled(self):
        """ Get nat_enabled value.

            Notes:
                This flag will determine whether the entry is NAT or PAT.

                
                This attribute is named `NATEnabled` in VSD API.
                
        """
        return self._nat_enabled

    @nat_enabled.setter
    def nat_enabled(self, value):
        """ Set nat_enabled value.

            Notes:
                This flag will determine whether the entry is NAT or PAT.

                
                This attribute is named `NATEnabled` in VSD API.
                
        """
        self._nat_enabled = value

    
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
    def private_ip(self):
        """ Get private_ip value.

            Notes:
                Private IP address for the interface

                
                This attribute is named `privateIP` in VSD API.
                
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, value):
        """ Set private_ip value.

            Notes:
                Private IP address for the interface

                
                This attribute is named `privateIP` in VSD API.
                
        """
        self._private_ip = value

    
    @property
    def associated_domain_id(self):
        """ Get associated_domain_id value.

            Notes:
                The ID of the associated l3-domain.

                
                This attribute is named `associatedDomainID` in VSD API.
                
        """
        return self._associated_domain_id

    @associated_domain_id.setter
    def associated_domain_id(self, value):
        """ Set associated_domain_id value.

            Notes:
                The ID of the associated l3-domain.

                
                This attribute is named `associatedDomainID` in VSD API.
                
        """
        self._associated_domain_id = value

    
    @property
    def associated_link_id(self):
        """ Get associated_link_id value.

            Notes:
                The ID of the associated domain-link.

                
                This attribute is named `associatedLinkID` in VSD API.
                
        """
        return self._associated_link_id

    @associated_link_id.setter
    def associated_link_id(self, value):
        """ Set associated_link_id value.

            Notes:
                The ID of the associated domain-link.

                
                This attribute is named `associatedLinkID` in VSD API.
                
        """
        self._associated_link_id = value

    
    @property
    def public_ip(self):
        """ Get public_ip value.

            Notes:
                Public IP address of the interface

                
                This attribute is named `publicIP` in VSD API.
                
        """
        return self._public_ip

    @public_ip.setter
    def public_ip(self, value):
        """ Set public_ip value.

            Notes:
                Public IP address of the interface

                
                This attribute is named `publicIP` in VSD API.
                
        """
        self._public_ip = value

    
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

    

    