# -*- coding: utf-8 -*-
# Copyright (c) 2007, 2008, Benoît Chesneau
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#	   * Redistributions of source code must retain the above copyright
#	   * notice, this list of conditions and the following disclaimer.
#	   * Redistributions in binary form must reproduce the above copyright
#	   * notice, this list of conditions and the following disclaimer in the
#	   * documentation and/or other materials provided with the
#	   * distribution.	Neither the name of the <ORGANIZATION> nor the names
#	   * of its contributors may be used to endorse or promote products
#	   * derived from this software without specific prior written
#	   * permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils.html import escape
from django.http import get_host

from openid.consumer.consumer import Consumer
from openid.consumer.discover import DiscoveryFailure

from util import OpenID, DjangoOpenIDStore

import re
#import logging


# needed for some linux distributions like debian
try:
	from openid.yadis import xri
except ImportError:
	from yadis import xri

__all__ = ['OpenidSigninForm', 'OpenidAuthForm', 'OpenidVerifyForm',
		'OpenidRegisterForm', 'RegistrationForm', 'ChangepwForm',
		'ChangeemailForm', 'EmailPasswordForm', 'DeleteForm',
		'ChangeOpenidForm', 'ChangeEmailForm', 'ChangepwForm']
		
		
def get_url_host(request):
	if request.is_secure():
		protocol = 'https'
	else:
		protocol = 'http'
	host = escape(get_host(request))
	return '%s://%s' % (protocol, host)

def get_full_url(request):
	if request.is_secure():
		protocol = 'https'
	else:
		protocol = 'http'
	host = escape(request.META['HTTP_HOST'])
	return get_url_host(request) + request.get_full_path()

next_url_re = re.compile('^/[-\w/]+$')

def is_valid_next_url(next):
	# When we allow this:
	#	/openid/?next=/welcome/
	# For security reasons we want to restrict the next= bit 
	# to being a local path, not a complete URL.
	return bool(next_url_re.match(next))

def ask_openid(request, openid_url):
	""" basic function to ask openid and return response """

	if xri.identifierScheme(openid_url) == 'XRI' and getattr(
			settings, 'OPENID_DISALLOW_INAMES', False
	):
		#msg = _("i-names are not supported")
		raise forms.ValidationError(_("i-names are not supported"))
		#return on_failure(request, msg)
		
	consumer = Consumer(request.session, DjangoOpenIDStore())
	try:
		auth_request = consumer.begin(openid_url)
		return auth_request
	except DiscoveryFailure:
		#msg = _("The password or OpenID was invalid")
		raise forms.ValidationError(_("The password or OpenID is invalid"))
		#return on_failure(request, msg)

	#return HttpResponseRedirect(redirect_url)
	return False


class OpenidSigninForm(forms.Form):
	""" signin form """
	
	def __init__(self, request=None, *args, **kwargs):
		self.request = request
		super(OpenidSigninForm, self).__init__(*args, **kwargs)
	
	openid_url = forms.CharField(max_length=255, 
			widget=forms.widgets.TextInput(attrs={'class': 'required openid',
												   'autocorrect': 'off',
												   'autocapitalize':'off'}))
	next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
			 required=False)

	def clean_openid_url(self):
		""" test if openid is accepted """
		if 'openid_url' in self.cleaned_data:
			openid_url = self.cleaned_data['openid_url']
			
			try:
				self.openid_auth_request = ask_openid(self.request, self.cleaned_data['openid_url'])
				return self.cleaned_data['openid_url']
			except forms.ValidationError as e:
				raise e	
				#pass # ask_open() should raise a ValidationError if OpenID is invalid


	def clean_next(self):
		""" validate next """
		if 'next' in self.cleaned_data and self.cleaned_data['next'] != "":
			next_url_re = re.compile('^/[-\w/]*$')
			if not next_url_re.match(self.cleaned_data['next']):
				raise forms.ValidationError(_('next url "%s" is invalid' % 
					self.cleaned_data['next']))
			return self.cleaned_data['next']


	def get_sreg_redirect(self, sreg_req, redirect_to):
		trust_root = getattr(
			settings, 'OPENID_TRUST_ROOT', get_url_host(self.request) + '/'
		)

		self.openid_auth_request.addExtension(sreg_req)
		redirect_url = self.openid_auth_request.redirectURL(trust_root, redirect_to)

		return redirect_url
		

attrs_dict = { 'class': 'required login',
			   'autocorrect':'off',
			   'autocapitalize':'off'}
username_re = re.compile(r'^\w+$')

class OpenidAuthForm(forms.Form):
	""" legacy account signin form """
	next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
			required=False)
	username = forms.CharField(max_length=30,  
			widget=forms.widgets.TextInput(attrs=attrs_dict))
	password = forms.CharField(max_length=128, 
			widget=forms.widgets.PasswordInput(attrs=attrs_dict))
	   
	def __init__(self, data=None, files=None, auto_id='id_%s',
			prefix=None, initial=None): 
		super(OpenidAuthForm, self).__init__(data, files, auto_id,
				prefix, initial)
		self.user_cache = None
			
	def clean_username(self):
		""" validate username and test if it exists."""
		if 'username' in self.cleaned_data and \
				'openid_url' not in self.cleaned_data:
			if not username_re.search(self.cleaned_data['username']):
				raise forms.ValidationError(_("Usernames can only contain \
					letters, numbers and underscores"))
			try:
				user = User.objects.get(
						username__exact = self.cleaned_data['username']
				)
			except User.DoesNotExist:
				raise forms.ValidationError(_("There is no account with this username."))
			return self.cleaned_data['username']

	def clean_password(self):
		"""" test if password is valid for this username """
		if 'username' in self.cleaned_data and \
				'password' in self.cleaned_data:
			self.user_cache =  authenticate(
					username=self.cleaned_data['username'], 
					password=self.cleaned_data['password']
			)
			if self.user_cache is None:
				raise forms.ValidationError(_("Please enter a correct \
					username and password. Note that both fields are \
					case-sensitive."))
			elif self.user_cache.is_active == False:
				raise forms.ValidationError(_("This account is inactive."))
			return self.cleaned_data['password']

	def clean_next(self):
		""" validate next url """
		if 'next' in self.cleaned_data and \
				self.cleaned_data['next'] != "":
			next_url_re = re.compile('^/[-\w/]*$')
			if not next_url_re.match(self.cleaned_data['next']):
				raise forms.ValidationError(
						_('next url "%s" is invalid' % 
							self.cleaned_data['next'])
				)
			return self.cleaned_data['next']
			
	def get_user(self):
		""" get authenticated user """
		return self.user_cache
			

class OpenidRegisterForm(forms.Form):
	""" openid signin form """
	next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
			required=False)
	username = forms.CharField(max_length=30, 
			widget=forms.widgets.TextInput(attrs=attrs_dict))
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
		maxlength=200)), label=u'Email address')
	
	def clean_username(self):
		""" test if username is valid and exist in database """
		if 'username' in self.cleaned_data:
			if not username_re.search(self.cleaned_data['username']):
				raise forms.ValidationError(_("Usernames can only contain \
					letters, numbers and underscores"))
			try:
				user = User.objects.get(
						username__exact = self.cleaned_data['username']
						)
			except User.DoesNotExist:
				return self.cleaned_data['username']
			raise forms.ValidationError(_("This username is already \
				taken. Please choose another."))
			
	def clean_email(self):
		"""For security reason one unique email in database"""
		if 'email' in self.cleaned_data:
			try:
				user = User.objects.get(email = self.cleaned_data['email'])
			except User.DoesNotExist:
				return self.cleaned_data['email']
			raise forms.ValidationError(_("This email is already \
				registered in our database. Please choose another."))
 
	
class OpenidVerifyForm(forms.Form):
	""" openid verify form (associate an openid with an account) """
	next = forms.CharField(max_length=255, widget = forms.HiddenInput(), 
			required=False)
	username = forms.CharField(max_length=30, 
			widget=forms.widgets.TextInput(attrs=attrs_dict))
	password = forms.CharField(max_length=128, 
			widget=forms.widgets.PasswordInput(attrs=attrs_dict))
	
	def __init__(self, data=None, files=None, auto_id='id_%s',
			prefix=None, initial=None): 
		super(OpenidVerifyForm, self).__init__(data, files, auto_id,
				prefix, initial)
		self.user_cache = None

	def clean_username(self):
		""" validate username """
		if 'username' in self.cleaned_data:
			if not username_re.search(self.cleaned_data['username']):
				raise forms.ValidationError(_("Usernames can only contain \
					letters, numbers and underscores"))
			try:
				user = User.objects.get(
						username__exact = self.cleaned_data['username']
				)
			except User.DoesNotExist:
				raise forms.ValidationError(_("This username doesn't exist. \
						Please choose another."))
			return self.cleaned_data['username']
			
	def clean_password(self):
		""" test if password is valid for this user """
		if 'username' in self.cleaned_data and \
				'password' in self.cleaned_data:
			self.user_cache =  authenticate(
					username = self.cleaned_data['username'], 
					password = self.cleaned_data['password']
			)
			if self.user_cache is None:
				raise forms.ValidationError(_("Please enter a correct \
					username and password. Note that both fields are \
					case-sensitive."))
			elif self.user_cache.is_active == False:
				raise forms.ValidationError(_("This account is inactive."))
			return self.cleaned_data['password']
			
	def get_user(self):
		""" get authenticated user """
		return self.user_cache


attrs_dict = { 'class': 'required' }
username_re = re.compile(r'^\w+$')

class RegistrationForm(forms.Form):
	""" legacy registration form """

	next = forms.CharField(max_length=255, widget=forms.HiddenInput(), 
			required=False)
	username = forms.CharField(max_length=30,
			widget=forms.TextInput(attrs=attrs_dict),
			label=u'Username')
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
			maxlength=200)), label=u'Email address')
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
			label=u'Password')
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
			label=u'Confirm password')

	def clean_username(self):
		"""
		Validates that the username is alphanumeric and is not already
		in use.
		
		"""
		if 'username' in self.cleaned_data:
			if not username_re.search(self.cleaned_data['username']):
				raise forms.ValidationError(u'Usernames can only contain \
						letters, numbers and underscores')
			try:
				user = User.objects.get(
						username__exact = self.cleaned_data['username']
				)

			except User.DoesNotExist:
				return self.cleaned_data['username']
			raise forms.ValidationError(u'This username is already taken. \
					Please choose another.')

	def clean_email(self):
		""" validate if email exist in database
		:return: raise error if it exist """
		if 'email' in self.cleaned_data:
			try:
				user = User.objects.get(email = self.cleaned_data['email'])
			except User.DoesNotExist:
				return self.cleaned_data['email']
			raise forms.ValidationError(u'This email is already registered \
					in our database. Please choose another.')
		return self.cleaned_data['email']
	
	def clean_password2(self):
		"""
		Validates that the two password inputs match.
		
		"""
		if 'password1' in self.cleaned_data and \
				'password2' in self.cleaned_data and \
				self.cleaned_data['password1'] == \
				self.cleaned_data['password2']:
			return self.cleaned_data['password2']
		raise forms.ValidationError(u'You must type the same password each \
				time')


class ChangepwForm(forms.Form):
	""" change password form """
	oldpw = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("Old password"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("New password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict), label=_("Confirm new password"))

	def __init__(self, data=None, user=None, *args, **kwargs):
		if user is None:
			raise TypeError("Keyword argument 'user' must be supplied")
		super(ChangepwForm, self).__init__(data, *args, **kwargs)
		self.user = user

	def clean_oldpw(self):
		""" test old password """
		if not self.user.check_password(self.cleaned_data['oldpw']):
			raise forms.ValidationError(_("Old password is wrong. \
					Please enter a valid password."))
		return self.cleaned_data['oldpw']
	
	def clean_password2(self):
		"""
		Validates that the two password inputs match.
		"""
		if 'password1' in self.cleaned_data and \
				'password2' in self.cleaned_data and \
		   self.cleaned_data['password1'] == self.cleaned_data['password2']:
			return self.cleaned_data['password2']
		raise forms.ValidationError(_("New passwords do not match each other"))
		
		
class ChangeemailForm(forms.Form):
	""" change email form """
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
		maxlength=200)), label=u'Email address')
	password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict))

	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, \
			initial=None, user=None):
		if user is None:
			raise TypeError("Keyword argument 'user' must be supplied")
		super(ChangeemailForm, self).__init__(data, files, auto_id, 
				prefix, initial)
		self.test_openid = False
		self.user = user

	def clean_password(self):
		""" check if we have to test a legacy account or not """
		if 'password' in self.cleaned_data:
			if not self.user.check_password(self.cleaned_data['password']):
				self.test_openid = True
		return self.cleaned_data['password']
				
class ChangeopenidForm(forms.Form):
	""" change openid form """
	openid_url = forms.CharField(max_length=255,
			widget=forms.TextInput(attrs={'class': "required" }), label=_("OpenID URL"))

	def __init__(self, request, data=None, user=None, *args, **kwargs):
		if user is None:
			raise TypeError("Keyword argument 'user' must be supplied")
		super(ChangeopenidForm, self).__init__(data, *args, **kwargs)
		self.user = user
		self.request = request
		
	
	def clean_openid_url(self):
		"""validate the openid_url field"""	
		if 'openid_url' in self.cleaned_data:
			try:
				self.openid_auth_request = ask_openid(self.request, self.cleaned_data['openid_url'])
				return self.cleaned_data['openid_url']
			except forms.ValidationError as e:
				raise e	

class DeleteForm(forms.Form):
	""" confirm form to delete an account """
	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
	openid_url = forms.CharField(required=False,widget=forms.TextInput(attrs={'autocomplete':'on'}), label=_("OpenID URL"))
	confirm = forms.CharField(required=True, widget=forms.CheckboxInput(attrs={'style':'display:inline', 'class':'required'}), label=_("I'm sure I want to delete all my personal information and books."))

	def __init__(self, data=None, files=None, auto_id='id_%s',
			prefix=None, initial=None, user=None):
		super(DeleteForm, self).__init__(data, files, auto_id, prefix, initial)
		self.user = user

	def clean(self):
		if not self.cleaned_data['password'] and not self.cleaned_data['openid_url']:
			raise forms.ValidationError(u'Either an OpenID URL or a password must be provided')
		if self.cleaned_data['password'] and self.cleaned_data['openid_url']:
			raise forms.ValidationError(u'Please enter either an OpenID URL or a password, but not both')
			
		if not self.cleaned_data['confirm'] or self.cleaned_data['confirm'] == 'False':
			raise forms.ValidationError(u"You must confirm that you're sure by checking the box.")
		return super(DeleteForm, self).clean()

class EmailPasswordForm(forms.Form):
	""" send new password form """
	username = forms.CharField(max_length=30,
			widget=forms.TextInput(attrs={'class': "required" }))

	def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
			initial=None):
		super(EmailPasswordForm, self).__init__(data, files, auto_id, 
				prefix, initial)
		self.user_cache = None


	def clean_username(self):
		""" get user for this username """
		if 'username' in self.cleaned_data:
			try:
				self.user_cache = User.objects.get(
						username = self.cleaned_data['username'])
			except:
				raise forms.ValidationError(_("Incorrect username."))
		return self.cleaned_data['username']
