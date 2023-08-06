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


class NUIngressQOSPolicy(NURESTObject):
    """ Represents a IngressQOSPolicy in the VSD

        Notes:
            A Tunnel Shaper QoS Policy is a policy that groups rate-limiting profiles, traffic directionality and classifiers to govern the rate of traffic being sent or received by an end-host or application.
    """

    __rest_name__ = "ingressqospolicy"
    __resource_name__ = "ingressqospolicies"

    
    ## Constants
    
    CONST_QUEUE2_FORWARDING_CLASSES_H = "H"
    
    CONST_QUEUE2_FORWARDING_CLASSES_NONE = "NONE"
    
    CONST_QUEUE2_FORWARDING_CLASSES_A = "A"
    
    CONST_QUEUE2_FORWARDING_CLASSES_B = "B"
    
    CONST_QUEUE2_FORWARDING_CLASSES_C = "C"
    
    CONST_QUEUE2_FORWARDING_CLASSES_D = "D"
    
    CONST_QUEUE2_FORWARDING_CLASSES_E = "E"
    
    CONST_QUEUE2_FORWARDING_CLASSES_F = "F"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_QUEUE4_FORWARDING_CLASSES_NONE = "NONE"
    
    CONST_QUEUE1_FORWARDING_CLASSES_NONE = "NONE"
    
    CONST_QUEUE3_FORWARDING_CLASSES_H = "H"
    
    CONST_QUEUE3_FORWARDING_CLASSES_C = "C"
    
    CONST_QUEUE3_FORWARDING_CLASSES_B = "B"
    
    CONST_QUEUE3_FORWARDING_CLASSES_A = "A"
    
    CONST_QUEUE3_FORWARDING_CLASSES_G = "G"
    
    CONST_QUEUE3_FORWARDING_CLASSES_F = "F"
    
    CONST_QUEUE3_FORWARDING_CLASSES_E = "E"
    
    CONST_QUEUE3_FORWARDING_CLASSES_D = "D"
    
    CONST_QUEUE1_FORWARDING_CLASSES_A = "A"
    
    CONST_QUEUE1_FORWARDING_CLASSES_C = "C"
    
    CONST_QUEUE1_FORWARDING_CLASSES_B = "B"
    
    CONST_QUEUE1_FORWARDING_CLASSES_E = "E"
    
    CONST_QUEUE1_FORWARDING_CLASSES_D = "D"
    
    CONST_QUEUE1_FORWARDING_CLASSES_G = "G"
    
    CONST_QUEUE1_FORWARDING_CLASSES_F = "F"
    
    CONST_QUEUE1_FORWARDING_CLASSES_H = "H"
    
    CONST_QUEUE4_FORWARDING_CLASSES_B = "B"
    
    CONST_QUEUE4_FORWARDING_CLASSES_C = "C"
    
    CONST_QUEUE4_FORWARDING_CLASSES_A = "A"
    
    CONST_QUEUE4_FORWARDING_CLASSES_F = "F"
    
    CONST_QUEUE4_FORWARDING_CLASSES_G = "G"
    
    CONST_QUEUE4_FORWARDING_CLASSES_D = "D"
    
    CONST_QUEUE4_FORWARDING_CLASSES_E = "E"
    
    CONST_QUEUE4_FORWARDING_CLASSES_H = "H"
    
    CONST_QUEUE2_FORWARDING_CLASSES_G = "G"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_QUEUE3_FORWARDING_CLASSES_NONE = "NONE"
    
    

    def __init__(self, **kwargs):
        """ Initializes a IngressQOSPolicy instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> ingressqospolicy = NUIngressQOSPolicy(id=u'xxxx-xxx-xxx-xxx', name=u'IngressQOSPolicy')
                >>> ingressqospolicy = NUIngressQOSPolicy(data=my_dict)
        """

        super(NUIngressQOSPolicy, self).__init__()

        # Read/Write Attributes
        
        self._name = None
        self._parent_queue_associated_rate_limiter_id = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._description = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._creation_date = None
        self._assoc_egress_qos_id = None
        self._queue1_associated_rate_limiter_id = None
        self._queue1_forwarding_classes = None
        self._queue2_associated_rate_limiter_id = None
        self._queue2_forwarding_classes = None
        self._queue3_associated_rate_limiter_id = None
        self._queue3_forwarding_classes = None
        self._queue4_associated_rate_limiter_id = None
        self._queue4_forwarding_classes = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="parent_queue_associated_rate_limiter_id", remote_name="parentQueueAssociatedRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="assoc_egress_qos_id", remote_name="assocEgressQosId", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="queue1_associated_rate_limiter_id", remote_name="queue1AssociatedRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="queue1_forwarding_classes", remote_name="queue1ForwardingClasses", attribute_type=list, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name="queue2_associated_rate_limiter_id", remote_name="queue2AssociatedRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="queue2_forwarding_classes", remote_name="queue2ForwardingClasses", attribute_type=list, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name="queue3_associated_rate_limiter_id", remote_name="queue3AssociatedRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="queue3_forwarding_classes", remote_name="queue3ForwardingClasses", attribute_type=list, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name="queue4_associated_rate_limiter_id", remote_name="queue4AssociatedRateLimiterID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="queue4_forwarding_classes", remote_name="queue4ForwardingClasses", attribute_type=list, is_required=False, is_unique=False, choices=[u'A', u'B', u'C', u'D', u'E', u'F', u'G', u'H', u'NONE'])
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def name(self):
        """ Get name value.

            Notes:
                A unique name of the QoS object

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                A unique name of the QoS object

                
        """
        self._name = value

    
    @property
    def parent_queue_associated_rate_limiter_id(self):
        """ Get parent_queue_associated_rate_limiter_id value.

            Notes:
                ID of the parent rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `parentQueueAssociatedRateLimiterID` in VSD API.
                
        """
        return self._parent_queue_associated_rate_limiter_id

    @parent_queue_associated_rate_limiter_id.setter
    def parent_queue_associated_rate_limiter_id(self, value):
        """ Set parent_queue_associated_rate_limiter_id value.

            Notes:
                ID of the parent rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `parentQueueAssociatedRateLimiterID` in VSD API.
                
        """
        self._parent_queue_associated_rate_limiter_id = value

    
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
    def description(self):
        """ Get description value.

            Notes:
                A description of the QoS object

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                A description of the QoS object

                
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
    def assoc_egress_qos_id(self):
        """ Get assoc_egress_qos_id value.

            Notes:
                ID of object associated with this QoS object

                
                This attribute is named `assocEgressQosId` in VSD API.
                
        """
        return self._assoc_egress_qos_id

    @assoc_egress_qos_id.setter
    def assoc_egress_qos_id(self, value):
        """ Set assoc_egress_qos_id value.

            Notes:
                ID of object associated with this QoS object

                
                This attribute is named `assocEgressQosId` in VSD API.
                
        """
        self._assoc_egress_qos_id = value

    
    @property
    def queue1_associated_rate_limiter_id(self):
        """ Get queue1_associated_rate_limiter_id value.

            Notes:
                ID of the queue1 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue1AssociatedRateLimiterID` in VSD API.
                
        """
        return self._queue1_associated_rate_limiter_id

    @queue1_associated_rate_limiter_id.setter
    def queue1_associated_rate_limiter_id(self, value):
        """ Set queue1_associated_rate_limiter_id value.

            Notes:
                ID of the queue1 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue1AssociatedRateLimiterID` in VSD API.
                
        """
        self._queue1_associated_rate_limiter_id = value

    
    @property
    def queue1_forwarding_classes(self):
        """ Get queue1_forwarding_classes value.

            Notes:
                Queue1 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue1ForwardingClasses` in VSD API.
                
        """
        return self._queue1_forwarding_classes

    @queue1_forwarding_classes.setter
    def queue1_forwarding_classes(self, value):
        """ Set queue1_forwarding_classes value.

            Notes:
                Queue1 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue1ForwardingClasses` in VSD API.
                
        """
        self._queue1_forwarding_classes = value

    
    @property
    def queue2_associated_rate_limiter_id(self):
        """ Get queue2_associated_rate_limiter_id value.

            Notes:
                ID of the queue2 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue2AssociatedRateLimiterID` in VSD API.
                
        """
        return self._queue2_associated_rate_limiter_id

    @queue2_associated_rate_limiter_id.setter
    def queue2_associated_rate_limiter_id(self, value):
        """ Set queue2_associated_rate_limiter_id value.

            Notes:
                ID of the queue2 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue2AssociatedRateLimiterID` in VSD API.
                
        """
        self._queue2_associated_rate_limiter_id = value

    
    @property
    def queue2_forwarding_classes(self):
        """ Get queue2_forwarding_classes value.

            Notes:
                Queue2 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue2ForwardingClasses` in VSD API.
                
        """
        return self._queue2_forwarding_classes

    @queue2_forwarding_classes.setter
    def queue2_forwarding_classes(self, value):
        """ Set queue2_forwarding_classes value.

            Notes:
                Queue2 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue2ForwardingClasses` in VSD API.
                
        """
        self._queue2_forwarding_classes = value

    
    @property
    def queue3_associated_rate_limiter_id(self):
        """ Get queue3_associated_rate_limiter_id value.

            Notes:
                ID of the queue3 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue3AssociatedRateLimiterID` in VSD API.
                
        """
        return self._queue3_associated_rate_limiter_id

    @queue3_associated_rate_limiter_id.setter
    def queue3_associated_rate_limiter_id(self, value):
        """ Set queue3_associated_rate_limiter_id value.

            Notes:
                ID of the queue3 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue3AssociatedRateLimiterID` in VSD API.
                
        """
        self._queue3_associated_rate_limiter_id = value

    
    @property
    def queue3_forwarding_classes(self):
        """ Get queue3_forwarding_classes value.

            Notes:
                Queue3 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue3ForwardingClasses` in VSD API.
                
        """
        return self._queue3_forwarding_classes

    @queue3_forwarding_classes.setter
    def queue3_forwarding_classes(self, value):
        """ Set queue3_forwarding_classes value.

            Notes:
                Queue3 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue3ForwardingClasses` in VSD API.
                
        """
        self._queue3_forwarding_classes = value

    
    @property
    def queue4_associated_rate_limiter_id(self):
        """ Get queue4_associated_rate_limiter_id value.

            Notes:
                ID of the queue4 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue4AssociatedRateLimiterID` in VSD API.
                
        """
        return self._queue4_associated_rate_limiter_id

    @queue4_associated_rate_limiter_id.setter
    def queue4_associated_rate_limiter_id(self, value):
        """ Set queue4_associated_rate_limiter_id value.

            Notes:
                ID of the queue4 rate limiter associated with this Ingress QOS policy.

                
                This attribute is named `queue4AssociatedRateLimiterID` in VSD API.
                
        """
        self._queue4_associated_rate_limiter_id = value

    
    @property
    def queue4_forwarding_classes(self):
        """ Get queue4_forwarding_classes value.

            Notes:
                Queue4 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue4ForwardingClasses` in VSD API.
                
        """
        return self._queue4_forwarding_classes

    @queue4_forwarding_classes.setter
    def queue4_forwarding_classes(self, value):
        """ Set queue4_forwarding_classes value.

            Notes:
                Queue4 Forwarding Classes for this Ingress QOS Policy Possible values are NONE, A, B, C, D, E, F, G, H, .

                
                This attribute is named `queue4ForwardingClasses` in VSD API.
                
        """
        self._queue4_forwarding_classes = value

    
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

    

    