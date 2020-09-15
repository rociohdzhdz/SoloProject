from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.db.models import Q
from .models import User, Receipt
import bcrypt


# Create your views here.
def index(request):
    #return HttpResponse('placeholder to users reg')
    return render(request, "index.html")

def newuser(request):
    if request.method == "POST":
        errors=User.objects.validator(request.POST)
        print(errors)
        if len(errors)>0:
            for key, values in errors.items():
                messages.error(request,values)
            return redirect('/')
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user_userid=User.objects.filter(userid=request.POST['userid'])
        if len(new_user_userid)>0:
            return redirect('/userexist')
        new_user=User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['mail'],userid=request.POST['userid'],country=request.POST['country'],tpin=request.POST['tpin'],usertype=request.POST['usert'],storename=request.POST['storen'],password=pw_hash)
        print(new_user)
        request.session['usrname']=new_user.first_name + " " + new_user.last_name
        request.session['usr_id']=new_user.id
        request.session['user_name']=new_user.userid
        request.session['user_type']=new_user.usertype
        if new_user.usertype =="user":
            return redirect(f'/userhome/{str(new_user.id)}')
        if new_user.usertype =="store":
            return redirect(f'/storehome/{str(new_user.id)}')
    return redirect('/')

def userexist(request):
    return render(request, "UserExist.html")

def userhome(request,id):
    if 'usrname' not in request.session:
        return redirect('/')
    x=User.objects.get(id=id)
    qs= Receipt.objects.all()
    print(x)
    y=x.userid
    u=request.session['usr_id']
    print(f'user_id{u}')
    if x !='':
        qs=qs.filter(recfromuser__icontains=y)
        context={
            'queryset':qs
        }   
        return render(request, "userhome.html",context)

def storehome(request,id):
    if 'usrname' not in request.session:
        return redirect('/')
    return render(request, "storehome.html")

def loginuser(request):
    if request.method == "POST":
        loggedusr=User.objects.filter(userid=request.POST['loguserid'])
        print(User.objects.all())
        if len(loggedusr)>0:
            loggedusr=loggedusr[0]
            if bcrypt.checkpw(request.POST['logpass'].encode(), loggedusr.password.encode()):
                request.session['usrname']=loggedusr.first_name +" " + loggedusr.last_name
                request.session['usr_id']=loggedusr.id
                request.session['user_name']=loggedusr.userid
                request.session['user_type']=loggedusr.usertype
                print(loggedusr.usertype)
                if loggedusr.usertype =="user":
                    return redirect(f'/userhome/{loggedusr.id}')
                if loggedusr.usertype =="store":
                    return redirect(f'/storehome/{loggedusr.id}')
    return redirect('/')

def myaccount(request,id):
    oneprofile=User.objects.get(id=id)
    if request.method == "POST":
        if request.POST['editfname'] == "" or request.POST['editlname'] == "" or request.POST['editmail']=="":
            return redirect('/errorprofile')
        oneprofile.first_name=request.POST['editfname']
        oneprofile.last_name=request.POST['editlname']
        oneprofile.email=request.POST['editmail']
        oneprofile.country=request.POST['editcountry']
        oneprofile.tpin=request.POST['editaxid']
        oneprofile.save()
        #return redirect(f'/user/{str(oneprofile.id)}')
    context={
        'editprofile': oneprofile
    }
    return render(request, "Editmyaccount.html", context)

def newreceipt(request):
    u=request.session['usr_id']
    print(f'user_id{u}')
    if request.method == "POST":
        #errors validation 
        errors=Receipt.objects.validator(request.POST)
        print(errors)
        if len(errors)>0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect(f'/userhome/{u}')
        new_receipt=Receipt.objects.create(category=request.POST['category'],amount=request.POST['amount'],recfromuser=request.session['user_name'],creator=User.objects.get(id=request.session['usr_id']))
        print(new_receipt)
        return redirect(f'/userhome/{u}')
    return redirect('/')

def newreceiptstore(request):
    if request.method == "POST":
        u=request.session['usr_id']
        print(f'user_id{u}')
        errors=Receipt.objects.validator(request.POST)
        print(errors)
        if len(errors)>0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect(f'/storehome/{str(u)}')
        #loggredusr=User.objects.filter(userid=request.POST['loguserid'])
        
        #request.session['usr_id']=loggedusr.id
        #request.session['user_name']=loggedusr.userid
        #request.session['user_type']=loggedusr.usertype
        new_receiptstore=Receipt.objects.create(category=request.POST['category'],amount=request.POST['amount'],recfromuser=request.POST['useridstore'],creator=User.objects.get(id=u))
        print(new_receiptstore.creator.first_name)
        return redirect(f'/storehome/{str(u)}')
    return redirect('/')

def searchreceiptstore(request):
    if 'usrname' not in request.session:
        return redirect('/')
    userqry=request.GET.get('useridsearch')
    dateqry=request.GET.get('datesearch')
    print(userqry)
    qsst= Receipt.objects.all()
    u=request.session['usr_id']
    print(f'user_id{u}')
    if userqry !='' and userqry is not None:
        qsst=qsst.filter(Q(recfromuser__icontains=userqry) & Q(creator=u))
    if dateqry !='' and dateqry is not None:
        qsst=qsst.filter(Q(created_at__icontains=dateqry) & Q(creator=u))
        context={
            'querysetstore':qsst
        }   
        return render(request, "storesearch.html",context)

def delete(request,id):
    u=request.session['usr_id']
    print(f'user_id{u}')
    Receipt.objects.get(id=id).delete()
    return redirect (f'/userhome/{str(u)}')

def logout(request):
    request.session.flush()
    return redirect('/')