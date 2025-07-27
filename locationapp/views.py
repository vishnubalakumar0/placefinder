from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from .models import CustomUser,ShopDb,CategoryDb,PlaceDb, Place_visited
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.urls import reverse
# Create your views here

def login_page(request):
    if request.method=="POST":
        u = request.POST.get('usname')
        ps = request.POST.get('pswd')
        user = authenticate(username=u,password=ps)
        if user:
            login(request,user)
            return redirect('home-page')
    return render(request,"login.html")


def homepage(request):
    data = ShopDb.objects.all()
    cat = CategoryDb.objects.all()
    place = PlaceDb.objects.all()
    catname =  request.GET.get('cname')
    locplace = request.GET.get('pname')
    if catname:
        data=data.filter(category_name=catname)
    if locplace:
        data=data.filter(place_id=locplace)
    return render(request,"home.html",{'data':data,'cat':cat,'place':place,'catname':catname,'locplace':locplace})


def register(request):
    if request.method=="POST":
        us = request.POST.get('usname')
        pa = request.POST.get('pswd')
        em = request.POST.get('email')
        if CustomUser.objects.filter(email=em).exists():
            messages.error(request,"email already exists")
        else:
            user=CustomUser.objects.create_user(username=us, password=pa, email=em)
            user.save()
            return redirect('login_page')
    return render(request, "register.html")



def shop_map(request,shop_id):
    shop=get_object_or_404(ShopDb,id=shop_id)
    return render(request,"shopmap.html",{'shop':shop})


@login_required
def place_visit(req):
    pla = PlaceDb.objects.all()
    cate = CategoryDb.objects.all()
    shop = ShopDb.objects.all()
    place_visits = Place_visited.objects.filter(user=req.user).order_by('-time')
    return render(req,"placevisited.html",{'place_visits':place_visits,'pla':pla,'cate':cate,'shop':shop})


@login_required
def visit(request):
    pla = PlaceDb.objects.all()
    cate = CategoryDb.objects.all()
    shop = ShopDb.objects.all()
    place_visits = Place_visited.objects.filter(user=request.user).order_by('-time')
    if request.method == "POST":
        u=request.user
        t = request.POST.get('time')
        c = request.POST.get('cname')
        p = request.POST.get('pname')
        s = request.POST.get('sname')
        pu = request.POST.get('pur')
        category_instance = CategoryDb.objects.get(categoryname=c)
        place_instance = PlaceDb.objects.get(place_name=p)
        shop_instance = ShopDb.objects.get(shop_name=s)
        obj = Place_visited(time=t, category=category_instance,place=place_instance,shop=shop_instance,
        purpose=pu,user=u)
        obj.save()
        place_visits = Place_visited.objects.filter(user=request.user).order_by('-time')
        return redirect(place_visit)
    return render(request,"placevisited.html",{'pla':pla,'shop':shop,'cate':cate,'place_visits':place_visits})
    
    
    
def speech_result(req):
    category = req.GET.get('categoryname')
    location = req.GET.get('place_name')
    return render(req,"visit.html",{'category':category,'location':location})


def forgot(req):
    return render(req, "forgot.html")

@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            print(email)
            if not email:
                return JsonResponse({'error':'email is required'},status=400)
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return JsonResponse({'message':'if email exists, a reset link been sent'})
            uid  = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://127.0.0.1:8000/locationapp/reset-password/{uid}/{token}/"
            send_mail(
            subject = "Reset your password",
            message = f"click the link to reset your password:{reset_url}",
            from_email = "aswachu20@gmail.com",
            recipient_list=[email],
            fail_silently=False,
            )
        except Exception as e:
            print(str(e))
        return JsonResponse({'message':'password reset link sent.'})
    return JsonResponse({'error':'Only POST allowed'},status=405)


@csrf_exempt
def reset_password(request,uidb64,token):
    if request.method =="POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            password = data.get('password')
        except:
            return JsonResponse({'error':'invalid data'},status=400)
        if not password:
            return JsonResponse({'error':'password is required'},status=400)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user  = CustomUser.objects.get(pk=uid)
        except:
            return JsonResponse({'error':'invalid reset link'},status=400)
        if not default_token_generator.check_token(user,token):
            return JsonResponse({'error':'invalid or expired tokenn'}, status=400)
        user.set_password(password)
        user.save()
        return JsonResponse({'message':'password has been reset successfully'})
    return JsonResponse({'error':'only POST allowed'}, status=405)


def reset(req,uidb64,token):
    return render(req,"reset.html",{'uidb64':uidb64,'token':token})