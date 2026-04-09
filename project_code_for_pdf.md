# Project Code: Smart Vehicle Procurement System using Blockchain Technology

This document contains the core implementation of the Smart Vehicle Procurement System. It includes the blockchain logic, vehicle transaction processing, and automated PDF document modification.

## 1. Routing & Configuration

### # File: Smart_Vehicle_Procurement_System_using_Blockchain_Technology/urls.py
```python
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from Admin import views as av
from Buyers import views as bv
from Smart_Vehicle_Procurement_System_using_Blockchain_Technology import views as mv
from seller import views as sv
from Buyers import api_views as api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mv.index, name='index'),

    # Registration & Login
    path('userRegisterForm', mv.userRegisterForm, name='userRegisterForm'),
    path('userLoginForm', mv.userLoginForm, name='userLoginForm'),
    path('adminLoginForm', mv.adminLoginForm, name='adminLoginForm'),

    # Admin URLs
    path('adminLoginCheck', av.adminLoginCheck, name='adminLoginCheck'),
    path('adminHome', av.adminHome, name='adminHome'),
    path('userdetails', av.userList, name='userdetails'),
    path('activate_user', av.activate_user, name='activate_user'),
    path('deactivate_user', av.deactivate_user, name='deactivate_user'),
    path('adminTransactions', av.adminTransactions, name='adminTransactions'),
    path('adminApproveTransaction', av.adminApproveTransaction, name='adminApproveTransaction'),

    # User (Buyer) URLs
    path('userHome', bv.userHome, name='userHome'),
    path('userRegisterCheck', bv.userRegisterCheck, name='userRegisterCheck'),
    path('userLoginCheck', bv.userLoginCheck, name='userLoginCheck'),
    path('browseVehicles', bv.browseVehicles, name='browseVehicles'),
    path('purchase_vehicle', bv.purchase_vehicle, name='purchase_vehicle'),
    path('purchaseHistory', bv.purchase_history, name='purchaseHistory'),

    # Seller URLs
    path('addVehicle', sv.addVehicle, name='addVehicle'),
    path('sellerLoginCheck', sv.sellerLoginCheck, name='sellerLoginCheck'),
    path('verify_rto_vehicle', sv.verify_rto_vehicle, name='verify_rto_vehicle'),
    path('vehicleHistory', sv.vehicleHistory, name='vehicleHistory'),

    path('log', av.log, name='log'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 2. Blockchain & Seller Logic

### # File: seller/models.py
```python
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_vehicle_number(value):
    if not re.fullmatch(r'[A-Z]{2}\d{2}[A-Z]{2}\d{4}', value):
        raise ValidationError("Invalid Vehicle Number format. Expected format: AP34DH5001")

class sellerRegisteredTable(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    loginid = models.CharField(max_length=30, unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=20, default='Active')
    location = models.CharField(max_length=255, null=True, blank=True)

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50, unique=True, validators=[validate_vehicle_number])
    seller_id = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    accidents_history = models.TextField(null=True, blank=True)
    ownership_documents = models.FileField(upload_to='documents/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255, null=True, blank=True)
    block_hash = models.CharField(max_length=66, null=True, blank=True)
    status = models.CharField(max_length=20, default='available')
```

### # File: seller/views.py (Blockchain Implementation)
```python
import hashlib
import json
import time

# Simple Blockchain Implementation for Vehicle Provenance
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        self.proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        self.proof_of_work(block)
        self.chain.append(block)

    def proof_of_work(self, block):
        while True:
            block.hash = block.compute_hash()
            if block.hash[:self.difficulty] == "0" * self.difficulty:
                break
            block.nonce += 1

# Initialize Global Blockchain instance
vehicle_blockchain = Blockchain()

def addVehicle(request):
    if request.method == 'POST':
        vehicle_number = request.POST.get('vehicle_number')
        price = request.POST.get('price')
        
        # ... validation ...

        # Create block for the new vehicle
        transaction_data = {
            'seller': request.session.get('name'),
            'vehicle_number': vehicle_number,
            'price': price,
            'timestamp': time.time()
        }
        
        block = Block(len(vehicle_blockchain.chain), [transaction_data], time.time(), vehicle_blockchain.chain[-1].hash)
        vehicle_blockchain.add_block(block)

        # Save to Database with Block Hash
        Vehicle.objects.create(
            vehicle_number=vehicle_number,
            price=price,
            block_hash=block.hash,
            status='available'
        )
        return redirect('sellerHome')
    return render(request, 'seller/addVehicle.html')
```

## 3. Buyer Logic & PDF Manipulation

### # File: Buyers/models.py
```python
class Transaction(models.Model):
    vehicle_number = models.CharField(max_length=50)
    buyer_id = models.IntegerField()
    seller_id = models.IntegerField(null=True, blank=True)
    buyer_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hash_code = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
```

### # File: Buyers/views.py (PDF Processing)
```python
import hashlib
import time
import os
import pdfplumber
from reportlab.pdfgen import canvas
from io import BytesIO

def purchase_vehicle(request):
    if request.method == 'POST':
        vehicle_number = request.POST.get('vehicle_number')
        buyer_name = request.session.get('name')

        # 1. Generate Transaction Hash (Pseudo-blockchain)
        raw_data = f"{vehicle_number}{time.time()}"
        block_hash = '0x' + hashlib.sha256(raw_data.encode()).hexdigest()

        # 2. Record Transaction
        Transaction.objects.create(
            buyer_name=buyer_name,
            vehicle_number=vehicle_number,
            hash_code=block_hash,
            status='pending'
        )

        # 3. Modify Ownership Documents (Neural PDF Processing)
        vehicle = Vehicle.objects.get(vehicle_number=vehicle_number)
        doc_path = vehicle.ownership_documents.path
        
        if os.path.exists(doc_path):
            output_dir = os.path.join(settings.MEDIA_ROOT, 'modified_pdfs')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"transferred_{vehicle_number}.pdf")

            with pdfplumber.open(doc_path) as pdf:
                buffer = BytesIO()
                c = canvas.Canvas(buffer)
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    lines = text.split('\n')
                    # Replace "Name:" field with new Buyer Name
                    new_lines = [f"Name: {buyer_name}" if l.startswith("Name:") else l for l in lines]
                    
                    # Redraw text in new PDF
                    t = c.beginText(40, 750)
                    for line in new_lines:
                        t.textLine(line)
                    c.drawText(t)
                    c.showPage()
                c.save()
                
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())

        return JsonResponse({'status': 'success', 'hash': block_hash})
```

## 4. Admin Management

### # File: Admin/views.py
```python
from django.shortcuts import render, redirect
from Buyers.models import Transaction
from seller.models import Vehicle

def adminApproveTransaction(request):
    hash_code = request.GET.get('hash_code')
    try:
        t = Transaction.objects.get(hash_code=hash_code)
        t.status = 'approved'
        t.save()

        # Finalize ownership transfer on "Blockchain" status
        v = Vehicle.objects.get(vehicle_number=t.vehicle_number)
        v.status = 'sold'
        v.save()
        
        messages.success(request, f'Transaction Approved: {hash_code[:10]}...')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('adminTransactions')
```
