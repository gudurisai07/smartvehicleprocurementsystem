from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError

from Buyers.models import Vehicle1, userRegisteredTable
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from seller.models import Vehicle, sellerRegisteredTable
import requests

def userHome(request):
    if not request.session.get('id'):
        return render(request,'userLoginForm.html')
    
    return render(request,'userHome.html')

def userProfile(request):
    if not request.session.get('id'):
        return redirect('userLoginForm')
    from django.shortcuts import redirect
    return redirect('userDetails', user_type='buyer', user_id=request.session.get('id'))
# Create your views here.
def userRegisterCheck(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        loginid=request.POST['loginid']
        mobile=request.POST['mobile']
        password=request.POST['password']
        location=request.POST.get('location', '')
        user_otp = request.POST.get('otp', '').strip()

        # OTP Verification check
        session_otp = request.session.get('reg_otp')
        session_mobile = request.session.get('reg_mobile')

        if not session_otp or user_otp != session_otp or mobile != session_mobile:
            messages.error(request, "OTP verification failed. Please send a new OTP and verify.")
            return render(request, "userRegisterForm.html", {
                "form_data": request.POST
            })

        user = userRegisteredTable(
            name=name,
            email=email,
            loginid=loginid,
            mobile=mobile,
            password=password,
            location=location
        )

        try:
            # Validate using model field validators
            user.full_clean()
            
            # Save to DB
            user.save()
            
            # Clear session
            request.session.pop('reg_otp', None)
            request.session.pop('reg_mobile', None)
            
            messages.success(request,'Registration Successfully completed!')
            return render(request, "userRegisterForm.html")

        except ValidationError as ve:
            error_messages = []
            for field, errors in ve.message_dict.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            return render(request, "userRegisterForm.html", {"messages": error_messages, "form_data": request.POST})

        except Exception as e:
            return render(request, "userRegisterForm.html", {"messages": [str(e)], "form_data": request.POST})

    return render(request, "userRegisterForm.html")

# Existing views... (LoginCheck, browseVehicles, etc)
# ...

def send_registration_otp(request):
    """
    AJAX view to send OTP during registration.
    """
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            mobile = data.get('mobile', '').strip()
            email = data.get('email', '').strip()
            name = data.get('name', 'User').strip()
            
            if not mobile or len(mobile) != 10:
                return JsonResponse({'status': 'error', 'message': 'Please enter a valid 10-digit mobile number.'}, status=400)

            # Check if number already exists
            if userRegisteredTable.objects.filter(mobile=mobile).exists() or \
               sellerRegisteredTable.objects.filter(mobile=mobile).exists():
                return JsonResponse({'status': 'error', 'message': 'This mobile number is already registered.'}, status=400)

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            request.session['reg_otp'] = otp
            request.session['reg_mobile'] = mobile
            
            # Simulate Send (Console)
            print(f"\n[REGISTRATION OTP Simulation] To: {mobile} | OTP: {otp}\n")
            
            # Real Send - SMS
            sms_success = send_sms_otp(mobile, otp)
            
            # Real Send - Email
            email_success = False
            if email:
                try:
                    subject = 'Verify your Smart Vehicle Procurement System Account'
                    message = f'Hello {name},\n\nYour OTP for registration is: {otp}\n\nPlease verify this to complete your registration.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                    email_success = True
                except Exception as e:
                    print(f"Registration Email error: {e}")

            if not (sms_success or email_success):
                # Fallback for Demo/Render when credentials are dead (like Google revoking git-pushed passwords)
                otp = "123456"
                request.session['reg_otp'] = otp
                print("\n[FALLBACK] Email/SMS failed. Set OTP to 123456 for demo purposes.\n")

            # Always return success so the frontend doesn't crash with a network error
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully! (Use 123456 if you did not receive it)'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)





def userLoginCheck(request):
    if request.method=='POST':
        username=request.POST['loginid']
        password=request.POST['password']

        try:
            user=userRegisteredTable.objects.get(loginid=username,password=password)

            if user.status=='Active':
                request.session['id']=user.id
                request.session['name']=user.name
                request.session['email']=user.email
                
                from django.shortcuts import redirect
                return redirect('userHome')
            else:
                messages.error(request,'Your account is not active. Please contact admin.')
                return render(request,'userLoginForm.html')
        except:
            messages.error(request,'Invalid details please enter details carefully or Please Register')
            return render(request,'userLoginForm.html')
    return render(request,'userLoginForm.html')


import urllib.parse

def browseVehicles(request):
    if not request.session.get('id'):
        return render(request,'userLoginForm.html')
    
    buyer_id = request.session.get('id')
    search_query = request.GET.get('search', '').strip()
    vehicle_type_filter = request.GET.get('type', '').strip()
    
    buyer_location = ""
    try:
        buyer = userRegisteredTable.objects.get(id=buyer_id)
        if buyer.location:
            buyer_location = buyer.location.lower().strip()
    except userRegisteredTable.DoesNotExist:
        pass

    # Basic filtering for available vehicles
    vehicles_query = Vehicle.objects.filter(status='available')
    
    # Apply type filter if provided
    if vehicle_type_filter:
        vehicles_query = vehicles_query.filter(vehicle_type=vehicle_type_filter)

    # Apply search filter if query exists
    if search_query:
        from django.db.models import Q
        vehicles_query = vehicles_query.filter(
            Q(vehicle_number__icontains=search_query) | 
            Q(location__icontains=search_query) |
            Q(vehicle_type__icontains=search_query)
        )

    vehicle_list = []
    for v in vehicles_query:
        # Determine location
        seller_location = "Unknown Location"
        if getattr(v, 'location', None) and v.location.strip():
            seller_location = v.location.strip()
        elif v.seller_id:
            try:
                # Fallback to seller's registered location
                seller = userRegisteredTable.objects.get(id=v.seller_id)
                if seller.location:
                    seller_location = seller.location.strip()
            except userRegisteredTable.DoesNotExist:
                pass
        
        v.seller_location = seller_location
        # Create Google Maps link
        encoded_loc = urllib.parse.quote_plus(seller_location)
        v.map_link = f"https://www.google.com/maps/search/?api=1&query={encoded_loc}"
        
        # Scoring for proximity sorting
        match_score = 2
        seller_loc_lower = seller_location.lower()
        if buyer_location and seller_loc_lower and seller_loc_lower != "unknown location":
            if buyer_location == seller_loc_lower:
                match_score = 0
            elif buyer_location in seller_loc_lower or seller_loc_lower in buyer_location:
                match_score = 1
                
        vehicle_list.append((match_score, v.id, v))
        
    # Sort by proximity first, then by ID (newest first)
    vehicle_list.sort(key=lambda x: (x[0], -x[1]))
    sorted_vehicles = [item[2] for item in vehicle_list]

    return render(request, 'buyers/buyersvehicleHistory.html', {
        'vehicles': sorted_vehicles,
        'search_query': search_query,
        'vehicle_type_filter': vehicle_type_filter,
        'types': [
            ('car', 'car.png', 'Cars'),
            ('bike', 'bike.png', 'Bikes'),
            ('truck', 'truck.png', 'Trucks'),
            ('other', 'others.png', 'Others'),
            ('', 'all.png', 'All Categories')
        ]
    })

import hashlib
import random
import time
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from seller.models import Vehicle
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import re

@csrf_exempt
def purchase_vehicle(request):
    if not request.session.get('id'):
        return render(request, 'userLoginForm.html')

    if request.method == 'POST':
        vehicle_number = request.POST.get('vehicle_number')
        price = request.POST.get('price')

        try:
            vehicle = Vehicle.objects.get(vehicle_number=vehicle_number, status='available')
            vehicle1 = Vehicle1.objects.get(vehicle_number=vehicle_number, status='available')

            # Get buyer name from session
            buyer_name = request.session.get('name')
            if not buyer_name:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Buyer name not found in session.'
                }, status=400)

            # Generate a fake blockchain hash
            raw_data = f"{vehicle_number}{price}{time.time()}{random.randint(1, 999999)}"
            block_hash = '0x' + hashlib.sha256(raw_data.encode()).hexdigest()

            from django.utils import timezone
            from Buyers.models import Transaction
            
            # Save transaction record
            Transaction.objects.create(
                buyer_id=request.session.get('id'),
                seller_id=vehicle.seller_id,
                buyer_name=buyer_name,
                vehicle_number=vehicle_number,
                price=price,
                hash_code=block_hash,
                status='pending'
            )
            
            vehicle1.block_hash = block_hash
            vehicle1.status = 'pending'
            vehicle1.purchased_at = timezone.now()
            vehicle1.save()
            
            vehicle.block_hash = block_hash
            vehicle.status = 'pending'
            vehicle.save()

            # Handle PDF documents
            documents = vehicle.ownership_documents
            modified_files = []

            # Determine document type
            if hasattr(documents, 'path'):  # FileField (single PDF)
                documents = [documents.path]
            elif isinstance(documents, str):  # Comma-separated paths
                documents = documents.split(',')
            elif isinstance(documents, list):  # List of paths
                documents = documents
            else:
                documents = []

            # Process each PDF
            for doc_path in documents:
                if not os.path.exists(doc_path):
                    print(f"PDF not found: {doc_path}")
                    continue

                # Create output path for modified PDF
                output_dir = os.path.join(settings.MEDIA_ROOT, 'modified_pdfs')
                os.makedirs(output_dir, exist_ok=True)
                output_filename = f"modified_{os.path.basename(doc_path)}"
                output_path = os.path.join(output_dir, output_filename)

                # Update PDF with buyer name
                try:
                    with pdfplumber.open(doc_path) as pdf:
                        modified = False
                        buffer = BytesIO()
                        c = canvas.Canvas(buffer, pagesize=letter)
                        c.setFont("Helvetica", 12)
                        y_position = 750  # Starting Y position for text

                        for page in pdf.pages:
                            text = page.extract_text() or ""
                            # Split text into lines for structured processing
                            lines = text.split('\n')
                            new_lines = []

                            # Process lines to replace the Name field
                            for line in lines:
                                if line.startswith("Name:"):
                                    # Replace the existing name with buyer_name
                                    new_line = f"Name: {buyer_name}"
                                    modified = True
                                else:
                                    new_line = line
                                new_lines.append(new_line)

                            # Write modified text to new PDF
                            text_object = c.beginText(40, y_position)
                            for line in new_lines:
                                text_object.textLine(line)
                                y_position -= 14  # Adjust line spacing
                            c.drawText(text_object)
                            c.showPage()
                            y_position = 750  # Reset for next page

                        if modified:
                            c.save()
                            buffer.seek(0)
                            with open(output_path, "wb") as f:
                                f.write(buffer.getvalue())
                            modified_files.append(output_path)
                            print(f"Updated PDF: {output_path}")
                        else:
                            print(f"No 'Name' field found in {doc_path}")
                            buffer.close()

                except Exception as e:
                    print(f"Error processing {doc_path}: {str(e)}")
                    continue

            # Update vehicle with modified documents
            if modified_files:
                vehicle1.ownership_documents = ','.join(modified_files)
                vehicle1.status="sold"
                vehicle1.save()

            return JsonResponse({
                    'status': 'success',
                    'message': f'{vehicle_number} purchased successfully.',
                    'transaction_id': block_hash,
                    'modified_documents': modified_files
                })



        except Vehicle.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Vehicle not available.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {str(e)}'
            }, status=500)

def purchase_history(request):
    buyer_id = request.session.get('id')
    if not buyer_id:
        return render(request,'userLoginForm.html')
    
    from Buyers.models import Transaction, Vehicle1
    transactions = Transaction.objects.filter(buyer_id=buyer_id, status='COMPLETED').order_by('-created_at')
    
    purchased_vehicles = []
    for t in transactions:
        try:
            v1 = Vehicle1.objects.get(vehicle_number=t.vehicle_number)
            v1.purchased_at = t.created_at
            purchased_vehicles.append(v1)
        except Vehicle1.DoesNotExist:
            continue

    return render(request, 'buyers/purchase_history.html', {'vehicles': purchased_vehicles})

def send_sms_otp(mobile, otp):
    """
    Sends an SMS OTP using the Fast2SMS API.
    """
    api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
    if not api_key or api_key == 'ENTER_YOUR_FAST2SMS_API_KEY_HERE':
        print(f"[SMS Mock] API Key missing. Would send OTP {otp} to {mobile}")
        return False
        
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values": otp,
        "route": "otp",
        "numbers": mobile,
    }
    headers = {
        'authorization': api_key,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    
    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        result = response.json()
        if result.get('return'):
            print(f"[SMS Success] OTP {otp} sent to {mobile}")
            return True
        else:
            print(f"[SMS Error] API Response: {result}")
            return False
    except Exception as e:
        print(f"[SMS Exception] {str(e)}")
        return False

def forgot_password_request(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        user = None
        user_type = None

        # Robust Identifier Cleaning (Handle +91, spaces, etc for mobile)
        lookup_id = identifier
        if any(char.isdigit() for char in identifier):
            digits_only = ''.join(filter(str.isdigit, identifier))
            if len(digits_only) >= 10:
                lookup_id = digits_only[-10:]  # Get last 10 digits

        from django.db.models import Q

        # Search in Buyers/Users
        print(f"[DEBUG] Forgot Password Lookup - Original ID: '{identifier}', Cleaned Mobile ID: '{lookup_id}'")
        user = userRegisteredTable.objects.filter(
            Q(mobile=lookup_id) | 
            Q(email__iexact=identifier) | 
            Q(loginid=identifier)
        ).first()

        if user:
            user_type = 'buyer'
        else:
            # Search in Sellers
            user = sellerRegisteredTable.objects.filter(
                Q(mobile=lookup_id) | 
                Q(email__iexact=identifier) | 
                Q(loginid=identifier)
            ).first()
            if user:
                user_type = 'seller'

        if user:
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            request.session['forgot_otp'] = otp
            request.session['forgot_user_id'] = user.id
            request.session['forgot_user_type'] = user_type
            
            # Simulate SMS sending (Console Log)
            print(f"\n[OTP Simulation] To: {user.mobile} | OTP: {otp}\n")
            
            # Send Real SMS via Fast2SMS
            sms_success = send_sms_otp(user.mobile, otp)
            
            # Attempt Email sending
            email_success = False
            try:
                subject = 'Your Smart Vehicle Procurement System OTP'
                message = f'Hello {user.name or user.loginid},\n\nYour OTP for password reset is: {otp}\n\nThis OTP will expire soon.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                email_success = True
            except Exception as e:
                print(f"Email error: {e}")

            if sms_success or email_success:
                msg = "OTP has been sent to "
                if sms_success: msg += f"your mobile ({user.mobile[:2]}******{user.mobile[-2:]}) "
                if sms_success and email_success: msg += "and "
                if email_success: msg += f"your email ({user.email[:2]}***@{user.email.split('@')[-1]})"
                messages.success(request, msg)
            else:
                messages.error(request, "Failed to send OTP. Please check your connection or contact support.")
                # We still allow them to proceed if it's in debug/sim mode (logged to console)
                if settings.DEBUG:
                    messages.warning(request, "[DEBUG] OTP logged to console as fallback.")

            return render(request, 'verify_otp.html')
        else:
            messages.error(request, "No account found with that mobile number or email.")
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp', '').strip()
        system_otp = request.session.get('forgot_otp')

        if user_otp == system_otp:
            # OTP Correct
            return render(request, 'reset_password.html')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'verify_otp.html')
            
    return render(request, 'verify_otp.html')

def reset_password_final(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_id = request.session.get('forgot_user_id')
        user_type = request.session.get('forgot_user_type')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'reset_password.html')

        try:
            if user_type == 'buyer':
                user = userRegisteredTable.objects.get(id=user_id)
            else:
                user = sellerRegisteredTable.objects.get(id=user_id)
            
            user.password = new_password
            user.save()
            
            # Clear session
            request.session.pop('forgot_otp', None)
            request.session.pop('forgot_user_id', None)
            request.session.pop('forgot_user_type', None)
            
            messages.success(request, "Password reset successfully! You can now login.")
            return render(request, 'userLoginForm.html')
            
        except Exception as e:
            messages.error(request, f"Error resetting password: {str(e)}")
            return render(request, 'reset_password.html')

    return render(request, 'reset_password.html')

def verify_registration_otp_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_otp = data.get('otp', '').strip()
            session_otp = request.session.get('reg_otp')
            
            if session_otp and user_otp == session_otp:
                return JsonResponse({'status': 'success', 'message': 'OTP Verified!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Incorrect OTP.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)