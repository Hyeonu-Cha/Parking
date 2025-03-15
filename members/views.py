from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import NewListingForm, NewUserForm
from .models import Property, RequestModel, RewardPoints, Messages
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import permission_required
from django.urls import reverse
import stripe

from datetime import datetime
from members.chatbot import get_response
import re
from datetime import datetime, timedelta

def stripe_checkout(request):
	print(request)
	if request.method == 'POST':
		# Get the request object
		booking_req_id = request.POST.get('request_id')

		all_requests = RequestModel.objects.all()
		req = all_requests.filter(id=booking_req_id).first()
		#req = RequestModel.objects.get(id=booking_req_id)
		# Create the Stripe Checkout Session
		session = stripe.checkout.Session.create(
			payment_method_types=['card'],
			line_items=[{
				'price_data': {
					'currency': 'aud',
					'unit_amount': int(req.booking_cost * 100),
					'product_data': {
						'name': f"Parking {req.id}",
					},
				},
				'quantity': 1,
			}],
			mode='payment',
			success_url=request.build_absolute_uri(reverse('payment_success')) + f'?request_id={booking_req_id}',
			cancel_url=request.build_absolute_uri(reverse('payment_cancel')) + f'?request_id={booking_req_id}',
		)

		# Redirect to the Stripe Checkout page
		return HttpResponseRedirect(session.url)

	return render(request, 'stripe_checkout.html', {'request_id': booking_req_id, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

def payment_success(request):
	if request.method == 'GET':
		request_id = request.GET.get('request_id')
		if request_id:
			req = RequestModel.objects.get(id=request_id)
			req.status = "Confirmed"
			req.save()
		
			my_bookings = RequestModel.objects.filter(userid=request.user).filter(status="Confirmed")
			# return render(request=request, template_name="customerbookings.html", context={'Bookings':my_bookings})
			# Render the customerbookings.html template here
			return render(request=request, template_name="customerbookings.html", context={'Bookings':my_bookings})
		else:
			# Redirect to an error page or home page if request_id is missing
			return redirect('/')
	else:
		# Redirect to an error page or home page if the request method is not GET
		return redirect('/')
	
def payment_cancel(request):
	if request.method == 'GET':
		return redirect('/my-requests')
	else:
		# Redirect to an error page or home page if the request method is not GET
		return redirect('/')

reward_count_bookings = 0
reward_count_parking = 0

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			print("reg success")
			RewardPoints.objects.create(userid=request.user, value=10, description="Thank you for Registering with Palm Spring Parking Spaces.")
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		print("reg failed")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homepage")

#@permission_required("members.add_property", login_url="/banned", raise_exception=True)
def homepage(request):
	listings = Property.objects.all()
	users = User.objects.all()
	if request.method == "POST":
		property_id = request.POST.get("property-id")
		user_id = request.POST.get("provider-id")
		send_req = request.POST.get("send-req")
		calc_req = request.POST.get("calc-req")
		print(request.POST)
		filter_req = request.POST.get("filter-req")
		if property_id:
			listing = listings.filter(id=property_id).first()
			if listing and (listing.providerid == request.user or request.user.is_superuser):
				listing.delete()
		elif user_id:
			user = users.filter(username=user_id).first()
			if user and request.user.is_superuser:
				try:
					group = Group.objects.get(name='default')
					group.user_set.remove(user)
					print("banned")
					user.delete()
					print("deleted")
				except:
					pass
					print("Already banned")
		elif send_req:
			print("req sent now")
			print(request.POST)
			send_req_id = int(request.POST.get('send-req'))
			listing = listings.filter(id=send_req_id).first()
			
			# Get start and end time from user input in the form
			start_datetime_str = request.POST.get('start_datetime')
			end_datetime_str = request.POST.get('end_datetime')
			chosen_start_time = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
			chosen_end_time = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')

			if chosen_start_time <= datetime.now():
				return render(request=request, template_name="header.html", context={'listings':listings, 'invalid_start_date':True})

			if chosen_end_time <= chosen_start_time:
				return render(request=request, template_name="header.html", context={'listings':listings, 'invalid_end_date':True})

			cost_for_dates = calculate_booking_cost(chosen_start_time, chosen_end_time, listing.price_weekday, listing.price_weekend)

			new_req = RequestModel(
				userid = request.user,
				propertyid = listing,
				providerid = listing.providerid,
				price = listing.price_weekday,
				property_image = listing.property_image,
				start_time = chosen_start_time,
				end_time = chosen_end_time,
				booking_cost = cost_for_dates,
				status = "Requested",
				created_at = datetime.now()
			)
			new_req.save()
			return render(request=request, template_name="header.html", context={'listings':listings, 'req_sent':True})


		elif calc_req:
			print("req sent now")
			print(request.POST)
			send_req_id = int(request.POST.get('calc-req'))
			listing = listings.filter(id=send_req_id).first()
			
			# Get start and end time from user input in the form
			start_datetime_str = request.POST.get('start_datetime')
			end_datetime_str = request.POST.get('end_datetime')
			chosen_start_time = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
			chosen_end_time = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
			cost_for_dates = calculate_booking_cost(chosen_start_time, chosen_end_time, listing.price_weekday, listing.price_weekend)
			calc_context = {
				'listings':listings, 
				'booking_cost': cost_for_dates, 
				'start_date': chosen_start_time,
				'end_date': chosen_end_time,
				'calc_for_id': listing.id
			}

			return render(request=request, template_name="header.html", context=calc_context)


		elif filter_req:
			price_filt = request.POST.get('price-slider')
			suburb_filt = request.POST.get('suburb-input')
			ev_filt = request.POST.get('ev-checkbox')
			handicap_filt = request.POST.get('handicap-checkbox')
			if price_filt and price_filt != '150':
				listings = listings.filter(price_weekend__lte=int(price_filt))
			if suburb_filt:
				listings = listings.filter(suburb__icontains=suburb_filt)
			if ev_filt:
				listings = listings.filter(ev=True)
			if handicap_filt:
				listings = listings.filter(handicap=True)
			print(price_filt, suburb_filt, ev_filt, handicap_filt)
			return render(request=request, template_name="header.html", context={'listings':listings})
		

	
	return render(request=request, template_name="header.html", context={'listings':listings})

def create_listing(request):
	if request.method == 'GET':
		return render(request, 'create_listing.html')
	elif request.method == 'POST':
		no_listings = Property.objects.all().filter(providerid=request.user).count()
		if no_listings == 0:
			RewardPoints.objects.create(userid=request.user, value=10, description="You listed your first Parking space!!")

		user1 = User.objects.get(id=request.user.id)
		updated_request = request.POST.copy()
		updated_request.update({'deleted': False})
		updated_request.update({'providerid': user1})

		handicapBool = False
		if request.POST.get('handicap') == 'on':
			handicapBool = True

		evBool = False
		if request.POST.get('ev') == 'on':
			evBool = True
		
		updated_request.update({'handicap': handicapBool})
		updated_request.update({'ev': evBool})

		listing_form = NewListingForm(updated_request,request.FILES)
		if listing_form.is_valid():
			listing_form.save()
			return redirect("homepage")
		else:
			print(listing_form.errors)
		return render(request, 'create_listing.html')

def banned_view(request):
    return render(request, 'banned.html')

def edit_listing(request):
	if request.method == 'GET':
		return render(request, 'create_listing.html')
	elif request.method == 'POST':

		user1 = User.objects.get(id=request.user.id)
		propertyid = request.POST.get('property-id')	

		updated_request = request.POST.copy()
		updated_request.update({'property-id': propertyid})
		updated_request.update({'deleted': False})
		updated_request.update({'providerid': user1})

		handicapBool = False
		if request.POST.get('handicap') == 'on':
			handicapBool = True

		evBool = False
		if request.POST.get('ev') == 'on':
			evBool = True
		
		updated_request.update({'handicap': handicapBool})
		updated_request.update({'ev': evBool})
		if propertyid is not None:
			listing_form = Property.objects.get(id = propertyid)
			listing_form.delete()

		listing_form = NewListingForm(updated_request,request.FILES)
		if listing_form.is_valid():
			listing_form.save()
			return redirect("homepage")
		else:
			print(listing_form.errors)
		return render(request, 'edit_listing.html')

def my_requests(request):
	all_requests = RequestModel.objects.all()
	my_requests = all_requests.filter(providerid=request.user, status="Requested")
	my_payments = all_requests.filter(userid=request.user, status="Payment")
	aprv = request.POST.get('aprv')
	rej = request.POST.get('rej')
	pmt = request.POST.get('pmt')
	print("pmt is", pmt)
	if(aprv):
		aprv_req = RequestModel.objects.get(id=int(aprv))
		aprv_req.status = "Payment"
		aprv_req.save()
		print("approved")
	elif(rej):
		req = RequestModel.objects.get(id=int(rej))
		req.status = "Available"
		req.save()
		print("rejected")
	elif(pmt):
		print("herere")
		req = RequestModel.objects.get(id=int(pmt))
		req.status = "Confirmed"
		req.save()
		print("Payment done")
	
	print(my_requests)
	return render(request, 'requests.html', context={'Requests':my_requests, 'Payments': my_payments})


def my_bookings(request):
	my_bookings = RequestModel.objects.filter(userid=request.user).filter(status="Confirmed")
	rented_out = RequestModel.objects.filter(providerid=request.user).filter(status="Confirmed")
	return render(request=request, template_name="customerbookings.html", context={'Bookings':my_bookings, 'Rented':rented_out})

def cancel_booking(request):
	all_requests = RequestModel.objects.all()
	my_requests = all_requests.filter(providerid=request.user, status="Requested")
	my_payments = all_requests.filter(userid=request.user, status="Payment")
	my_payments.delete()
	return render(request=request, template_name="requests.html", context={'Requests':my_requests, 'Payments': my_payments})

def bot_response(request):

	print(request.GET['usr_msg'])
	resp = request.GET['usr_msg']
	print(request.GET['user_id'])
	print(resp)
	resp = resp.lower()
	if ("parking" in resp) or ("cancel" in resp):
		print("cancelling booking")
		userid = request.GET['user_id']
		users = User.objects.all()
		user = users.filter(username=userid).first()
		my_bookings = RequestModel.objects.filter(userid=user).filter(status="Confirmed")
		parking_id = ''
		if(any(char.isdigit() for char in resp)):
			print(my_bookings)
			parking_id = int(re.search(r'\d+', resp).group())
		if parking_id:
			my_bookings = my_bookings.filter(id=parking_id)
			if my_bookings:
				my_bookings.delete()
				resp = "Your booking has been deleted"
			else:
				resp = "That booking was not found, try again"
			return JsonResponse({'Response':resp})
		else:
			return JsonResponse({'Response':"Helper Bot: Which booking would you like to cancel?"})

	resp = get_response(resp)
		
	resp = "Helper Bot: " + resp
	return JsonResponse({'Response':resp})


def chatbot(request):
	resp = ''
	print("home")
	return render(request=request, template_name="chatbot.html", context={'data':"Hello World!"})
def calculate_booking_cost(start_time, end_time, price_weekday, price_weekend):
	total_days = (end_time - start_time).days + 1
	total_cost = 0
	for i in range(total_days):
		current_day = start_time + timedelta(days=i)
		if current_day.weekday() < 5:
			total_cost += price_weekday
		else:
			total_cost += price_weekend
	return total_cost

def reward_points(request):
	global reward_count_bookings
	global reward_count_parking
	no_bookings = RequestModel.objects.filter(userid=request.user).filter(status="Confirmed").count()
	no_parkings = RequestModel.objects.filter(providerid=request.user).filter(status="Confirmed").count()
	
	if no_bookings % 10 > reward_count_bookings:
		RewardPoints.objects.create(userid=request.user, value=20, description="You have made a lot of bookings in the past.")
		reward_count_bookings += 1
	
	if no_parkings % 10 > reward_count_parking:
		RewardPoints.objects.create(userid=request.user, value=20, description="You're parking space is in demand.")
		reward_count_parking += 1

	all_points = RewardPoints.objects.all().filter(userid=request.user)
	totalpoints = 0
	for point in all_points:
		totalpoints += point.value
	return render(request=request, template_name="rewards.html", context={'Rewards':all_points, "Total":totalpoints})

@login_required
def get_dm(request):
    
    #admin can check the reported messages

    if request.user.is_superuser:	
        get_reported_messages = Messages.objects.filter(reported = True).order_by('created_at')
        return render(request, 'admin_messages.html', {'messages': get_reported_messages})
    
    if request.method == 'POST':
        #user = User.objects.get(username= request.user)
        receiver = request.POST.get('receiver')
        messages = Messages.objects.filter(receiver=receiver).order_by('created_at')
        return render(request, 'messages.html', {'messages': messages})

    return redirect("homepage")
@login_required
def send_dm(request):
    if request.method == 'POST':
        providerid = request.POST['receiver']

        receiver = User.objects.get(username= providerid)

        messages1 = Messages.objects.filter(sender=request.user).filter(receiver = providerid)
        messages2 = Messages.objects.filter(sender=receiver).filter(receiver = request.user.username)
        messages = messages1 | messages2
        if not messages.exists(): #when there is no messages each other 
            if not request.user.is_superuser:
                messages = Messages(sender=request.user, receiver = providerid, text="Hi! This is the start of conversation!")
                messages.save()
                messages1 = Messages.objects.filter(sender=request.user).filter(receiver = providerid)
                messages2 = Messages.objects.filter(sender=receiver).filter(receiver = request.user.username)
                messages = messages1 | messages2
                return render(request, 'send_messages.html', {'messages': messages})
        messages = messages.order_by('created_at')
    return render(request, 'send_messages.html', {'messages': messages})


@login_required
def send_msg(request):
    if request.method == 'POST':
        receiver = request.POST['receiver-btn']
        text = request.POST['text']

        messages = Messages(sender=request.user, receiver=receiver, text=text)
        messages.save()
	
        receiveruser = User.objects.get(username= receiver)	
        messages1 = Messages.objects.filter(sender=request.user).filter(receiver = receiver)
        messages2 = Messages.objects.filter(sender=receiveruser).filter(receiver = request.user.username)
        messages = messages1 | messages2
        messages = messages.order_by('created_at')
        return render(request, 'send_messages.html', {'messages': messages})
    
@login_required
def report_view(request):
    if request.method == 'POST':

        message_id = request.POST['report-btn']
        Messages.objects.filter(id=message_id).update(reported=True)

    return redirect('homepage')


@login_required
def del_report_view(request):
    if request.method == 'POST':

        message_id = request.POST['messageid']
        Messages.objects.filter(id=message_id).update(reported=False)

    return redirect('homepage')

def ban_user(request):

	user_id = request.POST['receiver']
	user = User.objects.get(username = user_id)

	if user and request.user.is_superuser:
		try:
			group = Group.objects.get(name='default')
			group.user_set.remove(user)
			print("banned")
			user.delete()
			print("deleted")
		except:	
			pass
			print("Already banned")
	return redirect('del_report_msg')

@login_required    
def get_messages(request):
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        user = User.objects.get(username= request.user)

        send_messages = Messages.objects.filter(sender=user)
        get_messages = Messages.objects.filter(reciever=user.username)
        messages = send_messages | get_messages
        return render(request, 'messages.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        receiver = request.POST['receiver']
        text = request.POST['text']
        message = Messages(sender=sender, receiver=receiver, text=text)
        message.save()
        return redirect('inbox')

    return render(request, 'send_message.html')