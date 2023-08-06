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


class NUIKECertificate(NURESTObject):
    """ Represents a IKECertificate in the VSD

        Notes:
            Represents an IKE Trusted Certificate
    """

    __rest_name__ = "ikecertificate"
    __resource_name__ = "ikecertificates"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a IKECertificate instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> ikecertificate = NUIKECertificate(id=u'xxxx-xxx-xxx-xxx', name=u'IKECertificate')
                >>> ikecertificate = NUIKECertificate(data=my_dict)
        """

        super(NUIKECertificate, self).__init__()

        # Read/Write Attributes
        
        self._pem_encoded = None
        self._name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._serial_number = None
        self._description = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._not_after = None
        self._not_before = None
        self._creation_date = None
        self._associated_enterprise_id = None
        self._issuer_dn = None
        self._subject_dn = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="pem_encoded", remote_name="PEMEncoded", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="serial_number", remote_name="serialNumber", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="not_after", remote_name="notAfter", attribute_type=float, is_required=False, is_unique=False)
        self.expose_attribute(local_name="not_before", remote_name="notBefore", attribute_type=float, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_enterprise_id", remote_name="associatedEnterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="issuer_dn", remote_name="issuerDN", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="subject_dn", remote_name="subjectDN", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def pem_encoded(self):
        """ Get pem_encoded value.

            Notes:
                PEM Encoded Certificate

                
                This attribute is named `PEMEncoded` in VSD API.
                
        """
        return self._pem_encoded

    @pem_encoded.setter
    def pem_encoded(self, value):
        """ Set pem_encoded value.

            Notes:
                PEM Encoded Certificate

                
                This attribute is named `PEMEncoded` in VSD API.
                
        """
        self._pem_encoded = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                Name of the Encryption Profile

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                Name of the Encryption Profile

                
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
    def serial_number(self):
        """ Get serial_number value.

            Notes:
                Serial Number of the Certificate - Read Only Attribute

                
                This attribute is named `serialNumber` in VSD API.
                
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, value):
        """ Set serial_number value.

            Notes:
                Serial Number of the Certificate - Read Only Attribute

                
                This attribute is named `serialNumber` in VSD API.
                
        """
        self._serial_number = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Description of the IKEv2 Authentication

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Description of the IKEv2 Authentication

                
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
    def not_after(self):
        """ Get not_after value.

            Notes:
                Date this Certificate is valid to - Read Only Attribute

                
                This attribute is named `notAfter` in VSD API.
                
        """
        return self._not_after

    @not_after.setter
    def not_after(self, value):
        """ Set not_after value.

            Notes:
                Date this Certificate is valid to - Read Only Attribute

                
                This attribute is named `notAfter` in VSD API.
                
        """
        self._not_after = value

    
    @property
    def not_before(self):
        """ Get not_before value.

            Notes:
                Date this Certificate is valid from - Read Only Attribute

                
                This attribute is named `notBefore` in VSD API.
                
        """
        return self._not_before

    @not_before.setter
    def not_before(self, value):
        """ Set not_before value.

            Notes:
                Date this Certificate is valid from - Read Only Attribute

                
                This attribute is named `notBefore` in VSD API.
                
        """
        self._not_before = value

    
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
    def associated_enterprise_id(self):
        """ Get associated_enterprise_id value.

            Notes:
                The ID of the associated Enterprise

                
                This attribute is named `associatedEnterpriseID` in VSD API.
                
        """
        return self._associated_enterprise_id

    @associated_enterprise_id.setter
    def associated_enterprise_id(self, value):
        """ Set associated_enterprise_id value.

            Notes:
                The ID of the associated Enterprise

                
                This attribute is named `associatedEnterpriseID` in VSD API.
                
        """
        self._associated_enterprise_id = value

    
    @property
    def issuer_dn(self):
        """ Get issuer_dn value.

            Notes:
                Issuer Distinguished Name of the Certificate - Read Only Attribute

                
                This attribute is named `issuerDN` in VSD API.
                
        """
        return self._issuer_dn

    @issuer_dn.setter
    def issuer_dn(self, value):
        """ Set issuer_dn value.

            Notes:
                Issuer Distinguished Name of the Certificate - Read Only Attribute

                
                This attribute is named `issuerDN` in VSD API.
                
        """
        self._issuer_dn = value

    
    @property
    def subject_dn(self):
        """ Get subject_dn value.

            Notes:
                Subject Distinguished Name of the Certificate - Read Only Attribute

                
                This attribute is named `subjectDN` in VSD API.
                
        """
        return self._subject_dn

    @subject_dn.setter
    def subject_dn(self, value):
        """ Set subject_dn value.

            Notes:
                Subject Distinguished Name of the Certificate - Read Only Attribute

                
                This attribute is named `subjectDN` in VSD API.
                
        """
        self._subject_dn = value

    
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

    

    