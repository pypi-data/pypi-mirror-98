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


from .fetchers import NUMonitorscopesFetcher


from .fetchers import NUApplicationBindingsFetcher

from bambou import NURESTObject


class NUApplication(NURESTObject):
    """ Represents a Application in the VSD

        Notes:
            represents a application with L4/L7 classification
    """

    __rest_name__ = "application"
    __resource_name__ = "applications"

    
    ## Constants
    
    CONST_POST_CLASSIFICATION_PATH_ANY = "ANY"
    
    CONST_PROTOCOL_NONE = "NONE"
    
    CONST_PERFORMANCE_MONITOR_TYPE_FIRST_PACKET = "FIRST_PACKET"
    
    CONST_PRE_CLASSIFICATION_PATH_PRIMARY = "PRIMARY"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_PRE_CLASSIFICATION_PATH_SECONDARY = "SECONDARY"
    
    CONST_PERFORMANCE_MONITOR_TYPE_CONTINUOUS = "CONTINUOUS"
    
    CONST_OPTIMIZE_PATH_SELECTION_PACKETLOSS = "PACKETLOSS"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_OPTIMIZE_PATH_SELECTION_LATENCY = "LATENCY"
    
    CONST_OPTIMIZE_PATH_SELECTION_JITTER = "JITTER"
    
    CONST_PROTOCOL_UDP = "UDP"
    
    CONST_POST_CLASSIFICATION_PATH_PRIMARY = "PRIMARY"
    
    CONST_POST_CLASSIFICATION_PATH_SECONDARY = "SECONDARY"
    
    CONST_PERFORMANCE_MONITOR_TYPE_FIRST_PACKET_AND_CONTINUOUS = "FIRST_PACKET_AND_CONTINUOUS"
    
    CONST_PROTOCOL_TCP = "TCP"
    
    CONST_PRE_CLASSIFICATION_PATH_DEFAULT = "DEFAULT"
    
    

    def __init__(self, **kwargs):
        """ Initializes a Application instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> application = NUApplication(id=u'xxxx-xxx-xxx-xxx', name=u'Application')
                >>> application = NUApplication(data=my_dict)
        """

        super(NUApplication, self).__init__()

        # Read/Write Attributes
        
        self._dscp = None
        self._name = None
        self._bandwidth = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._read_only = None
        self._performance_monitor_type = None
        self._certificate_common_name = None
        self._description = None
        self._destination_ip = None
        self._destination_port = None
        self._network_symmetry = None
        self._embedded_metadata = None
        self._enable_pps = None
        self._one_way_delay = None
        self._one_way_jitter = None
        self._one_way_loss = None
        self._entity_scope = None
        self._post_classification_path = None
        self._source_ip = None
        self._source_port = None
        self._app_id = None
        self._optimize_path_selection = None
        self._pre_classification_path = None
        self._creation_date = None
        self._protocol = None
        self._associated_l7_application_signature_id = None
        self._ether_type = None
        self._owner = None
        self._external_id = None
        self._symmetry = None
        
        self.expose_attribute(local_name="dscp", remote_name="DSCP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="bandwidth", remote_name="bandwidth", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="read_only", remote_name="readOnly", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="performance_monitor_type", remote_name="performanceMonitorType", attribute_type=str, is_required=False, is_unique=False, choices=[u'CONTINUOUS', u'FIRST_PACKET', u'FIRST_PACKET_AND_CONTINUOUS'])
        self.expose_attribute(local_name="certificate_common_name", remote_name="certificateCommonName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="destination_ip", remote_name="destinationIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="destination_port", remote_name="destinationPort", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="network_symmetry", remote_name="networkSymmetry", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enable_pps", remote_name="enablePPS", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="one_way_delay", remote_name="oneWayDelay", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="one_way_jitter", remote_name="oneWayJitter", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="one_way_loss", remote_name="oneWayLoss", attribute_type=float, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="post_classification_path", remote_name="postClassificationPath", attribute_type=str, is_required=False, is_unique=False, choices=[u'ANY', u'PRIMARY', u'SECONDARY'])
        self.expose_attribute(local_name="source_ip", remote_name="sourceIP", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="source_port", remote_name="sourcePort", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="app_id", remote_name="appId", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="optimize_path_selection", remote_name="optimizePathSelection", attribute_type=str, is_required=False, is_unique=False, choices=[u'JITTER', u'LATENCY', u'PACKETLOSS'])
        self.expose_attribute(local_name="pre_classification_path", remote_name="preClassificationPath", attribute_type=str, is_required=False, is_unique=False, choices=[u'DEFAULT', u'PRIMARY', u'SECONDARY'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="protocol", remote_name="protocol", attribute_type=str, is_required=False, is_unique=False, choices=[u'NONE', u'TCP', u'UDP'])
        self.expose_attribute(local_name="associated_l7_application_signature_id", remote_name="associatedL7ApplicationSignatureID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ether_type", remote_name="etherType", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="symmetry", remote_name="symmetry", attribute_type=bool, is_required=False, is_unique=False)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.monitorscopes = NUMonitorscopesFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.application_bindings = NUApplicationBindingsFetcher.fetcher_with_object(parent_object=self, relationship="member")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def dscp(self):
        """ Get dscp value.

            Notes:
                DSCP match condition to be set in the rule. It is either * or from 0-63.

                
                This attribute is named `DSCP` in VSD API.
                
        """
        return self._dscp

    @dscp.setter
    def dscp(self, value):
        """ Set dscp value.

            Notes:
                DSCP match condition to be set in the rule. It is either * or from 0-63.

                
                This attribute is named `DSCP` in VSD API.
                
        """
        self._dscp = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                name of the application

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                name of the application

                
        """
        self._name = value

    
    @property
    def bandwidth(self):
        """ Get bandwidth value.

            Notes:
                Minimum Failover Bandwidth of the application.

                
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        """ Set bandwidth value.

            Notes:
                Minimum Failover Bandwidth of the application.

                
        """
        self._bandwidth = value

    
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
    def read_only(self):
        """ Get read_only value.

            Notes:
                determines whether this entity is read only.  Read only objects cannot be modified or deleted.

                
                This attribute is named `readOnly` in VSD API.
                
        """
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        """ Set read_only value.

            Notes:
                determines whether this entity is read only.  Read only objects cannot be modified or deleted.

                
                This attribute is named `readOnly` in VSD API.
                
        """
        self._read_only = value

    
    @property
    def performance_monitor_type(self):
        """ Get performance_monitor_type value.

            Notes:
                Describes the trigger for the application.

                
                This attribute is named `performanceMonitorType` in VSD API.
                
        """
        return self._performance_monitor_type

    @performance_monitor_type.setter
    def performance_monitor_type(self, value):
        """ Set performance_monitor_type value.

            Notes:
                Describes the trigger for the application.

                
                This attribute is named `performanceMonitorType` in VSD API.
                
        """
        self._performance_monitor_type = value

    
    @property
    def certificate_common_name(self):
        """ Get certificate_common_name value.

            Notes:
                Describes the certificate common name

                
                This attribute is named `certificateCommonName` in VSD API.
                
        """
        return self._certificate_common_name

    @certificate_common_name.setter
    def certificate_common_name(self, value):
        """ Set certificate_common_name value.

            Notes:
                Describes the certificate common name

                
                This attribute is named `certificateCommonName` in VSD API.
                
        """
        self._certificate_common_name = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                description of Application

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                description of Application

                
        """
        self._description = value

    
    @property
    def destination_ip(self):
        """ Get destination_ip value.

            Notes:
                destination IP in CIDR format

                
                This attribute is named `destinationIP` in VSD API.
                
        """
        return self._destination_ip

    @destination_ip.setter
    def destination_ip(self, value):
        """ Set destination_ip value.

            Notes:
                destination IP in CIDR format

                
                This attribute is named `destinationIP` in VSD API.
                
        """
        self._destination_ip = value

    
    @property
    def destination_port(self):
        """ Get destination_port value.

            Notes:
                value should be either * or single port number or maximum 5 ranges comma separated.

                
                This attribute is named `destinationPort` in VSD API.
                
        """
        return self._destination_port

    @destination_port.setter
    def destination_port(self, value):
        """ Set destination_port value.

            Notes:
                value should be either * or single port number or maximum 5 ranges comma separated.

                
                This attribute is named `destinationPort` in VSD API.
                
        """
        self._destination_port = value

    
    @property
    def network_symmetry(self):
        """ Get network_symmetry value.

            Notes:
                Network symmetry flag

                
                This attribute is named `networkSymmetry` in VSD API.
                
        """
        return self._network_symmetry

    @network_symmetry.setter
    def network_symmetry(self, value):
        """ Set network_symmetry value.

            Notes:
                Network symmetry flag

                
                This attribute is named `networkSymmetry` in VSD API.
                
        """
        self._network_symmetry = value

    
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
    def enable_pps(self):
        """ Get enable_pps value.

            Notes:
                Enable the performance probe for this application

                
                This attribute is named `enablePPS` in VSD API.
                
        """
        return self._enable_pps

    @enable_pps.setter
    def enable_pps(self, value):
        """ Set enable_pps value.

            Notes:
                Enable the performance probe for this application

                
                This attribute is named `enablePPS` in VSD API.
                
        """
        self._enable_pps = value

    
    @property
    def one_way_delay(self):
        """ Get one_way_delay value.

            Notes:
                one way Delay

                
                This attribute is named `oneWayDelay` in VSD API.
                
        """
        return self._one_way_delay

    @one_way_delay.setter
    def one_way_delay(self, value):
        """ Set one_way_delay value.

            Notes:
                one way Delay

                
                This attribute is named `oneWayDelay` in VSD API.
                
        """
        self._one_way_delay = value

    
    @property
    def one_way_jitter(self):
        """ Get one_way_jitter value.

            Notes:
                one way Jitter

                
                This attribute is named `oneWayJitter` in VSD API.
                
        """
        return self._one_way_jitter

    @one_way_jitter.setter
    def one_way_jitter(self, value):
        """ Set one_way_jitter value.

            Notes:
                one way Jitter

                
                This attribute is named `oneWayJitter` in VSD API.
                
        """
        self._one_way_jitter = value

    
    @property
    def one_way_loss(self):
        """ Get one_way_loss value.

            Notes:
                one way loss

                
                This attribute is named `oneWayLoss` in VSD API.
                
        """
        return self._one_way_loss

    @one_way_loss.setter
    def one_way_loss(self, value):
        """ Set one_way_loss value.

            Notes:
                one way loss

                
                This attribute is named `oneWayLoss` in VSD API.
                
        """
        self._one_way_loss = value

    
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
    def post_classification_path(self):
        """ Get post_classification_path value.

            Notes:
                default set to any , possible values primary/secondary/any

                
                This attribute is named `postClassificationPath` in VSD API.
                
        """
        return self._post_classification_path

    @post_classification_path.setter
    def post_classification_path(self, value):
        """ Set post_classification_path value.

            Notes:
                default set to any , possible values primary/secondary/any

                
                This attribute is named `postClassificationPath` in VSD API.
                
        """
        self._post_classification_path = value

    
    @property
    def source_ip(self):
        """ Get source_ip value.

            Notes:
                source IP address

                
                This attribute is named `sourceIP` in VSD API.
                
        """
        return self._source_ip

    @source_ip.setter
    def source_ip(self, value):
        """ Set source_ip value.

            Notes:
                source IP address

                
                This attribute is named `sourceIP` in VSD API.
                
        """
        self._source_ip = value

    
    @property
    def source_port(self):
        """ Get source_port value.

            Notes:
                source Port ,value should be either * or single port number or maximum 5 ranges comma separated.

                
                This attribute is named `sourcePort` in VSD API.
                
        """
        return self._source_port

    @source_port.setter
    def source_port(self, value):
        """ Set source_port value.

            Notes:
                source Port ,value should be either * or single port number or maximum 5 ranges comma separated.

                
                This attribute is named `sourcePort` in VSD API.
                
        """
        self._source_port = value

    
    @property
    def app_id(self):
        """ Get app_id value.

            Notes:
                a unique 2 byte id generated when a application is created and used by VRS  for probing.

                
                This attribute is named `appId` in VSD API.
                
        """
        return self._app_id

    @app_id.setter
    def app_id(self, value):
        """ Set app_id value.

            Notes:
                a unique 2 byte id generated when a application is created and used by VRS  for probing.

                
                This attribute is named `appId` in VSD API.
                
        """
        self._app_id = value

    
    @property
    def optimize_path_selection(self):
        """ Get optimize_path_selection value.

            Notes:
                with values being Latency, Jitter, PacketLoss

                
                This attribute is named `optimizePathSelection` in VSD API.
                
        """
        return self._optimize_path_selection

    @optimize_path_selection.setter
    def optimize_path_selection(self, value):
        """ Set optimize_path_selection value.

            Notes:
                with values being Latency, Jitter, PacketLoss

                
                This attribute is named `optimizePathSelection` in VSD API.
                
        """
        self._optimize_path_selection = value

    
    @property
    def pre_classification_path(self):
        """ Get pre_classification_path value.

            Notes:
                default set to primary , possible values primary/secondary

                
                This attribute is named `preClassificationPath` in VSD API.
                
        """
        return self._pre_classification_path

    @pre_classification_path.setter
    def pre_classification_path(self, value):
        """ Set pre_classification_path value.

            Notes:
                default set to primary , possible values primary/secondary

                
                This attribute is named `preClassificationPath` in VSD API.
                
        """
        self._pre_classification_path = value

    
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
    def protocol(self):
        """ Get protocol value.

            Notes:
                Protocol number that must be matched

                
        """
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """ Set protocol value.

            Notes:
                Protocol number that must be matched

                
        """
        self._protocol = value

    
    @property
    def associated_l7_application_signature_id(self):
        """ Get associated_l7_application_signature_id value.

            Notes:
                associated Layer7 Application Type ID

                
                This attribute is named `associatedL7ApplicationSignatureID` in VSD API.
                
        """
        return self._associated_l7_application_signature_id

    @associated_l7_application_signature_id.setter
    def associated_l7_application_signature_id(self, value):
        """ Set associated_l7_application_signature_id value.

            Notes:
                associated Layer7 Application Type ID

                
                This attribute is named `associatedL7ApplicationSignatureID` in VSD API.
                
        """
        self._associated_l7_application_signature_id = value

    
    @property
    def ether_type(self):
        """ Get ether_type value.

            Notes:
                Ether type of the packet to be matched. etherType can be * or a valid hexadecimal value

                
                This attribute is named `etherType` in VSD API.
                
        """
        return self._ether_type

    @ether_type.setter
    def ether_type(self, value):
        """ Set ether_type value.

            Notes:
                Ether type of the packet to be matched. etherType can be * or a valid hexadecimal value

                
                This attribute is named `etherType` in VSD API.
                
        """
        self._ether_type = value

    
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

    
    @property
    def symmetry(self):
        """ Get symmetry value.

            Notes:
                Maintain path symmetry during SLA violation

                
        """
        return self._symmetry

    @symmetry.setter
    def symmetry(self, value):
        """ Set symmetry value.

            Notes:
                Maintain path symmetry during SLA violation

                
        """
        self._symmetry = value

    

    