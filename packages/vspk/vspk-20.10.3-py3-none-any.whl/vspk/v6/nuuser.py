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


from .fetchers import NUVMsFetcher


from .fetchers import NUContainersFetcher


from .fetchers import NUGroupsFetcher


from .fetchers import NUAvatarsFetcher


from .fetchers import NUEventLogsFetcher

from bambou import NURESTObject


class NUUser(NURESTObject):
    """ Represents a User in the VSD

        Notes:
            Users represent people of your organization. A user can be placed into a group and this group can have some permissions to add VMs into a domain for instance.
    """

    __rest_name__ = "user"
    __resource_name__ = "users"

    
    ## Constants
    
    CONST_MANAGEMENT_MODE_CMS = "CMS"
    
    CONST_ENTITY_SCOPE_GLOBAL = "GLOBAL"
    
    CONST_ENTITY_SCOPE_ENTERPRISE = "ENTERPRISE"
    
    CONST_AVATAR_TYPE_URL = "URL"
    
    CONST_AVATAR_TYPE_COMPUTEDURL = "COMPUTEDURL"
    
    CONST_AVATAR_TYPE_BASE64 = "BASE64"
    
    CONST_MANAGEMENT_MODE_DEFAULT = "DEFAULT"
    
    

    def __init__(self, **kwargs):
        """ Initializes a User instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> user = NUUser(id=u'xxxx-xxx-xxx-xxx', name=u'User')
                >>> user = NUUser(data=my_dict)
        """

        super(NUUser, self).__init__()

        # Read/Write Attributes
        
        self._ldapuser_dn = None
        self._management_mode = None
        self._password = None
        self._last_name = None
        self._last_updated_by = None
        self._last_updated_date = None
        self._first_name = None
        self._disable_certificate_auth = None
        self._disable_password_auth = None
        self._disabled = None
        self._email = None
        self._embedded_metadata = None
        self._entity_scope = None
        self._mobile_number = None
        self._creation_date = None
        self._user_name = None
        self._avatar_data = None
        self._avatar_type = None
        self._owner = None
        self._external_id = None
        
        self.expose_attribute(local_name="ldapuser_dn", remote_name="LDAPUserDN", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="management_mode", remote_name="managementMode", attribute_type=str, is_required=False, is_unique=False, choices=[u'CMS', u'DEFAULT'])
        self.expose_attribute(local_name="password", remote_name="password", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_name", remote_name="lastName", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="last_updated_by", remote_name="lastUpdatedBy", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="last_updated_date", remote_name="lastUpdatedDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="first_name", remote_name="firstName", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="disable_certificate_auth", remote_name="disableCertificateAuth", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="disable_password_auth", remote_name="disablePasswordAuth", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="disabled", remote_name="disabled", attribute_type=bool, is_required=False, is_unique=False)
        self.expose_attribute(local_name="email", remote_name="email", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="embedded_metadata", remote_name="embeddedMetadata", attribute_type=list, is_required=False, is_unique=False)
        self.expose_attribute(local_name="entity_scope", remote_name="entityScope", attribute_type=str, is_required=False, is_unique=False, choices=[u'ENTERPRISE', u'GLOBAL'])
        self.expose_attribute(local_name="mobile_number", remote_name="mobileNumber", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="creation_date", remote_name="creationDate", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="user_name", remote_name="userName", attribute_type=str, is_required=True, is_unique=False)
        self.expose_attribute(local_name="avatar_data", remote_name="avatarData", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="avatar_type", remote_name="avatarType", attribute_type=str, is_required=False, is_unique=False, choices=[u'BASE64', u'COMPUTEDURL', u'URL'])
        self.expose_attribute(local_name="owner", remote_name="owner", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="external_id", remote_name="externalID", attribute_type=str, is_required=False, is_unique=True)
        

        # Fetchers
        
        
        self.permissions = NUPermissionsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.metadatas = NUMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.global_metadatas = NUGlobalMetadatasFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.vms = NUVMsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.containers = NUContainersFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.groups = NUGroupsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.avatars = NUAvatarsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        
        
        self.event_logs = NUEventLogsFetcher.fetcher_with_object(parent_object=self, relationship="child")
        

        self._compute_args(**kwargs)

    # Properties
    
    @property
    def ldapuser_dn(self):
        """ Get ldapuser_dn value.

            Notes:
                The LDAP distinguished name (DN) for the user.

                
                This attribute is named `LDAPUserDN` in VSD API.
                
        """
        return self._ldapuser_dn

    @ldapuser_dn.setter
    def ldapuser_dn(self, value):
        """ Set ldapuser_dn value.

            Notes:
                The LDAP distinguished name (DN) for the user.

                
                This attribute is named `LDAPUserDN` in VSD API.
                
        """
        self._ldapuser_dn = value

    
    @property
    def management_mode(self):
        """ Get management_mode value.

            Notes:
                Management mode of the user object - allows for override of external authorization and syncup

                
                This attribute is named `managementMode` in VSD API.
                
        """
        return self._management_mode

    @management_mode.setter
    def management_mode(self, value):
        """ Set management_mode value.

            Notes:
                Management mode of the user object - allows for override of external authorization and syncup

                
                This attribute is named `managementMode` in VSD API.
                
        """
        self._management_mode = value

    
    @property
    def password(self):
        """ Get password value.

            Notes:
                User password in clear text. Password cannot be a single character asterisk (*)

                
        """
        return self._password

    @password.setter
    def password(self, value):
        """ Set password value.

            Notes:
                User password in clear text. Password cannot be a single character asterisk (*)

                
        """
        self._password = value

    
    @property
    def last_name(self):
        """ Get last_name value.

            Notes:
                Last name of the user

                
                This attribute is named `lastName` in VSD API.
                
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """ Set last_name value.

            Notes:
                Last name of the user

                
                This attribute is named `lastName` in VSD API.
                
        """
        self._last_name = value

    
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
    def first_name(self):
        """ Get first_name value.

            Notes:
                First name of the user

                
                This attribute is named `firstName` in VSD API.
                
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """ Set first_name value.

            Notes:
                First name of the user

                
                This attribute is named `firstName` in VSD API.
                
        """
        self._first_name = value

    
    @property
    def disable_certificate_auth(self):
        """ Get disable_certificate_auth value.

            Notes:
                Whether Certificate-Based Authentication is disabled. Default is false.

                
                This attribute is named `disableCertificateAuth` in VSD API.
                
        """
        return self._disable_certificate_auth

    @disable_certificate_auth.setter
    def disable_certificate_auth(self, value):
        """ Set disable_certificate_auth value.

            Notes:
                Whether Certificate-Based Authentication is disabled. Default is false.

                
                This attribute is named `disableCertificateAuth` in VSD API.
                
        """
        self._disable_certificate_auth = value

    
    @property
    def disable_password_auth(self):
        """ Get disable_password_auth value.

            Notes:
                Whether Username-Password Authentication is disabled. Default is false.

                
                This attribute is named `disablePasswordAuth` in VSD API.
                
        """
        return self._disable_password_auth

    @disable_password_auth.setter
    def disable_password_auth(self, value):
        """ Set disable_password_auth value.

            Notes:
                Whether Username-Password Authentication is disabled. Default is false.

                
                This attribute is named `disablePasswordAuth` in VSD API.
                
        """
        self._disable_password_auth = value

    
    @property
    def disabled(self):
        """ Get disabled value.

            Notes:
                Status of the user account; true=disabled, false=not disabled; default value = false

                
        """
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        """ Set disabled value.

            Notes:
                Status of the user account; true=disabled, false=not disabled; default value = false

                
        """
        self._disabled = value

    
    @property
    def email(self):
        """ Get email value.

            Notes:
                Email address of the user

                
        """
        return self._email

    @email.setter
    def email(self, value):
        """ Set email value.

            Notes:
                Email address of the user

                
        """
        self._email = value

    
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
    def mobile_number(self):
        """ Get mobile_number value.

            Notes:
                Mobile Number of the user

                
                This attribute is named `mobileNumber` in VSD API.
                
        """
        return self._mobile_number

    @mobile_number.setter
    def mobile_number(self, value):
        """ Set mobile_number value.

            Notes:
                Mobile Number of the user

                
                This attribute is named `mobileNumber` in VSD API.
                
        """
        self._mobile_number = value

    
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
    def user_name(self):
        """ Get user_name value.

            Notes:
                Unique Username of the user. Valid characters are alphabets, numbers and hyphen( - ).

                
                This attribute is named `userName` in VSD API.
                
        """
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        """ Set user_name value.

            Notes:
                Unique Username of the user. Valid characters are alphabets, numbers and hyphen( - ).

                
                This attribute is named `userName` in VSD API.
                
        """
        self._user_name = value

    
    @property
    def avatar_data(self):
        """ Get avatar_data value.

            Notes:
                URL to the avatar data associated with the enterprise. If the avatarType is URL then value of avatarData should an URL of the image. If the avatarType BASE64 then avatarData should be BASE64 encoded value of the image

                
                This attribute is named `avatarData` in VSD API.
                
        """
        return self._avatar_data

    @avatar_data.setter
    def avatar_data(self, value):
        """ Set avatar_data value.

            Notes:
                URL to the avatar data associated with the enterprise. If the avatarType is URL then value of avatarData should an URL of the image. If the avatarType BASE64 then avatarData should be BASE64 encoded value of the image

                
                This attribute is named `avatarData` in VSD API.
                
        """
        self._avatar_data = value

    
    @property
    def avatar_type(self):
        """ Get avatar_type value.

            Notes:
                Avatar type.

                
                This attribute is named `avatarType` in VSD API.
                
        """
        return self._avatar_type

    @avatar_type.setter
    def avatar_type(self, value):
        """ Set avatar_type value.

            Notes:
                Avatar type.

                
                This attribute is named `avatarType` in VSD API.
                
        """
        self._avatar_type = value

    
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

    

    