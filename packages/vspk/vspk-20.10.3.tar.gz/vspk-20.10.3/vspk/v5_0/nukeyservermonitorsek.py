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


class NUKeyServerMonitorSEK(NURESTObject):
    """ Represents a KeyServerMonitorSEK in the VSD

        Notes:
            Represents a Keyserver Monitor SEK Snapshot.
    """

    __rest_name__ = "keyservermonitorsek"
    __resource_name__ = "keyservermonitorseks"

    
    ## Constants
    
    CONST_SEED_PAYLOAD_AUTHENTICATION_ALGORITHM_HMAC_SHA256 = "HMAC_SHA256"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_SEED_PAYLOAD_ENCRYPTION_ALGORITHM_AES_128_CBC = "AES_128_CBC"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_SEED_PAYLOAD_AUTHENTICATION_ALGORITHM_HMAC_SHA512 = "HMAC_SHA512"
    
    CONST_SEED_PAYLOAD_ENCRYPTION_ALGORITHM_AES_256_CBC = "AES_256_CBC"
    
    CONST_SEED_PAYLOAD_ENCRYPTION_ALGORITHM_TRIPLE_DES_CBC = "TRIPLE_DES_CBC"
    
    CONST_SEED_PAYLOAD_AUTHENTICATION_ALGORITHM_HMAC_SHA1 = "HMAC_SHA1"
    
    

    def __init__(self, **kwargs):
        """ Initializes a KeyServerMonitorSEK instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> keyservermonitorsek = NUKeyServerMonitorSEK(id=u'xxxx-xxx-xxx-xxx', name=u'KeyServerMonitorSEK')
                >>> keyservermonitorsek = NUKeyServerMonitorSEK(data=my_dict)
        """

        super(NUKeyServerMonitorSEK, self).__init__()

        # Read/Write Attributes
        
        self._last_updated_by = None
        self._seed_payload_authentication_algorithm = None
        self._seed_payload_encryption_algorithm = None
        self._lifetime = None
        self._entity_scope = None
        self._creation_time = None
        self._start_time = None
        self._external_id = None
        
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="seed_payload_authentication_algorithm", remote_name="seedPayloadAuthenticationAlgorithm", attribute_type=str, is_required=False, is_unique=False, choices=[u'HMAC_SHA1', u'HMAC_SHA256', u'HMAC_SHA512'])
        self.expose_attribute(local_name="seed_payload_encryption_algorithm", remote_name="seedPayloadEncryptionAlgorithm", attribute_type=str, is_required=False, is_unique=False, choices=[u'AES_128_CBC', u'AES_256_CBC', u'TRIPLE_DES_CBC'])
        self.expose_attribute(local_name="lifetime", remote_name="lifetime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_time", remote_name="creationTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="start_time", remote_name="startTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
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
    def seed_payload_authentication_algorithm(self):
        """ Get seed_payload_authentication_algorithm value.

            Notes:
                SEK Payload Signature Algorithm Possible values are HMAC_SHA1, HMAC_SHA256, HMAC_SHA512, .

                
                This attribute is named `seedPayloadAuthenticationAlgorithm` in VSD API.
                
        """
        return self._seed_payload_authentication_algorithm

    @seed_payload_authentication_algorithm.setter
    def seed_payload_authentication_algorithm(self, value):
        """ Set seed_payload_authentication_algorithm value.

            Notes:
                SEK Payload Signature Algorithm Possible values are HMAC_SHA1, HMAC_SHA256, HMAC_SHA512, .

                
                This attribute is named `seedPayloadAuthenticationAlgorithm` in VSD API.
                
        """
        self._seed_payload_authentication_algorithm = value

    
    @property
    def seed_payload_encryption_algorithm(self):
        """ Get seed_payload_encryption_algorithm value.

            Notes:
                SEK Payload Encryption Algorithm Possible values are AES_128_CBC, AES_256_CBC, TRIPLE_DES_CBC, .

                
                This attribute is named `seedPayloadEncryptionAlgorithm` in VSD API.
                
        """
        return self._seed_payload_encryption_algorithm

    @seed_payload_encryption_algorithm.setter
    def seed_payload_encryption_algorithm(self, value):
        """ Set seed_payload_encryption_algorithm value.

            Notes:
                SEK Payload Encryption Algorithm Possible values are AES_128_CBC, AES_256_CBC, TRIPLE_DES_CBC, .

                
                This attribute is named `seedPayloadEncryptionAlgorithm` in VSD API.
                
        """
        self._seed_payload_encryption_algorithm = value

    
    @property
    def lifetime(self):
        """ Get lifetime value.

            Notes:
                The lifetime of this entry (seconds)

                
        """
        return self._lifetime

    @lifetime.setter
    def lifetime(self, value):
        """ Set lifetime value.

            Notes:
                The lifetime of this entry (seconds)

                
        """
        self._lifetime = value

    
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
    def creation_time(self):
        """ Get creation_time value.

            Notes:
                The time this entry was created (milliseconds since epoch)

                
                This attribute is named `creationTime` in VSD API.
                
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value):
        """ Set creation_time value.

            Notes:
                The time this entry was created (milliseconds since epoch)

                
                This attribute is named `creationTime` in VSD API.
                
        """
        self._creation_time = value

    
    @property
    def start_time(self):
        """ Get start_time value.

            Notes:
                The time this entry  was activated (milliseconds since epoch)

                
                This attribute is named `startTime` in VSD API.
                
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """ Set start_time value.

            Notes:
                The time this entry  was activated (milliseconds since epoch)

                
                This attribute is named `startTime` in VSD API.
                
        """
        self._start_time = value

    
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

    

    