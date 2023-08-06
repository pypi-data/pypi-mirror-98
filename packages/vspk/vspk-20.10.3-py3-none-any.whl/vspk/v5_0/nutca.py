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


from .fetchers import NUAlarmsFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUTCA(NURESTObject):
    """ Represents a TCA in the VSD

        Notes:
            Provides the definition of the Threshold Control Alarms.
    """

    __rest_name__ = "tca"
    __resource_name__ = "tcas"

    
    ## Constants
    
    CONST_METRIC_PACKETS_OUT_DROPPED = "PACKETS_OUT_DROPPED"
    
    CONST_METRIC_Q4_BYTES = "Q4_BYTES"
    
    CONST_METRIC_FIP_RATE_LIMIT_DROPPED_PACKETS = "FIP_RATE_LIMIT_DROPPED_PACKETS"
    
    CONST_METRIC_TX_ERRORS = "TX_ERRORS"
    
    CONST_METRIC_RX_BYTES = "RX_BYTES"
    
    CONST_TYPE_BREACH = "BREACH"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_METRIC_TCP_FLAG_RST_IN = "TCP_FLAG_RST_IN"
    
    CONST_METRIC_RX_DROPPED = "RX_DROPPED"
    
    CONST_METRIC_Q3_PKT_COUNT = "Q3_PKT_COUNT"
    
    CONST_METRIC_TCP_FLAG_ACK_OUT = "TCP_FLAG_ACK_OUT"
    
    CONST_METRIC_TCP_FLAG_ACK_IN = "TCP_FLAG_ACK_IN"
    
    CONST_METRIC_EGRESS_PACKET_COUNT = "EGRESS_PACKET_COUNT"
    
    CONST_METRIC_Q2_DROPPED = "Q2_DROPPED"
    
    CONST_METRIC_PACKETS_IN_DROPPED = "PACKETS_IN_DROPPED"
    
    CONST_METRIC_L7_BYTES_OUT = "L7_BYTES_OUT"
    
    CONST_TYPE_ROLLING_AVERAGE = "ROLLING_AVERAGE"
    
    CONST_METRIC_FIP_RATE_LIMIT_DROPPED_BYTES = "FIP_RATE_LIMIT_DROPPED_BYTES"
    
    CONST_METRIC_PACKETS_DROPPED_BY_RATE_LIMIT = "PACKETS_DROPPED_BY_RATE_LIMIT"
    
    CONST_METRIC_Q1_BYTES = "Q1_BYTES"
    
    CONST_METRIC_Q3_BYTES = "Q3_BYTES"
    
    CONST_METRIC_EGRESS_BYTE_COUNT = "EGRESS_BYTE_COUNT"
    
    CONST_METRIC_INGRESS_PACKET_COUNT = "INGRESS_PACKET_COUNT"
    
    CONST_METRIC_TX_DROPPED = "TX_DROPPED"
    
    CONST_METRIC_Q1_DROPPED = "Q1_DROPPED"
    
    CONST_METRIC_ADDRESS_MAP_INGRESS_BYTE_CNT = "ADDRESS_MAP_INGRESS_BYTE_CNT"
    
    CONST_METRIC_PACKETS_IN = "PACKETS_IN"
    
    CONST_METRIC_Q2_PKT_COUNT = "Q2_PKT_COUNT"
    
    CONST_METRIC_RX_PKT_COUNT = "RX_PKT_COUNT"
    
    CONST_METRIC_TX_BYTES = "TX_BYTES"
    
    CONST_METRIC_ANTI_SPOOF_EVENT_COUNT = "ANTI_SPOOF_EVENT_COUNT"
    
    CONST_METRIC_ACL_DENY_EVENT_COUNT = "ACL_DENY_EVENT_COUNT"
    
    CONST_METRIC_TCP_FLAG_NULL_IN = "TCP_FLAG_NULL_IN"
    
    CONST_METRIC_Q3_DROPPED = "Q3_DROPPED"
    
    CONST_METRIC_TCP_FLAG_NULL_OUT = "TCP_FLAG_NULL_OUT"
    
    CONST_METRIC_Q10_BYTES = "Q10_BYTES"
    
    CONST_METRIC_BYTES_IN = "BYTES_IN"
    
    CONST_METRIC_Q10_PKT_COUNT = "Q10_PKT_COUNT"
    
    CONST_METRIC_FIP_PRE_RATE_LIMIT_BYTES = "FIP_PRE_RATE_LIMIT_BYTES"
    
    CONST_METRIC_Q4_PKT_COUNT = "Q4_PKT_COUNT"
    
    CONST_METRIC_ADDRESS_MAP_EGRESS_BYTE_CNT = "ADDRESS_MAP_EGRESS_BYTE_CNT"
    
    CONST_METRIC_INGRESS_BYTE_COUNT = "INGRESS_BYTE_COUNT"
    
    CONST_ACTION_ALERT_POLICYGROUPCHANGE = "Alert_PolicyGroupChange"
    
    CONST_METRIC_PACKETS_IN_ERROR = "PACKETS_IN_ERROR"
    
    CONST_METRIC_TX_PKT_COUNT = "TX_PKT_COUNT"
    
    CONST_METRIC_TCP_FLAG_RST_OUT = "TCP_FLAG_RST_OUT"
    
    CONST_METRIC_Q1_PKT_COUNT = "Q1_PKT_COUNT"
    
    CONST_METRIC_ADDRESS_MAP_EGRESS_PKT_CNT = "ADDRESS_MAP_EGRESS_PKT_CNT"
    
    CONST_METRIC_ADDRESS_MAP_INGRESS_PKT_CNT = "ADDRESS_MAP_INGRESS_PKT_CNT"
    
    CONST_METRIC_RX_ERRORS = "RX_ERRORS"
    
    CONST_METRIC_Q0_BYTES = "Q0_BYTES"
    
    CONST_METRIC_PACKETS_OUT_ERROR = "PACKETS_OUT_ERROR"
    
    CONST_METRIC_BYTES_OUT = "BYTES_OUT"
    
    CONST_METRIC_L7_PACKETS_OUT = "L7_PACKETS_OUT"
    
    CONST_METRIC_Q0_PKT_COUNT = "Q0_PKT_COUNT"
    
    CONST_METRIC_L7_BYTES_IN = "L7_BYTES_IN"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_METRIC_TCP_FLAG_SYN_OUT = "TCP_FLAG_SYN_OUT"
    
    CONST_METRIC_PACKETS_OUT = "PACKETS_OUT"
    
    CONST_METRIC_Q10_DROPPED = "Q10_DROPPED"
    
    CONST_METRIC_Q4_DROPPED = "Q4_DROPPED"
    
    CONST_METRIC_CONNECTION_TYPE = "CONNECTION_TYPE"
    
    CONST_METRIC_Q2_BYTES = "Q2_BYTES"
    
    CONST_METRIC_FIP_PRE_RATE_LIMIT_PACKETS = "FIP_PRE_RATE_LIMIT_PACKETS"
    
    CONST_ACTION_ALERT = "Alert"
    
    CONST_METRIC_TCP_FLAG_SYN_IN = "TCP_FLAG_SYN_IN"
    
    CONST_METRIC_Q0_DROPPED = "Q0_DROPPED"
    
    CONST_METRIC_TCP_SYN_EVENT_COUNT = "TCP_SYN_EVENT_COUNT"
    
    CONST_METRIC_L7_PACKETS_IN = "L7_PACKETS_IN"
    
    

    def __init__(self, **kwargs):
        """ Initializes a TCA instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> tca = NUTCA(id=u'xxxx-xxx-xxx-xxx', name=u'TCA')
                >>> tca = NUTCA(data=my_dict)
        """

        super(NUTCA, self).__init__()

        # Read/Write Attributes
        
        self._url_end_point = None
        self._name = None
        self._target_policy_group_id = None
        self._last_updated_by = None
        self._action = None
        self._period = None
        self._description = None
        self._metric = None
        self._threshold = None
        self._throttle_time = None
        self._disable = None
        self._display_status = None
        self._entity_scope = None
        self._count = None
        self._status = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="url_end_point", remote_name="URLEndPoint", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="target_policy_group_id", remote_name="targetPolicyGroupID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="action", remote_name="action", attribute_type=str, is_required=True, is_unique=False, choices=[u'Alert', u'Alert_PolicyGroupChange'])
        self.expose_attribute(local_name="period", remote_name="period", attribute_type=int, is_required=True, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="metric", remote_name="metric", attribute_type=str, is_required=True, is_unique=False, choices=[u'ACL_DENY_EVENT_COUNT', u'ADDRESS_MAP_EGRESS_BYTE_CNT', u'ADDRESS_MAP_EGRESS_PKT_CNT', u'ADDRESS_MAP_INGRESS_BYTE_CNT', u'ADDRESS_MAP_INGRESS_PKT_CNT', u'ANTI_SPOOF_EVENT_COUNT', u'BYTES_IN', u'BYTES_OUT', u'CONNECTION_TYPE', u'EGRESS_BYTE_COUNT', u'EGRESS_PACKET_COUNT', u'FIP_PRE_RATE_LIMIT_BYTES', u'FIP_PRE_RATE_LIMIT_PACKETS', u'FIP_RATE_LIMIT_DROPPED_BYTES', u'FIP_RATE_LIMIT_DROPPED_PACKETS', u'INGRESS_BYTE_COUNT', u'INGRESS_PACKET_COUNT', u'L7_BYTES_IN', u'L7_BYTES_OUT', u'L7_PACKETS_IN', u'L7_PACKETS_OUT', u'PACKETS_DROPPED_BY_RATE_LIMIT', u'PACKETS_IN', u'PACKETS_IN_DROPPED', u'PACKETS_IN_ERROR', u'PACKETS_OUT', u'PACKETS_OUT_DROPPED', u'PACKETS_OUT_ERROR', u'Q0_BYTES', u'Q0_DROPPED', u'Q0_PKT_COUNT', u'Q10_BYTES', u'Q10_DROPPED', u'Q10_PKT_COUNT', u'Q1_BYTES', u'Q1_DROPPED', u'Q1_PKT_COUNT', u'Q2_BYTES', u'Q2_DROPPED', u'Q2_PKT_COUNT', u'Q3_BYTES', u'Q3_DROPPED', u'Q3_PKT_COUNT', u'Q4_BYTES', u'Q4_DROPPED', u'Q4_PKT_COUNT', u'RX_BYTES', u'RX_DROPPED', u'RX_ERRORS', u'RX_PKT_COUNT', u'TCP_FLAG_ACK_IN', u'TCP_FLAG_ACK_OUT', u'TCP_FLAG_NULL_IN', u'TCP_FLAG_NULL_OUT', u'TCP_FLAG_RST_IN', u'TCP_FLAG_RST_OUT', u'TCP_FLAG_SYN_IN', u'TCP_FLAG_SYN_OUT', u'TCP_SYN_EVENT_COUNT', u'TX_BYTES', u'TX_DROPPED', u'TX_ERRORS', u'TX_PKT_COUNT'])
        self.expose_attribute(local_name="threshold", remote_name="threshold", attribute_type=int, is_required=True, is_unique=False)
        self.expose_attribute(local_name="throttle_time", remote_name="throttleTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="disable", remote_name="disable", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="display_status", remote_name="displayStatus", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="count", remote_name="count", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="status", remote_name="status", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=True, is_unique=False, choices=[u'BREACH', u'ROLLING_AVERAGE'])
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.alarms = NUAlarmsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def url_end_point(self):
        """ Get url_end_point value.

            Notes:
                URL endpoint to post Alarm data to when TCA is triggered

                
                This attribute is named `URLEndPoint` in VSD API.
                
        """
        return self._url_end_point

    @url_end_point.setter
    def url_end_point(self, value):
        """ Set url_end_point value.

            Notes:
                URL endpoint to post Alarm data to when TCA is triggered

                
                This attribute is named `URLEndPoint` in VSD API.
                
        """
        self._url_end_point = value

    
    @property
    def name(self):
        """ Get name value.

            Notes:
                The name of the TCA

                
        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                The name of the TCA

                
        """
        self._name = value

    
    @property
    def target_policy_group_id(self):
        """ Get target_policy_group_id value.

            Notes:
                Target policygroup when TCA is triggered

                
                This attribute is named `targetPolicyGroupID` in VSD API.
                
        """
        return self._target_policy_group_id

    @target_policy_group_id.setter
    def target_policy_group_id(self, value):
        """ Set target_policy_group_id value.

            Notes:
                Target policygroup when TCA is triggered

                
                This attribute is named `targetPolicyGroupID` in VSD API.
                
        """
        self._target_policy_group_id = value

    
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
    def action(self):
        """ Get action value.

            Notes:
                Action to be taken when TCA is fired - Alert or PolicyGroupChange

                
        """
        return self._action

    @action.setter
    def action(self, value):
        """ Set action value.

            Notes:
                Action to be taken when TCA is fired - Alert or PolicyGroupChange

                
        """
        self._action = value

    
    @property
    def period(self):
        """ Get period value.

            Notes:
                The averaging period

                
        """
        return self._period

    @period.setter
    def period(self, value):
        """ Set period value.

            Notes:
                The averaging period

                
        """
        self._period = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Description of the TCA

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Description of the TCA

                
        """
        self._description = value

    
    @property
    def metric(self):
        """ Get metric value.

            Notes:
                The metric associated with the TCA. The following enum values have been deprecated and will be removed in the next major release 6.0: ADDRESS_MAP_EGRESS_BYTE_CNT, ADDRESS_MAP_EGRESS_PKT_CNT, ADDRESS_MAP_INGRESS_BYTE_CNT, ADDRESS_MAP_INGRESS_PKT_CNT, CONNECTION_TYPE, EGRESS_BYTE_COUNT, EGRESS_PACKET_COUNT, INGRESS_BYTE_COUNT, INGRESS_PACKET_COUNT, Q0_BYTES, Q0_DROPPED, Q0_PKT_COUNT, Q10_BYTES, Q10_DROPPED, Q10_PKT_COUNT, Q1_BYTES, Q1_DROPPED, Q1_PKT_COUNT, Q2_BYTES, Q2_DROPPED, Q2_PKT_COUNT, Q3_BYTES, Q3_DROPPED, Q3_PKT_COUNT, Q4_BYTES, Q4_DROPPED, Q4_PKT_COUNT, RX_BYTES, RX_DROPPED, RX_ERRORS, RX_PKT_COUNT, TCP_SYN_EVENT_COUNT, TX_BYTES, TX_DROPPED, TX_ERRORS, TX_PKT_COUNT

                
        """
        return self._metric

    @metric.setter
    def metric(self, value):
        """ Set metric value.

            Notes:
                The metric associated with the TCA. The following enum values have been deprecated and will be removed in the next major release 6.0: ADDRESS_MAP_EGRESS_BYTE_CNT, ADDRESS_MAP_EGRESS_PKT_CNT, ADDRESS_MAP_INGRESS_BYTE_CNT, ADDRESS_MAP_INGRESS_PKT_CNT, CONNECTION_TYPE, EGRESS_BYTE_COUNT, EGRESS_PACKET_COUNT, INGRESS_BYTE_COUNT, INGRESS_PACKET_COUNT, Q0_BYTES, Q0_DROPPED, Q0_PKT_COUNT, Q10_BYTES, Q10_DROPPED, Q10_PKT_COUNT, Q1_BYTES, Q1_DROPPED, Q1_PKT_COUNT, Q2_BYTES, Q2_DROPPED, Q2_PKT_COUNT, Q3_BYTES, Q3_DROPPED, Q3_PKT_COUNT, Q4_BYTES, Q4_DROPPED, Q4_PKT_COUNT, RX_BYTES, RX_DROPPED, RX_ERRORS, RX_PKT_COUNT, TCP_SYN_EVENT_COUNT, TX_BYTES, TX_DROPPED, TX_ERRORS, TX_PKT_COUNT

                
        """
        self._metric = value

    
    @property
    def threshold(self):
        """ Get threshold value.

            Notes:
                The threshold that must be exceeded before an alarm is issued

                
        """
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        """ Set threshold value.

            Notes:
                The threshold that must be exceeded before an alarm is issued

                
        """
        self._threshold = value

    
    @property
    def throttle_time(self):
        """ Get throttle_time value.

            Notes:
                Throttle time in secs

                
                This attribute is named `throttleTime` in VSD API.
                
        """
        return self._throttle_time

    @throttle_time.setter
    def throttle_time(self, value):
        """ Set throttle_time value.

            Notes:
                Throttle time in secs

                
                This attribute is named `throttleTime` in VSD API.
                
        """
        self._throttle_time = value

    
    @property
    def disable(self):
        """ Get disable value.

            Notes:
                This flag is used to indicate whether the watch(TCA) is enabled/disabled

                
        """
        return self._disable

    @disable.setter
    def disable(self, value):
        """ Set disable value.

            Notes:
                This flag is used to indicate whether the watch(TCA) is enabled/disabled

                
        """
        self._disable = value

    
    @property
    def display_status(self):
        """ Get display_status value.

            Notes:
                Explanation of the TCA status

                
                This attribute is named `displayStatus` in VSD API.
                
        """
        return self._display_status

    @display_status.setter
    def display_status(self, value):
        """ Set display_status value.

            Notes:
                Explanation of the TCA status

                
                This attribute is named `displayStatus` in VSD API.
                
        """
        self._display_status = value

    
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
    def count(self):
        """ Get count value.

            Notes:
                Count of the attempts by maintenanace thread to create/update watcher

                
        """
        return self._count

    @count.setter
    def count(self, value):
        """ Set count value.

            Notes:
                Count of the attempts by maintenanace thread to create/update watcher

                
        """
        self._count = value

    
    @property
    def status(self):
        """ Get status value.

            Notes:
                This flag is used to indicate the status of TCA

                
        """
        return self._status

    @status.setter
    def status(self, value):
        """ Set status value.

            Notes:
                This flag is used to indicate the status of TCA

                
        """
        self._status = value

    
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
    def type(self):
        """ Get type value.

            Notes:
                Rolling average or sequence of samples over the averaging period.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                Rolling average or sequence of samples over the averaging period.

                
        """
        self._type = value

    

    