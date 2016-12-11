from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserManager(models.Manager):

	def add_user(self, name, email_id, mobile, password):
		user = self.model(user_name=name,
						  email_id=email_id,
						  mobile_number=mobile,
						  password=password)
		user.save()
		return user

class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=255)
	email_id = models.CharField(max_length=255)
	mobile_number = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	is_integrated = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user_id)

	objects = UserManager()


# class FacebookUserManager(models.Manager):
	
# 	def add_facebook_user(self, id, name, token, expires_in, user):
# 		fb_user = self.model(user_id=id,
# 							 name=name,
# 							 token=token,
# 							 expires_in=expires_in,
# 							 user=user)
# 		fb_user.save()
# 		return fb_user


# class FacebookUser(models.Model):
# 	user_id = models.CharField(primary_key=True)
# 	name = models.CharField(max_length=255)
# 	access_token = models.TextField()
# 	expires_in = models.IntegerField()
# 	signed_request = models.TextField()
# 	user = models.ForeignKey(User)

# 	objects = FacebookUserManager()


class UserPageManager(models.Manager):

	def add_user_page(self, page_id, token, category, name, user):
		user_page = UserPage(page_id=page_id, acces_token=token, category=category,
							 name=name, facebook_user=user)
		user_page.save()
		return user_page


class UserPage(models.Model):
	page_id = models.CharField(max_length=255, primary_key=True)
	acces_token = models.TextField()
	category = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	facebook_user = models.ForeignKey(User)
	is_active = models.BooleanField(default=True)

	objects = UserPageManager()




