from django.shortcuts import render
from django.core.exceptions import ValidationError

from Buyers.models import Vehicle1, userRegisteredTable
from django.contrib import messages


from seller.models import Vehicle

def userHome(request):
    if not request.session.get('id'):
        return render(request,'userLoginForm.html')
    
    return render(request,'userHome.html')
# Create your views here.
def userRegisterCheck(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        loginid=request.POST['loginid']
        mobile=request.POST['mobile']
        password=request.POST['password']
        location=request.POST.get('location', '')

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
            messages.success(request,'registration Successfully done,please wait for admin APPROVAL')
            return render(request, "userRegisterForm.html")


        except ValidationError as ve:
            # Get a list of error messages to display
            error_messages = []
            for field, errors in ve.message_dict.items():
                for error in errors:
                    error_messages.append(f"{field.capitalize()}: {error}")
            return render(request, "userRegisterForm.html", {"messages": error_messages})

        except Exception as e:
            # Handle other exceptions (like unique constraint fails)
            return render(request, "userRegisterForm.html", {"messages": [str(e)]})

    return render(request, "userRegisterForm.html")





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
                messages.error(request,'Status not activated please wait for admin approval')
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
    
    buyer_location = ""
    try:
        buyer = userRegisteredTable.objects.get(id=buyer_id)
        if buyer.location:
            buyer_location = buyer.location.lower().strip()
    except userRegisteredTable.DoesNotExist:
        pass

    # Basic filtering for available vehicles
    vehicles_query = Vehicle.objects.filter(status='available')
    
    # Apply search filter if query exists
    if search_query:
        from django.db.models import Q
        vehicles_query = vehicles_query.filter(
            Q(vehicle_number__icontains=search_query) | 
            Q(location__icontains=search_query)
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
        'search_query': search_query
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