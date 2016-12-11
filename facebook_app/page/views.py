from django.shortcuts import render, redirect
from django.views.generic import View
from facebook_app.response import send_400, send_200
from facebook_app.settings import FACEBOOK_URL
from models import User, UserPage
import json
import requests
import copy

# Create your views here.


class PageView(View):
	
	def post(self, request):
		pages = request.POST.get("pages")
		user_id = request.POST.get("user_id")
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return send_400({"message": "Invalid User"})
		
		try:
			pages = json.loads(pages)
		except ValueError, e:
			return send_400({"message": "You don't have any pages. Create at least one page on facebook"})
		page = pages[0]
		try:
			user_page = UserPage.objects.add_user_page(page["id"], 
												   page["access_token"], 
												   page["category"], 
												   page["name"], 
												   user)
			user.is_integrated = True
			user.save()
		except IntegrityError, e:
			pass
		# item = {}
		# item["page_id"] = user_page.pk
		# item["name"] = user_page.name
		# item["category"] = user_page.category
		# url = FACEBOOK_URL + user_page.pk
		# data = {"fields": "about,bio,location,description,contact_address,hours,emails,phone,website,likes,overall_star_rating,fan_count",
		# 		"access_token": user_page.acces_token
		# 		}
		# response = requests.get(url, params=data)
		# item.update(json.loads(response.text))
		# print item
		# return redirect('/page/v1/listpage/', **kwargs)
		# kwargs = {"user_id": user.pk}
		# return redirect('list_page_view1', permanent=True, **kwargs)
		#return render('pages.html', context={"message": "Success", "page": item})
		return send_200({"message": "Successfully added."})


	def get(self, request):
		user_id =  request.GET.get("user_id")
		try:
			user = User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return send_400({"message": "Invalid User"})

		pages = UserPage.objects.filter(user=user)
		page_list = []
		for page in pages:
			item = {}
			item["page_id"] = page.pk
			item["name"] = page.name
			item["category"] = page.category
			page_list.append(item)
		return send_200({"message" : "Success", "pages": page_list})


def list_page_view(request, *args, **kwargs):
	print kwargs
	print request.POST
	user_id = kwargs.get("user_id")
	print user_id
	pages = UserPage.objects.filter(facebook_user_id=int(user_id))
	print pages.count()
	item = {}
	if pages:
		print "Here1"
		page = pages[0]
		item["page_id"] = page.pk
		item["name"] = page.name
		item["category"] = page.category
		url = FACEBOOK_URL + page.pk
		data = {"fields": "about,bio,location,description,contact_address,hours,emails,phone,website,likes,overall_star_rating,fan_count",
				"access_token": page.acces_token
				}
		response = requests.get(url, params=data)
		item.update(json.loads(response.text))
		print item
	print "Here"
	return render(request, 'pages.html', {"message": "Success", "page": item})


class Register(View):

	def post(self, request):
		full_name = request.POST.get("full_name")
		password = request.POST.get("password")
		email = request.POST.get("email")
		mobile = request.POST.get("mobile")
		if not full_name:
			return send_400({"message": "Name is missing."})
		if not password:
			return send_400({"message": "Password is missing."})
		if not email:
			return send_400({"message": "Email is missing."})
		if not mobile:
			return send_400({"message": "Mobile number is missing."})
		try:
			user = User.objects.get(email_id=email)
		except User.DoesNotExist, e:
			user = User.objects.add_user(full_name, email, mobile, password)
		else:
			return send_400({"message": "User already registed with this email id.Please login."})
		return send_200({"message": "Success", "user_id": user.pk})


class Login(View):

	def post(self, request):
		email = request.POST.get("email")
		password = request.POST.get("password")
		try:
			user = User.objects.get(email_id=email)
		except User.DoesNotExist:
			return send_400({"message": "User does not exists."})
		if user.password == password:
			return send_200({"message": "Login successful.", 
							"user_id": user.pk, 
							"user_name": user.user_name, 
							"user_email": user.email_id,
							"is_integrated": user.is_integrated})
			# kwargs = {"user_id": user.pk}
			# print kwargs
			# return redirect('/')
		return send_400({"message": "Wrong password."})


class UpdatePage(View):

	def post(self, request):
		data = request.POST
		page_id = data.get("page_id")
		data = dict(copy.deepcopy(data))
		try:
			page = UserPage.objects.get(page_id=page_id)
		except UserPage.DoesNotExist, e:
			return send_400({"message": "Page not found"})

		url = FACEBOOK_URL + page_id
		del data["page_id"]
		# del data["phone"]
		# del data["contact_address"]
		# del data["name"]
		data["access_token"] = page.acces_token
		print data
		res = requests.post(url, params=data)
		print res.text
		print res
		return send_200({"message": "Success"})










