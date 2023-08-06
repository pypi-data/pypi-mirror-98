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


class NUStatistics(NURESTObject):
    """ Represents a Statistics in the VSD

        Notes:
            Retrieves the statistics for a particular domain, zone, subnet, or VM.
    """

    __rest_name__ = "statistics"
    __resource_name__ = "statistics"

    

    def __init__(self, **kwargs):
        """ Initializes a Statistics instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> statistics = NUStatistics(id=u'xxxx-xxx-xxx-xxx', name=u'Statistics')
                >>> statistics = NUStatistics(data=my_dict)
        """

        super(NUStatistics, self).__init__()

        # Read/Write Attributes
        
        self._version = None
        self._embedded_metadata = None
        self._end_time = None
        self._start_time = None
        self._stats_data = None
        self._number_of_data_points = None
        
        self.expose_attribute(local_name="version", remote_name="version", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="end_time", remote_name="endTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="start_time", remote_name="startTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="stats_data", remote_name="statsData", attribute_type=dict, is_required=False, is_unique=False)
        self.expose_attribute(local_name="number_of_data_points", remote_name="numberOfDataPoints", attribute_type=int, is_required=False, is_unique=False)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def version(self):
        """ Get version value.

            Notes:
                Version of this Sequence number.

                
        """
        return self._version

    @version.setter
    def version(self, value):
        """ Set version value.

            Notes:
                Version of this Sequence number.

                
        """
        self._version = value

    
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
    def end_time(self):
        """ Get end_time value.

            Notes:
                End time for the statistics to be retrieved

                
                This attribute is named `endTime` in VSD API.
                
        """
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        """ Set end_time value.

            Notes:
                End time for the statistics to be retrieved

                
                This attribute is named `endTime` in VSD API.
                
        """
        self._end_time = value

    
    @property
    def start_time(self):
        """ Get start_time value.

            Notes:
                Start time for the statistics to be retrieved

                
                This attribute is named `startTime` in VSD API.
                
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """ Set start_time value.

            Notes:
                Start time for the statistics to be retrieved

                
                This attribute is named `startTime` in VSD API.
                
        """
        self._start_time = value

    
    @property
    def stats_data(self):
        """ Get stats_data value.

            Notes:
                Contains the requested statistics data. Possible values are PACKETS_IN, BYTES_IN, PACKETS_IN_DROPPED, PACKETS_IN_ERRORS, PACKETS_OUT, BYTES_OUT, PACKETS_OUT_DROPPED, PACKETS_OUT_ERRORS, PACKETS_DROPPED_RATE_LIMIT, DISKS, MEMORY, CPU

                
                This attribute is named `statsData` in VSD API.
                
        """
        return self._stats_data

    @stats_data.setter
    def stats_data(self, value):
        """ Set stats_data value.

            Notes:
                Contains the requested statistics data. Possible values are PACKETS_IN, BYTES_IN, PACKETS_IN_DROPPED, PACKETS_IN_ERRORS, PACKETS_OUT, BYTES_OUT, PACKETS_OUT_DROPPED, PACKETS_OUT_ERRORS, PACKETS_DROPPED_RATE_LIMIT, DISKS, MEMORY, CPU

                
                This attribute is named `statsData` in VSD API.
                
        """
        self._stats_data = value

    
    @property
    def number_of_data_points(self):
        """ Get number_of_data_points value.

            Notes:
                Number of data points between start time and end time

                
                This attribute is named `numberOfDataPoints` in VSD API.
                
        """
        return self._number_of_data_points

    @number_of_data_points.setter
    def number_of_data_points(self, value):
        """ Set number_of_data_points value.

            Notes:
                Number of data points between start time and end time

                
                This attribute is named `numberOfDataPoints` in VSD API.
                
        """
        self._number_of_data_points = value

    

    