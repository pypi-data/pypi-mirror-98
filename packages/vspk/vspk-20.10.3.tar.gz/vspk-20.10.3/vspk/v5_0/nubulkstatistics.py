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


class NUBulkStatistics(NURESTObject):
    """ Represents a BulkStatistics in the VSD

        Notes:
            Retrieves the statistics for a particular Entity and its immediate child entity.
    """

    __rest_name__ = "bulkstatistics"
    __resource_name__ = "bulkstatistics"

    

    def __init__(self, **kwargs):
        """ Initializes a BulkStatistics instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> bulkstatistics = NUBulkStatistics(id=u'xxxx-xxx-xxx-xxx', name=u'BulkStatistics')
                >>> bulkstatistics = NUBulkStatistics(data=my_dict)
        """

        super(NUBulkStatistics, self).__init__()

        # Read/Write Attributes
        
        self._data = None
        self._version = None
        self._end_time = None
        self._start_time = None
        self._number_of_data_points = None
        
        self.expose_attribute(local_name="data", remote_name="data", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="version", remote_name="version", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="end_time", remote_name="endTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="start_time", remote_name="startTime", attribute_type=int, is_required=False, is_unique=False)
        self.expose_attribute(local_name="number_of_data_points", remote_name="numberOfDataPoints", attribute_type=int, is_required=False, is_unique=False)
        

        # Fetchers
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def data(self):
        """ Get data value.

            Notes:
                Map<TCAMetric, Long> TCAMetric is an Enum. Possible values are packets_in, bytes_in, packets_in_dropped, packets_in_errors, packets_out, bytes_out, packets_out_dropped, packeMaprs, packets_dropped_rate_limit

                
        """
        return self._data

    @data.setter
    def data(self, value):
        """ Set data value.

            Notes:
                Map<TCAMetric, Long> TCAMetric is an Enum. Possible values are packets_in, bytes_in, packets_in_dropped, packets_in_errors, packets_out, bytes_out, packets_out_dropped, packeMaprs, packets_dropped_rate_limit

                
        """
        self._data = value

    
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

    

    