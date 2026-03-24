from django.shortcuts import render
from django.views.decorators.cache import cache_control
# Create your views here.
from django.shortcuts import render
from django.contrib import messages
from  seller.models import sellerRegisteredTable
from Buyers.models import userRegisteredTable


from Buyers.models import Transaction
from seller.models import Vehicle

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def adminHome(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html')  
    
    total_users = userRegisteredTable.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_transactions = Transaction.objects.count()
    
    return render(request, 'admin/adminHome.html', {
        'total_users': total_users,
        'total_vehicles': total_vehicles,
        'total_transactions': total_transactions
    })

def adminTransactions(request):
    if not request.session.get('admin'):
        return render(request, 'adminLoginForm.html')
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'admin/adminTransactions.html', {'transactions': transactions})

from django.shortcuts import redirect

def adminApproveTransaction(request):
    if not request.session.get('admin'):
        return redirect('adminLoginForm')

    hash_code = request.GET.get('hash_code', '').strip()
    if not hash_code:
        messages.error(request, 'No hash code provided. Please paste a valid blockchain hash.')
        return redirect('adminTransactions')

    try:
        from Buyers.models import Transaction
        t = Transaction.objects.get(hash_code=hash_code)

        if t.status == 'approved':
            messages.error(request, f'Transaction {hash_code[:20]}... is already approved.')
            return redirect('adminTransactions')

        # Approve transaction
        t.status = 'approved'
        t.save()

        # Update Vehicle status to sold (seller vehicle)
        try:
            vehicle = Vehicle.objects.get(vehicle_number=t.vehicle_number)
            vehicle.status = 'sold'
            vehicle.save()
        except Exception:
            pass  # Vehicle might not exist in seller model

        # Update Vehicle1 status (buyer-facing vehicle)
        try:
            from Buyers.models import Vehicle1
            vehicle1 = Vehicle1.objects.get(vehicle_number=t.vehicle_number)
            vehicle1.status = 'sold'
            vehicle1.save()
        except Exception:
            pass

        messages.success(request, f'Transaction APPROVED! Vehicle {t.vehicle_number} ownership transferred to {t.buyer_name}.')

    except Transaction.DoesNotExist:
        messages.error(request, f'No pending transaction found for hash: {hash_code[:30]}...')
    except Exception as e:
        messages.error(request, f'Verification failed: {str(e)}')

    return redirect('adminTransactions')


def adminLoginCheck(request):
    if request.method=="POST":
        username=request.POST['loginid']
        adminPassword=request.POST['password']

        if adminPassword=="admin" and username=='admin':
            request.session['admin']=True
            from django.shortcuts import redirect
            return redirect('adminHome')
        else:
            messages.error(request,'Invalid details')
            return render(request,'adminLoginForm.html')
    else:
        return render(request,'adminLoginForm.html')
    

def userList(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})


def log(request):
    request.session.flush()  # clears all session data
    return render(request,'index.html')


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def activate_user(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 

    id=request.GET['id']
    user = get_object_or_404(userRegisteredTable, id=id)
    user.status = 'Active'
    user.save()
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})  

def deactivate_user(request):
    if not request.session.get('admin'):
        return render(request,'adminLoginForm.html') 
    
    id=request.GET['id']
    user = get_object_or_404(userRegisteredTable, id=id)
    user.status = 'Inactive'
    user.save()
    users=userRegisteredTable.objects.all()
    return render(request,'admin/userList.html',{'users':users})
