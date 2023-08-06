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


class NUAlarm(NURESTObject):
    """ Represents a Alarm in the VSD

        Notes:
            The alarm API allows the management of system alarms.
    """

    __rest_name__ = "alarm"
    __resource_name__ = "alarms"

    
    ## Constants
    
    CONST_SEVERITY_WARNING = "WARNING"
    
    CONST_SEVERITY_MAJOR = "MAJOR"
    
    CONST_SEVERITY_CRITICAL = "CRITICAL"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_SEVERITY_INFO = "INFO"
    
    CONST_SEVERITY_MINOR = "MINOR"
    
    

    def __init__(self, **kwargs):
        """ Initializes a Alarm instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> alarm = NUAlarm(id=u'xxxx-xxx-xxx-xxx', name=u'Alarm')
                >>> alarm = NUAlarm(data=my_dict)
        """

        super(NUAlarm, self).__init__()

        # Read/Write Attributes
        
        self._target_object = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._acknowledged = None
        self._remedy = None
        self._description = None
        self._severity = None
        self._timestamp = None
        self._title = None
        self._alarmed_object_id = None
        self._embedded_metadata = None
        self._enterprise_id = None
        self._entity_scope = None
        self._creation_date = None
        self._error_condition = None
        self._number_of_occurances = None
        self._owner = None
        self._external_id = None
        self._system_id = None
        
        self.expose_attribute(local_name="target_object", remote_name="targetObject", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="acknowledged", remote_name="acknowledged", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="remedy", remote_name="remedy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="severity", remote_name="severity", attribute_type=str, is_required=False, is_unique=False, choices=[u'CRITICAL', u'INFO', u'MAJOR', u'MINOR', u'WARNING'])
        self.expose_attribute(local_name="timestamp", remote_name="timestamp", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="title", remote_name="title", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="alarmed_object_id", remote_name="alarmedObjectID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="enterprise_id", remote_name="enterpriseID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="error_condition", remote_name="errorCondition", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="number_of_occurances", remote_name="numberOfOccurances", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="system_id", remote_name="systemID", attribute_type=str, is_required=False, is_unique=False)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def target_object(self):
        """ Get target_object value.

            Notes:
                Identifies affected Entity.  Example: Alarm generated by TCA for Domain domain1(Packets towards a VM, Breach)

                
                This attribute is named `targetObject` in VSD API.
                
        """
        return self._target_object

    @target_object.setter
    def target_object(self, value):
        """ Set target_object value.

            Notes:
                Identifies affected Entity.  Example: Alarm generated by TCA for Domain domain1(Packets towards a VM, Breach)

                
                This attribute is named `targetObject` in VSD API.
                
        """
        self._target_object = value

    
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
    def acknowledged(self):
        """ Get acknowledged value.

            Notes:
                Flag to indicate if the alarm has been acknowledged already.

                
        """
        return self._acknowledged

    @acknowledged.setter
    def acknowledged(self, value):
        """ Set acknowledged value.

            Notes:
                Flag to indicate if the alarm has been acknowledged already.

                
        """
        self._acknowledged = value

    
    @property
    def remedy(self):
        """ Get remedy value.

            Notes:
                Remedial Actions for the alarm.

                
        """
        return self._remedy

    @remedy.setter
    def remedy(self, value):
        """ Set remedy value.

            Notes:
                Remedial Actions for the alarm.

                
        """
        self._remedy = value

    
    @property
    def description(self):
        """ Get description value.

            Notes:
                Description of the alarm

                
        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                Description of the alarm

                
        """
        self._description = value

    
    @property
    def severity(self):
        """ Get severity value.

            Notes:
                Severity of the alarm.

                
        """
        return self._severity

    @severity.setter
    def severity(self, value):
        """ Set severity value.

            Notes:
                Severity of the alarm.

                
        """
        self._severity = value

    
    @property
    def timestamp(self):
        """ Get timestamp value.

            Notes:
                Indicates the time at which the alarm was triggered

                
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        """ Set timestamp value.

            Notes:
                Indicates the time at which the alarm was triggered

                
        """
        self._timestamp = value

    
    @property
    def title(self):
        """ Get title value.

            Notes:
                The alarm title.  Each type of alarm will generate its own title

                
        """
        return self._title

    @title.setter
    def title(self, value):
        """ Set title value.

            Notes:
                The alarm title.  Each type of alarm will generate its own title

                
        """
        self._title = value

    
    @property
    def alarmed_object_id(self):
        """ Get alarmed_object_id value.

            Notes:
                Alarmed Object ID

                
                This attribute is named `alarmedObjectID` in VSD API.
                
        """
        return self._alarmed_object_id

    @alarmed_object_id.setter
    def alarmed_object_id(self, value):
        """ Set alarmed_object_id value.

            Notes:
                Alarmed Object ID

                
                This attribute is named `alarmedObjectID` in VSD API.
                
        """
        self._alarmed_object_id = value

    
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
    def enterprise_id(self):
        """ Get enterprise_id value.

            Notes:
                Enterprise that this alarm belongs to

                
                This attribute is named `enterpriseID` in VSD API.
                
        """
        return self._enterprise_id

    @enterprise_id.setter
    def enterprise_id(self, value):
        """ Set enterprise_id value.

            Notes:
                Enterprise that this alarm belongs to

                
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
    def error_condition(self):
        """ Get error_condition value.

            Notes:
                Identifies the error condition

                
                This attribute is named `errorCondition` in VSD API.
                
        """
        return self._error_condition

    @error_condition.setter
    def error_condition(self, value):
        """ Set error_condition value.

            Notes:
                Identifies the error condition

                
                This attribute is named `errorCondition` in VSD API.
                
        """
        self._error_condition = value

    
    @property
    def number_of_occurances(self):
        """ Get number_of_occurances value.

            Notes:
                Number of times that the alarm was triggered

                
                This attribute is named `numberOfOccurances` in VSD API.
                
        """
        return self._number_of_occurances

    @number_of_occurances.setter
    def number_of_occurances(self, value):
        """ Set number_of_occurances value.

            Notes:
                Number of times that the alarm was triggered

                
                This attribute is named `numberOfOccurances` in VSD API.
                
        """
        self._number_of_occurances = value

    
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
    def system_id(self):
        """ Get system_id value.

            Notes:
                System ID of the Gateway

                
                This attribute is named `systemID` in VSD API.
                
        """
        return self._system_id

    @system_id.setter
    def system_id(self, value):
        """ Set system_id value.

            Notes:
                System ID of the Gateway

                
                This attribute is named `systemID` in VSD API.
                
        """
        self._system_id = value

    

    