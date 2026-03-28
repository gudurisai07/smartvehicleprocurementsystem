


from django.shortcuts import render


def index(request):
    return render(request,'index.html')

def userRegisterForm(request):
    return render(request,'userRegisterForm.html')

def userLoginForm(request):
    return render(request,'userLoginForm.html')

def adminLoginForm(request):
    from django.shortcuts import redirect
    return redirect('adminHome')