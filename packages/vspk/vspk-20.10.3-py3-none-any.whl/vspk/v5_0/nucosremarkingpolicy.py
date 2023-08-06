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


class NUCOSRemarkingPolicy(NURESTObject):
    """ Represents a COSRemarkingPolicy in the VSD

        Notes:
            Provides the definition of a single Forwarding class to CoS mapping that is part of a COS Remarking Policy Table used in QoS policies.
    """

    __rest_name__ = "cosremarkingpolicy"
    __resource_name__ = "cosremarkingpolicies"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_FORWARDING_CLASS_E = "E"
    
    CONST_FORWARDING_CLASS_D = "D"
    
    CONST_FORWARDING_CLASS_G = "G"
    
    CONST_FORWARDING_CLASS_F = "F"
    
    CONST_FORWARDING_CLASS_A = "A"
    
    CONST_FORWARDING_CLASS_C = "C"
    
    CONST_FORWARDING_CLASS_B = "B"
    
    CONST_FORWARDING_CLASS_H = "H"
    
    

    def __init__(self, **kwargs):
        """ Initializes a COSRemarkingPolicy instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> cosremarkingpolicy = NUCOSRemarkingPolicy(id=u'xxxx-xxx-xxx-xxx', name=u'COSRemarkingPolicy')
                >>> cosremarkingpolicy = NUCOSRemarkingPolicy(data=my_dict)
        """

        super(NUCOSRemarkingPolicy, self).__init__()

        # Read/Write Attributes
        
        self._dscp = None
        self._last_updated_by = None
        self._entity_scope = None
        self._forwarding_class = None
        self._external_id = None
        
        self.expose_attribute(local_name="dscp", remote_name="DSCP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="forwarding_class", remote_name="forwardingClass", attribute_type=str, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H'])
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def dscp(self):
        """ Get dscp value.

            Notes:
                DSCP value range from enumeration of 8 values: *, 0, 1, ..., 7

                
                This attribute is named `DSCP` in VSD API.
                
        """
        return self._dscp

    @dscp.setter
    def dscp(self, value):
        """ Set dscp value.

            Notes:
                DSCP value range from enumeration of 8 values: *, 0, 1, ..., 7

                
                This attribute is named `DSCP` in VSD API.
                
        """
        self._dscp = value

    
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
    def forwarding_class(self):
        """ Get forwarding_class value.

            Notes:
                Class of service to be used. Service classes in order of priority are A, B, C, D, E, F, G, and H.

                
                This attribute is named `forwardingClass` in VSD API.
                
        """
        return self._forwarding_class

    @forwarding_class.setter
    def forwarding_class(self, value):
        """ Set forwarding_class value.

            Notes:
                Class of service to be used. Service classes in order of priority are A, B, C, D, E, F, G, and H.

                
                This attribute is named `forwardingClass` in VSD API.
                
        """
        self._forwarding_class = value

    
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

    

    