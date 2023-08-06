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




from .fetchers import NUDeploymentFailuresFetcher


from .fetchers import NUMetadatasFetcher


from .fetchers import NUGlobalMetadatasFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUStaticRoute(NURESTObject):
    """ Represents a StaticRoute in the VSD

        Notes:
            Static routes allow end users to define how traffic is routed through the dVRS in addition to the routes learned by VSC through VM activation. By using static routes, end users can define for example that all traffic with a destination address towards a specific subnet must be forwarded to a specific VM attached in the dVRS and this VM could be a firewall
    """

    __rest_name__ = "staticroute"
    __resource_name__ = "staticroutes"

    
    ## Constants
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_TYPE_OVERLAY_ADDRESS_TRANSLATION = "OVERLAY_ADDRESS_TRANSLATION"
    
    CONST_TYPE_OVERLAY = "OVERLAY"
    
    CONST_TYPE_NETCONF = "NETCONF"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_IP_TYPE_IPV6 = "IPV6"
    
    CONST_IP_TYPE_IPV4 = "IPV4"
    
    CONST_TYPE_EXIT_DOMAIN = "EXIT_DOMAIN"
    
    

    def __init__(self, **kwargs):
        """ Initializes a StaticRoute instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> staticroute = NUStaticRoute(id=u'xxxx-xxx-xxx-xxx', name=u'StaticRoute')
                >>> staticroute = NUStaticRoute(data=my_dict)
        """

        super(NUStaticRoute, self).__init__()

        # Read/Write Attributes
        
        self._bfd_enabled = None
        self._ip_type = None
        self._ipv6_address = None
        self._last_updated_by = None
        self._address = None
        self._netmask = None
        self._next_hop_ip = None
        self._black_hole_enabled = None
        self._entity_scope = None
        self._route_distinguisher = None
        self._associated_gateway_ids = None
        self._associated_subnet_id = None
        self._external_id = None
        self._type = None
        
        self.expose_attribute(local_name="bfd_enabled", remote_name="BFDEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="ip_type", remote_name="IPType", attribute_type=str, is_required=False, is_unique=False, choices=[u'IPV4', u'IPV6'])
        self.expose_attribute(local_name="ipv6_address", remote_name="IPv6Address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="address", remote_name="address", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="netmask", remote_name="netmask", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="next_hop_ip", remote_name="nextHopIp", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="black_hole_enabled", remote_name="blackHoleEnabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="route_distinguisher", remote_name="routeDistinguisher", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_gateway_ids", remote_name="associatedGatewayIDs", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="associated_subnet_id", remote_name="associatedSubnetID", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        self.expose_attribute(local_name="type", remote_name="type", attribute_type=str, is_required=False, is_unique=False, choices=[u'EXIT_DOMAIN', u'NETCONF', u'OVERLAY', u'OVERLAY_ADDRESS_TRANSLATION'])
        

        # Fetchers
        
        
        self.deployment_failures = NUDeploymentFailuresFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def bfd_enabled(self):
        """ Get bfd_enabled value.

            Notes:
                Enable or disable Bidirectional Forwarding Detection for this static route

                
                This attribute is named `BFDEnabled` in VSD API.
                
        """
        return self._bfd_enabled

    @bfd_enabled.setter
    def bfd_enabled(self, value):
        """ Set bfd_enabled value.

            Notes:
                Enable or disable Bidirectional Forwarding Detection for this static route

                
                This attribute is named `BFDEnabled` in VSD API.
                
        """
        self._bfd_enabled = value

    
    @property
    def ip_type(self):
        """ Get ip_type value.

            Notes:
                IPv4 or IPv6

                
                This attribute is named `IPType` in VSD API.
                
        """
        return self._ip_type

    @ip_type.setter
    def ip_type(self, value):
        """ Set ip_type value.

            Notes:
                IPv4 or IPv6

                
                This attribute is named `IPType` in VSD API.
                
        """
        self._ip_type = value

    
    @property
    def ipv6_address(self):
        """ Get ipv6_address value.

            Notes:
                IPv6 address of the route

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        return self._ipv6_address

    @ipv6_address.setter
    def ipv6_address(self, value):
        """ Set ipv6_address value.

            Notes:
                IPv6 address of the route

                
                This attribute is named `IPv6Address` in VSD API.
                
        """
        self._ipv6_address = value

    
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
    def address(self):
        """ Get address value.

            Notes:
                IP address of the route

                
        """
        return self._address

    @address.setter
    def address(self, value):
        """ Set address value.

            Notes:
                IP address of the route

                
        """
        self._address = value

    
    @property
    def netmask(self):
        """ Get netmask value.

            Notes:
                Netmask associated with the route

                
        """
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        """ Set netmask value.

            Notes:
                Netmask associated with the route

                
        """
        self._netmask = value

    
    @property
    def next_hop_ip(self):
        """ Get next_hop_ip value.

            Notes:
                IP address of the next hop. This must be a VM attached to the dVRS

                
                This attribute is named `nextHopIp` in VSD API.
                
        """
        return self._next_hop_ip

    @next_hop_ip.setter
    def next_hop_ip(self, value):
        """ Set next_hop_ip value.

            Notes:
                IP address of the next hop. This must be a VM attached to the dVRS

                
                This attribute is named `nextHopIp` in VSD API.
                
        """
        self._next_hop_ip = value

    
    @property
    def black_hole_enabled(self):
        """ Get black_hole_enabled value.

            Notes:
                Indicates if this is a black hole static route. Applicable only when the static route type is 'NETCONF'.

                
                This attribute is named `blackHoleEnabled` in VSD API.
                
        """
        return self._black_hole_enabled

    @black_hole_enabled.setter
    def black_hole_enabled(self, value):
        """ Set black_hole_enabled value.

            Notes:
                Indicates if this is a black hole static route. Applicable only when the static route type is 'NETCONF'.

                
                This attribute is named `blackHoleEnabled` in VSD API.
                
        """
        self._black_hole_enabled = value

    
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
    def route_distinguisher(self):
        """ Get route_distinguisher value.

            Notes:
                Route distinguisher associated with the nexthop. System generates this identifier automatically

                
                This attribute is named `routeDistinguisher` in VSD API.
                
        """
        return self._route_distinguisher

    @route_distinguisher.setter
    def route_distinguisher(self, value):
        """ Set route_distinguisher value.

            Notes:
                Route distinguisher associated with the nexthop. System generates this identifier automatically

                
                This attribute is named `routeDistinguisher` in VSD API.
                
        """
        self._route_distinguisher = value

    
    @property
    def associated_gateway_ids(self):
        """ Get associated_gateway_ids value.

            Notes:
                List of associated gateway IDs for static route, returned as a JSON list of strings

                
                This attribute is named `associatedGatewayIDs` in VSD API.
                
        """
        return self._associated_gateway_ids

    @associated_gateway_ids.setter
    def associated_gateway_ids(self, value):
        """ Set associated_gateway_ids value.

            Notes:
                List of associated gateway IDs for static route, returned as a JSON list of strings

                
                This attribute is named `associatedGatewayIDs` in VSD API.
                
        """
        self._associated_gateway_ids = value

    
    @property
    def associated_subnet_id(self):
        """ Get associated_subnet_id value.

            Notes:
                UUID of Do Not Advertise Subnet

                
                This attribute is named `associatedSubnetID` in VSD API.
                
        """
        return self._associated_subnet_id

    @associated_subnet_id.setter
    def associated_subnet_id(self, value):
        """ Set associated_subnet_id value.

            Notes:
                UUID of Do Not Advertise Subnet

                
                This attribute is named `associatedSubnetID` in VSD API.
                
        """
        self._associated_subnet_id = value

    
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
                Type flag for static-route provisioning for exit-domain (break-to-underlay) prefixes.

                
        """
        return self._type

    @type.setter
    def type(self, value):
        """ Set type value.

            Notes:
                Type flag for static-route provisioning for exit-domain (break-to-underlay) prefixes.

                
        """
        self._type = value

    

    