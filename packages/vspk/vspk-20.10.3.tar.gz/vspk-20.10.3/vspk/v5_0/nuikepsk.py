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


class NUIKEPSK(NURESTObject):
    """ Represents a IKEPSK in the VSD

        Notes:
            Shared secret used during the authentication phase of IKE protocol.
    """

    __rest_name__ = "ikepsk"
    __resource_name__ = "ikepsks"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a IKEPSK instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> ikepsk = NUIKEPSK(id=u'xxxx-xxx-xxx-xxx', name=u'IKEPSK')
                >>> ikepsk = NUIKEPSK(data=my_dict)
        """

        super(NUIKEPSK, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._last_updated_by = None
        self._description = None
        self._signature = None
        self._signing_certificate_serial_number = None
        self._encrypted_psk = None
        self._encrypting_certificate_serial_number = None
        self._unencrypted_psk = None
        self._entity_scope = None
        self._associated_enterprise_id = None
        self._auto_created = None
        self._external_id = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="signature", remote_name="signature", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="signing_certificate_serial_number", remote_name="signingCertificateSerialNumber", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="encrypted_psk", remote_name="encryptedPSK", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="encrypting_certificate_serial_number", remote_name="encryptingCertificateSerialNumber", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="unencrypted_psk", remote_name="unencryptedPSK", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="associated_enterprise_id", remote_name="associatedEnterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="auto_created", remote_name="autoCreated", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
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
    def signature(self):
        """ Get signature value.

            Notes:
                Base64 Encoded private key signature

                
        """
        return self._signature

    @signature.setter
    def signature(self, value):
        """ Set signature value.

            Notes:
                Base64 Encoded private key signature

                
        """
        self._signature = value

    
    @property
    def signing_certificate_serial_number(self):
        """ Get signing_certificate_serial_number value.

            Notes:
                Serial Number of the certificate needed to verify the encrypted data

                
                This attribute is named `signingCertificateSerialNumber` in VSD API.
                
        """
        return self._signing_certificate_serial_number

    @signing_certificate_serial_number.setter
    def signing_certificate_serial_number(self, value):
        """ Set signing_certificate_serial_number value.

            Notes:
                Serial Number of the certificate needed to verify the encrypted data

                
                This attribute is named `signingCertificateSerialNumber` in VSD API.
                
        """
        self._signing_certificate_serial_number = value

    
    @property
    def encrypted_psk(self):
        """ Get encrypted_psk value.

            Notes:
                Base64 Encoded Encrypted PSK

                
                This attribute is named `encryptedPSK` in VSD API.
                
        """
        return self._encrypted_psk

    @encrypted_psk.setter
    def encrypted_psk(self, value):
        """ Set encrypted_psk value.

            Notes:
                Base64 Encoded Encrypted PSK

                
                This attribute is named `encryptedPSK` in VSD API.
                
        """
        self._encrypted_psk = value

    
    @property
    def encrypting_certificate_serial_number(self):
        """ Get encrypting_certificate_serial_number value.

            Notes:
                Serial Number of the certificate of the public key that encrypted this data

                
                This attribute is named `encryptingCertificateSerialNumber` in VSD API.
                
        """
        return self._encrypting_certificate_serial_number

    @encrypting_certificate_serial_number.setter
    def encrypting_certificate_serial_number(self, value):
        """ Set encrypting_certificate_serial_number value.

            Notes:
                Serial Number of the certificate of the public key that encrypted this data

                
                This attribute is named `encryptingCertificateSerialNumber` in VSD API.
                
        """
        self._encrypting_certificate_serial_number = value

    
    @property
    def unencrypted_psk(self):
        """ Get unencrypted_psk value.

            Notes:
                Unencrypted PSK

                
                This attribute is named `unencryptedPSK` in VSD API.
                
        """
        return self._unencrypted_psk

    @unencrypted_psk.setter
    def unencrypted_psk(self, value):
        """ Set unencrypted_psk value.

            Notes:
                Unencrypted PSK

                
                This attribute is named `unencryptedPSK` in VSD API.
                
        """
        self._unencrypted_psk = value

    
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
    def auto_created(self):
        """ Get auto_created value.

            Notes:
                Was this object autocreated from the connection

                
                This attribute is named `autoCreated` in VSD API.
                
        """
        return self._auto_created

    @auto_created.setter
    def auto_created(self, value):
        """ Set auto_created value.

            Notes:
                Was this object autocreated from the connection

                
                This attribute is named `autoCreated` in VSD API.
                
        """
        self._auto_created = value

    
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

    

    