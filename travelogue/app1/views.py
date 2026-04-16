from django.shortcuts import render,redirect,HttpResponse # type: ignore
from django.contrib.auth import authenticate # type: ignore
from .models import *
from django.shortcuts import HttpResponseRedirect # type: ignore
from django.db.models import Q, Sum  # type: ignore
from django.contrib import messages # type: ignore
from datetime import date as d, datetime as dt

# Create your views here.
def index(request):
    return render(request,"index.html")

def login(request):
    if request.POST:
        email=request.POST['email']
        password=request.POST['password']
        # print(username,"##",password)
        user=authenticate(username=email,password=password)
        # print(user.id)
        if user is not None:
            # login(request,user)
            if user.usertype=='admin':
                id=user.id
                request.session['uid']=id
                request.session['type']='admin'
                messages.info(request,"login successfully")
                return redirect('/adminindex')
            elif user.usertype=='user':
                id=user.id
                request.session['uid']=id
                request.session['type']='user'
                messages.info(request,"login successfully")
                return redirect('/userindex')
            elif user.usertype=='shop':
                id=user.id
                request.session['uid']=id
                request.session['type']='shop'
                messages.info(request,"login successfully")
                return redirect('/shopindex')
            elif user.usertype=='club':
                id=user.id
                request.session['uid']=id
                request.session['type']='club'
                messages.info(request,"login successfully")
                return redirect('/clubindex')           
        else:
                messages.info(request,"login failed.Please enter correct email and password")
                return redirect('/login')
    return render(request,'login.html')

# def contact(request):
#     return render(request,"contact.html")

# def galleryclub(request):
#     post=Posts.objects.all()
#     return render(request,"club/galleryclub.html",{"post":post})


def galleryuser(request):
    post=Posts.objects.all()
    return render(request,"user/galleryuser.html",{"post":post})


# def galleryadmin(request):
#     post=Posts.objects.all()
#     return render(request,"admin/galleryadmin.html",{"post":post})

# def about(request):
#     return render(request,"about.html")
def services(request):
    return render(request,"services.html")
def typo(request):
    return render(request,"typo.html")

def register_user(request):
    if request.POST:
        uname=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        rname=request.POST["ridername"]
        DOB=request.POST["DOB"]
        # gender=request.POST["gender"]
        phonenumber=request.POST["phonenumber"]
        address=request.POST["address"]
        loguser=Login.objects.create_user(usertype="user",viewpassword=password,username=email,password=password)
        loguser.save()
        # user_login is the foreign key it should required for login to identify each user
        reguser=Register_user.objects.create(user_login=loguser,username=uname,email=email,DOB=DOB,address=address,phonenumber=phonenumber,ridername=rname)
        reguser.save()
        messages.info(request,"registered successfully")
        return HttpResponseRedirect('/login')
    return render(request,'register_user.html')


def register_club(request):
    if request.method == "POST":
        uname = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        clubname = request.POST["clubname"]
        phoneNum = request.POST["phoneNum"]
        location = request.POST["location"]
        image = request.FILES.get("image")  # important

        # Create login user
        logclub = Login.objects.create_user(
            usertype="club",
            viewpassword=password,
            password=password,
            username=email,
            is_active=0
        )
        logclub.save()

        # Create club record
        regclub = Register_club(
            user_login=logclub,
            username=uname,
            email=email,
            clubname=clubname,
            location=location,
            phonenumber=phoneNum
        )
        if image:
            regclub.image = image  # assign the uploaded file
        regclub.save()

        messages.success(request, "Registered successfully!")
        return HttpResponseRedirect('/login')

    return render(request, "register_club.html")


def register_shop(request):
    if request.POST:
        uname=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        shopname=request.POST["shopname"]
        phonenumber=request.POST["phonenumber"]
        location=request.POST["location"]
        logshop=Login.objects.create_user(usertype="shop",viewpassword=password,password=password,username=email,is_active=0)
        logshop.save()
        regshop=Register_shop.objects.create(user_login=logshop,username=uname,email=email,shopname=shopname,location=location,phonenumber=phonenumber)
        regshop.save()
        messages.info(request,"registered successfully")
        return HttpResponseRedirect('/login')
    return render(request,"register_shop.html")

def shopapprove(request):
    shop=Register_shop.objects.all()
    return render(request,"admin/shopapprove.html",{"shop":shop})

def clubapprove(request):
    club=Register_club.objects.all()
    return render(request,"admin/clubapprove.html",{"club":club})

def acceptapproval(request):
    status=request.GET['status']
    id=request.GET.get('id')

    if status=='1':
        # Approve: activate the login account
        Login.objects.filter(id=id).update(is_active=1, usertype='club')
        messages.success(request,'Club approved successfully')
    elif status=='0':
        # Reject pending club: delete the login user (cascades to register_club)
        try:
            Login.objects.filter(id=id).delete()
            messages.warning(request,'Club registration rejected and deleted')
        except Exception as e:
            messages.error(request, f'Error deleting club: {e}')
    elif status=='block':
        # Block an approved club
        Login.objects.filter(id=id).update(is_active=0, usertype='blocked_club')
        messages.info(request,'Club blocked')
    elif status=='unblock':
        # Unblock a blocked club
        Login.objects.filter(id=id).update(is_active=1, usertype='club')
        messages.info(request,'Club unblocked')
    return HttpResponseRedirect('/clubapprove')


def acceptapprovalshop(request):
    status=request.GET['status']
    id=request.GET.get('id')

    if status=='1':
        # Approve: activate the login account
        Login.objects.filter(id=id).update(is_active=1, usertype='shop')
        messages.success(request,'Shop approved successfully')
    elif status=='0':
        # Reject pending shop: delete the login user (cascades to register_shop)
        try:
            Login.objects.filter(id=id).delete()
            messages.warning(request,'Shop registration rejected and deleted')
        except Exception as e:
            messages.error(request, f'Error deleting shop: {e}')
    elif status=='block':
        # Block an approved shop
        Login.objects.filter(id=id).update(is_active=0, usertype='blocked_shop')
        messages.info(request,'Shop blocked')
    elif status=='unblock':
        # Unblock a blocked shop
        Login.objects.filter(id=id).update(is_active=1, usertype='shop')
        messages.info(request,'Shop unblocked')
    return HttpResponseRedirect('/shopapprove')
                                             

def commonpage(request):
    return render(request,"commonpage.html")
def userindex(request):
    return render(request,"user/userindex.html")
def adminindex(request):
    return render(request,"admin/adminindex.html")
def shopindex(request):
    return render(request,"shop/shopindex.html")
def clubindex(request):
    return render(request,"club/clubindex.html")


def add_pdt_sell(request):
    uid=request.session["uid"]
    shop=Register_shop.objects.get(user_login=uid)
    if request.POST:
        productname=request.POST["productname"]
        price=request.POST["price"]
        image=request.FILES["image"]
        stock=request.POST["stock"]
        addpdt=Product_sell.objects.create(shop_name_id=shop.id,productname=productname,price=price,images=image,stock=stock)
        addpdt.save()
        messages.info(request,"product added successfully")
        return redirect("/viewsalepdt")
    return render(request,"shop/add_pdt_sell.html")

def add_pdt_rent(request):
    uid=request.session["uid"]
    club=Register_club.objects.get(user_login=uid)
    if request.POST:
        bikename=request.POST["bikename"]
        rent=request.POST["rent"]
        img=request.FILES['image']
        addpdt=Product_rent.objects.create(club_name_id=club.id,productname=bikename,rent=rent,images=img)
        addpdt.save()
        messages.info(request,"product added successfully")
        return redirect("/viewrentpdt")
    return render(request,"club/add_pdt_rent.html")

def shopping(request):   
    buycart = Product_sell.objects.filter(stock__gt=0)
    return render(request,'user/shopping.html',{"buycart":buycart})
    
def add_shopcart(request):
    uid = request.session['uid']
    id = request.GET['id']
    pdt=Product_sell.objects.filter(id=id)
    user=Register_user.objects.get(user_login=uid)
    if request.POST:
        quantity=request.POST["qty"]
        print(quantity)
        pdtt=Product_sell.objects.get(id=id)
        price = int(pdtt.price)
        total_c=price * int(quantity)
        order, created = Shoporder.objects.get_or_create(user_login= user, status='pending', defaults={'total': 0})
        order.total += int(total_c)
        order.save()
        cart_product = Shopcart.objects.filter( product=pdtt, order=order).first()
        if Shopcart.objects.filter(product=pdtt, order__user_login_id=user.id,status='pending').exists():
            message="already in cart"
            messages.info(request,message)
        elif cart_product:
            cart_product.quantity += int(quantity)
            cart_product.total += total_c
            cart_product.save()
        else:        
            cart = Shopcart.objects.create(product=pdtt, order=order, quantity = quantity, total = total_c)
            cart.save()
            message="item added to cart"
            messages.info(request,message)
            return redirect("/shopcart",{"message":messages.get_messages(request)})
    return render(request,'user/shoppdt.html',{"pdt":pdt})

def shopcart(request):
    uid = request.session['uid']
    oid=""
    user = Register_user.objects.get(user_login=uid)
    # print(user)
    buycart=Shopcart.objects.filter(order__user_login=user ,status="pending")
    try:
        order=Shoporder.objects.get(user_login=user, status = "pending")
        oid=order.id
    except:
        order=None
    print(order)
    print(buycart,"ioioioioppppppp")
    return render(request, 'user/shopcart.html',{"buycart":buycart,"oid":oid, "order":order})

def deleteshopcart(request):
    id=request.GET.get("id")
    cart_item = Shopcart.objects.get(id=id)    
    order = Shoporder.objects.get(user_login=cart_item.order.user_login, status='pending')
    order.total -= cart_item.total
    order.save()
    cart_item.delete()
    messages.info(request,"Item deleted successfully")
    return redirect("/shopcart")

def shoppayment(request):
    uid = request.session['uid']
    user = Register_user.objects.get(user_login=uid)
    
    order_id = request.GET.get('id')
    cart_ids_str = request.GET.get('cart_ids')
    
    order = Shoporder.objects.get(id=order_id)
    
    selected_carts = None
    display_total = order.total
    
    if cart_ids_str:
        cart_ids = cart_ids_str.split(',')
        selected_carts = Shopcart.objects.filter(id__in=cart_ids, order=order)
        display_total = sum(item.total for item in selected_carts)

    if request.POST:
        if selected_carts:
            for c in selected_carts:
                product = c.product
                product.stock -= c.quantity
                product.save()
                c.status = "paid"
                c.save()
            # If no more pending items in this order, mark order as paid
            if not Shopcart.objects.filter(order=order, status="pending").exists():
                order.status = "paid"
                order.save()
        else:
            # Pay entire order
            order.status = "paid"
            carts = Shopcart.objects.filter(order=order)
            for c in carts:
                product = c.product
                product.stock -= c.quantity
                product.save()
                c.status = "paid"
                c.save()
            order.save()
            
        messages.info(request, "Paid successfully")
        return redirect("/purchasehistory")
        
    context_order = {'total': display_total, 'id': order.id}
    return render(request, "user/payment.html", {"order": context_order})

def rent(request):
    rentcart=Product_rent.objects.all()
    return render(request,'user/rent.html',{"rentcart":rentcart})

def add_rentcart(request):
    uid = request.session['uid']
    id = request.GET['id']
    pdtt=Product_rent.objects.filter(id=id)
    user=Register_user.objects.get(user_login=uid)
    pdt=Product_rent.objects.get(id=id)
    if request.POST:
        rentdate=request.POST["rentdate"]
        returndate=request.POST["returndate"]
        if 'file' not in request.FILES:
            messages.error(request, "Please upload ID proof file")
            return redirect(f"/add_rentcart/?id={id}")
        file=request.FILES["file"]
        pdtt=Product_rent.objects.get(id=id)
        rent = int(pdtt.rent)
        available=Rentcart.objects.filter(product=pdt,rented_date__lte=rentdate,return_date__gte=rentdate) |\
                  Rentcart.objects.filter(product=pdt,rented_date__lte=returndate,return_date__gte=returndate)
        if available.exists():
            message="item not available on requested date"
            messages.info(request,message)
        else:
            if rentdate and returndate:  # Check if the date values are not empty
                try:
                    sdate = dt.strptime(rentdate, "%Y-%m-%d")
                    edate = dt.strptime(returndate, "%Y-%m-%d")
                except ValueError:
                    message = "Invalid date format"
                    messages.error(request, message)
                    return redirect(f"/add_rentcart/?id={id}")
            else:
                messages.error(request, "Please enter both dates")
                return redirect(f"/add_rentcart/?id={id}")
            
            date_diff = edate - sdate
            print("date_diff", date_diff)
            if date_diff.days <= 0:
                total_c = (int(rent))
            else:
                total_c = int(date_diff.days) * (int(rent))
            
            # Use status='requested' for initial order
            order, created = Rentorder.objects.get_or_create(user_login= user, status='requested',file=file, defaults={'total': 0})
            order.total = int(order.total) + int(total_c)
            order.save()    
            pdtid=pdtt.id
            oid=order.id
            print(order.id)
            try:
                if Rentcart.objects.filter(product_id=pdtid, order_id=oid).exists():
                    cart_product = Rentcart.objects.get(product_id=pdtid, order_id=oid)
                    cart_product.rented_date=rentdate
                    cart_product.return_date=returndate
                    cart_product.days=date_diff.days
                    cart_product.total = int(total_c)
                    cart_product.save()
                else:
                    cart = Rentcart.objects.create(product=pdtt, order=order, rented_date = rentdate, return_date=returndate,days=date_diff.days if date_diff.days > 0 else 1, total = total_c)
                    cart.save()  
            except Exception as e:
                   print(e)
                   cart = Rentcart.objects.create(product=pdtt, order=order, rented_date = rentdate, return_date=returndate,days=date_diff.days if date_diff.days > 0 else 1, total = total_c)
                   cart.save()    
            message="Rental request sent to club for approval"
            messages.info(request,message)
        return redirect("/rentcart")
    return render(request,'user/rentpdt.html',{"pdtt":pdtt})

def rentcart(request):
    uid = request.session['uid']
    oid=""
    user = Register_user.objects.get(user_login=uid)
    # Only show active (non-completed) cart items
    cart=Rentcart.objects.filter(order__user_login=user).exclude(status__in=["paid", "delivered"])
    try:
        # Get active order (not paid yet)
        order=Rentorder.objects.filter(user_login=user).exclude(status__in=["paid", "delivered"]).last()
        if order:
            oid=order.id
        else:
            order=None
    except:
        order=None
    return render(request, 'user/rentcart.html',{"cart":cart,"oid":oid, "order":order})

def deleterentcart(request):
    id=request.GET.get("id")
    cart_item = Rentcart.objects.get(id=id)
    order = cart_item.order  # Get the associated Rentorder
    order.total -= cart_item.total  # Subtract the item's total from the order's total
    order.save()  # Save the updated order

    cart_item.delete() 
    messages.info(request,"Item deleted successfully")
    return redirect("/rentcart")

def rentpayment(request):
    uid = request.session['uid']
    user = Register_user.objects.get(user_login=uid)
    
    order_id = request.GET.get('id')
    cart_ids_str = request.GET.get('cart_ids')
    
    try:
        order = Rentorder.objects.get(id=order_id)
    except Rentorder.DoesNotExist:
        messages.error(request, "Order not found")
        return redirect("/rentcart")

    selected_carts = None
    display_total = order.total
    
    if cart_ids_str:
        cart_ids = cart_ids_str.split(',')
        selected_carts = Rentcart.objects.filter(id__in=cart_ids, order=order, status="approved")
        if not selected_carts.exists():
            messages.error(request, "No approved items selected for payment")
            return redirect("/rentcart")
        display_total = sum(item.total for item in selected_carts)
    else:
        # If no specific items, we assume full order payment but only if order is approved
        if order.status != "approved":
            messages.error(request, "Order must be approved by the club before payment")
            return redirect("/rentcart")

    if request.POST:
        if selected_carts:
            for c in selected_carts:
                c.status = "paid"
                c.save()
            # If no more non-paid items in this order, mark order as paid
            if not Rentcart.objects.filter(order=order).exclude(status__in=["paid", "delivered"]).exists():
                order.status = "paid"
                order.save()
        else:
            # Pay entire order
            order.status = "paid"
            carts = Rentcart.objects.filter(order=order)
            for c in carts:
                c.status = "paid"
                c.save()
            order.save()
            
        messages.info(request, "Paid successfully")
        return redirect("/renthistory")
        
    context_order = {'total': display_total, 'id': order.id}
    return render(request, "user/rentpayment.html", {"order": context_order})

def approverent(request):
    uid=request.session["uid"]
    club=Register_club.objects.get(user_login=uid)
    # Find orders that contain products from this club and are requested
    orders = Rentorder.objects.filter(rentcart__product__club_name=club, status="requested").distinct()
    return render(request,"club/approverent.html",{"orders":orders})

def acceptrent(request):
    id=request.GET.get('id')
    order=Rentorder.objects.get(id=id)
    order.status = "approved"
    order.save()
    # Also update status in Rentcart items
    Rentcart.objects.filter(order=order).update(status="approved")
    messages.info(request,'Approved successfuly')
    return redirect('/approverent')

def rejectrent(request):
    id=request.GET.get('id')
    order=Rentorder.objects.get(id=id)
    order.status = "rejected"
    order.save()
    Rentcart.objects.filter(order=order).update(status="rejected")
    messages.info(request,'Rejected successfuly')
    return redirect('/approverent')

def renttt(request):
    return redirect("/")

def userprofile(request):
    uid = request.session['uid']
    user = Register_user.objects.filter(user_login=uid)
    return render (request,"user/userprofile.html",{"user":user})

def clubuser(request):
    uid = request.session['uid']
    clb=Register_club.objects.get(user_login=uid)
    print(clb)
    club = Register_club.objects.filter(user_login=uid)
    post=Posts.objects.filter(club_login=clb)
    artcle=Article.objects.filter(club_login=clb)
    print(artcle)
    return render(request,"club/clubuser.html",{"club":club,"post":post,"artcle":artcle})



def editclub(request):
    uid = request.session['uid']
    user = Register_club.objects.get(user_login=uid)
    if request.POST:
        user.username = request.POST["username"]
        user.clubname = request.POST["clubname"]
        user.phonenumber = request.POST["phoneNum"]
        user.location = request.POST["location"]
        if 'image' in request.FILES:
            user.image = request.FILES["image"]
        user.save()
        messages.info(request, "Profile updated successfully")
        return redirect('/clubuser')
    return render(request, "club/editclub.html", {"user": user})

def postimage(request):
    uid = request.session['uid']
    club = Register_club.objects.get(user_login=uid)
    if request.POST:
        photo=request.FILES.get("photo")
        post=Posts.objects.create(images=photo,club_login=club)
        messages.info(request,"Photo posted successfully")
        return redirect('/clubuser')
    return render(request,"club/postimage.html")

def clubbu(request):
    clb=Register_club.objects.all()
    return render(request,"club/clubbu.html",{"clb":clb})
def clubclub(request):
    # id is passed as the name"clubname
    club=request.GET.get('name')
    print(club)
    uid=request.session['uid']

    clbs=Register_club.objects.get(id=club)
    clb=Register_club.objects.filter(id=club)
    post=Posts.objects.filter(club_login=clbs)
    artcle=Article.objects.filter(club_login=clbs)
        
    return render(request,"club/clubclub.html",{"clb":clb,"post":post,"artcle":artcle})


def postarticle(request):
    uid = request.session['uid']
    club = Register_club.objects.get(user_login=uid)
    if request.POST:
        hd=request.POST["articlename"]
        art=request.POST["article"]
        post=Article.objects.create(articlename=hd,articles=art,club_login=club)
        messages.info(request,"Article posted successfully")
        return redirect('/clubuser')
    return render(request,"club/postarticle.html")

def article(request):
    id=request.GET.get("id")
    artcle=Article.objects.filter(id=id)
    return render(request,"club/article.html",{"artcle":artcle})


def articleadmin(request):
    id=request.GET.get("id")
    artcle=Article.objects.filter(id=id)
    return render(request,"admin/articleadmin.html",{"artcle":artcle})


def articleuser(request):
    id=request.GET.get("id")
    artcle=Article.objects.filter(id=id)
    return render(request,"user/articleuser.html",{"artcle":artcle})

def clubview(request):
    # id is passed as the name"clubname
    club=request.GET.get('name')
    print(club)
    uid=request.session['uid']
    # pid=request.GET.get('id')
    uuid=Register_user.objects.get(user_login=uid)

    clbs=Register_club.objects.get(id=club)
    clb=Register_club.objects.filter(id=club)
    post=Posts.objects.filter(club_login=clbs)
    artcle=Article.objects.filter(club_login=clbs)
    reqq=Requests.objects.filter(user_login=uuid,club_name=clbs.id)
    if request.POST:
        # request=request.POST["rqst"]
        club=Register_club.objects.get(id=club)
        req=Requests.objects.create(user_login=uuid,club_name=club,status = "Join request sent")
        req.save()        
    return render(request,"user/clubview.html",{"clb":clb,"post":post,"artcle":artcle,"reqq":reqq})

def clubs(request):
    clb=Register_club.objects.all()
    return render(request,"user/clubs.html",{"clb":clb})

def joinrqst(request):
    req=""
    uid=request.GET.get('user')
    clb_id = request.GET.get('clubname')
    if request.POST:
        request=request.POST["rqst"]
        uuid=Register_user.objects.get(user_login=uid)
        club=Register_club.objects.get(id=clb_id)
        req=Requests.objects.create(user_login=uuid,club_name=club)
        req.save()

    return render(request,"user/joinrqst.html",{"req":req})

def viewrqst(request):
    uid=request.session["uid"]
    club=Register_club.objects.get(user_login=uid)
    req=Requests.objects.filter(club_name=club.id,status="Join request sent")
    return render(request,"club/viewrqst.html",{"req":req})

def rejectrqst(request):
    id=request.GET.get('id')  
    req=Requests.objects.get(id=id)
    req.status = "Request rejected"
    req.save()
    return redirect("/viewrqst")

def acceptrqst(request):
    id=request.GET.get('id')
    print(id)
    req=Requests.objects.get(id=id)
    print(req)  
    req.status = "Joined as a member"
    req.save()
        # req=Requests.objects.get(id=id).delete()
    return redirect("/viewrqst")
    
def addevent(request):
    uid = request.session['uid']  
    clu=Register_club.objects.get(user_login_id__id=uid)
    if request.POST:
        eventname=request.POST["eventname"]
        s_loc=request.POST['startlocation']
        destination=request.POST['destination']
        date=request.POST['date']
        estimatedcost=request.POST["estimatedcost"]
        route=request.POST["route"]
        evnt=Events.objects.create(club_id=clu,date=date,name=eventname,starting_location=s_loc,destination=destination,estimated_cost=estimatedcost,route=route)
        evnt.save()
        message = "event added successfully."
        messages.info(request, message)
        return redirect("/addevent")
    return render(request,"club/addevent.html")

def editevents(request):
    uid=request.session["uid"]
    clb=Register_club.objects.get(user_login=uid)
    evnt=Events.objects.filter(club_id=clb)
    return render(request,"club/editevents.html",{"evnt":evnt})

def editevents2(request):
    uid=request.session["uid"]
    clb=Register_club.objects.get(user_login=uid)
    evnt=Events.objects.filter(club_id=clb)
    id=request.GET.get("id")
    event=Events.objects.get(id=id)
    if request.POST:
        name=request.POST["event"]
        sloc=request.POST["startlocation"]
        des=request.POST["destination"]
        cost=request.POST["estimatedcost"]
        date=request.POST["date"]
        edit=Events.objects.filter(id=event.id).update(name=name,starting_location=sloc,destination=des,estimated_cost=cost,date=date)
        message = "event updated successfully."
        messages.info(request, message)
        return redirect("/editevents")
    return render(request,"club/editevents2.html",{"evnt":evnt,"event":event})

def deleteevents(request):
    id=request.GET.get("id")
    evnt=Events.objects.get(id=id).delete()
    message = "event deleted successfully."
    messages.info(request, message)
    return redirect("/editevents")

def eventadmin(request):
    evnt=Events.objects.all()
    return render(request,"admin/eventadmin.html",{"evnt":evnt})

from datetime import date, datetime  # Import required modules
from django.shortcuts import get_object_or_404 # type: ignore

def eventuser(request):
    uid=request.session["uid"]
    user=Register_user.objects.get(user_login=uid)
    evnt=Events.objects.all()
    # Get participation status for each event for the current user
    participations = Participate.objects.filter(user_id=user.id)
    par_dict = {p.event_id: p.status for p in participations}
    for e in evnt:
        e.participation_status = par_dict.get(e.id)
    today = date.today()
    return render(request,"user/eventuser.html",{"evnt":evnt,"today":today})

def joinevent(request):
    uid=request.session["uid"]
    user=Register_user.objects.get(user_login=uid)
    id=request.GET.get("id")
    evnt=Events.objects.get(id=id)
    if Participate.objects.filter(user_id=user.id, event_id=evnt.id).exists():
        message = "You have already joined this event."
        messages.info(request, message)
    else:
        participate = Participate.objects.create(user_id=user.id, event_id=evnt.id, status="requested to join")
        message = "Request sent to join event."
        messages.info(request, message)
    return redirect("/eventuser")  


def editprofile(request):
    uid = request.session['uid']
    user = Register_user.objects.get(user_login=uid)
    if request.POST:
        user.username = request.POST["username"]
        user.phonenumber = request.POST["phonenumber"]
        user.address = request.POST["address"]
        if 'dp' in request.FILES:
            user.images = request.FILES["dp"]
        user.save()
        messages.info(request, "Profile edited successfully")
        return redirect("/userprofile")
    return render(request, "user/editprofile.html", {"data": user})

def clubsadmin(request):
    clb=Register_club.objects.all()
    return render(request,"admin/clubsadmin.html",{"clb":clb})


def memberships(request):
    id=request.GET.get("id")
    club=Register_club.objects.get(id=id)
    print(club)
    mem=Requests.objects.filter(club_name=club.id,status="Joined as a member")
    return render(request,"admin/memberships.html",{"mem":mem})


def clubviewadmin(request):
    # id is passed as the name"clubname
    club=request.GET.get('name')
    print(club)
    uid=request.session['uid']
    # pid=request.GET.get('id')
    clbs=Register_club.objects.filter(id=club)
    clb=Register_club.objects.filter(id=club)
    post=Posts.objects.filter(club_login=clbs)
    artcle=Article.objects.filter(club_login=clbs)  
    return render(request,"admin/clubviewadmin.html",{"clb":clb,"post":post,"artcle":artcle})

def removeclub(request):
    club=request.GET.get('name')
    print(club)
    clb=Register_club.objects.get(id=club).delete()
    messages.info(request,"club removed")
    return redirect("/clubsadmin")

def purchasehistory(request):
    uid=request.session['uid']
    user=Register_user.objects.get(user_login=uid)
    # Only show items that are paid or delivered (completed)
    buycart=Shopcart.objects.filter(status__in=["paid","delivered"],order__user_login=user).order_by('-id')
    return render(request,"user/purchasehistory.html",{"buycart":buycart})

def renthistory(request):
    uid=request.session['uid']
    user=Register_user.objects.get(user_login=uid)
    rentcart=Rentcart.objects.filter(
        status__in=["paid", "delivered"],
        order__user_login=user
    ).order_by('-id')
    today = d.today().strftime('%Y-%m-%d')
    return render(request,"user/renthistory.html",{"rentcart":rentcart, "today": today})

def renthistoryclub(request):
    uid=request.session['uid']
    user=Register_club.objects.get(user_login=uid)
    rentcart=Rentcart.objects.filter(status="paid",order_id__club_login_id=user.id)
    return render(request,"club/renthistoryclub.html",{"rentcart":rentcart})

def purchasehistoryclub(request):
    uid=request.session['uid']
    user=Register_club.objects.get(user_login=uid)
    buycart=Shopcart.objects.filter(status="paid",order_id__club_login_id=user.id)
    return render(request,"club/purchasehistoryclub.html",{"buycart":buycart})

def viewrentpdt(request):
    uid=request.session['uid']
    club=Register_club.objects.get(user_login=uid)
    # id=request.GET.get("id")
    if request.POST:
        id = request.POST['ID']
        print(id)
        bikename=request.POST.get("bikename")
        rent=request.POST.get("rent")
        item=Product_rent.objects.get(id=id)
        if 'image' in request.FILES:
            image=request.FILES["image"]
        else:
            image=item.images
        stock=request.POST.get("stock")

        item.productname=bikename
        item.rent=rent
        item.images=image
        item.save()
        messages.info(request,"updated successfully")
        # return HttpResponseRedirect('/viewsalepdt')
    rent=Product_rent.objects.filter(club_name_id=club)
    return render(request,"club/viewrentpdt.html",{"rent":rent})

def de(request):
    Product_rent.objects.filter(productname='Himalaya').delete()
    return HttpResponse('succeed')

def deleterent(request):
    id=request.GET.get("id")
    rnt=Product_rent.objects.filter(id=id).delete()
    messages.info(request,"deleted successfully")
    return HttpResponseRedirect('/viewrentpdt')

def viewsalepdt(request):
    uid=request.session['uid']
    user=Register_shop.objects.get(user_login=uid)
    # id=request.GET.get("id")
    if request.POST:
        id = request.POST['ID']
        print(id)
        # prdt=request.POST.get("chai")
        # print(prdt)
        price=request.POST.get("price")
        saleitem=Product_sell.objects.get(id=id)

        print(price)
        if 'image' in request.FILES:
            image=request.FILES["image"]
        else:
            image=saleitem.images
        stock=request.POST.get("stock")

        # saleitem.productname="chain"
        saleitem.price=price
        saleitem.images=image
        saleitem.stock=stock
        saleitem.save()
        # item.save()  
        messages.info(request,"updated successfully")
        # return HttpResponseRedirect('/viewsalepdt')
    sale=Product_sell.objects.filter(shop_name_id=user)
    return render(request,"shop/viewsalepdt.html",{"sale":sale})

def deletesale(request):
    id=request.GET.get("id")
    rnt=Product_sell.objects.filter(id=id).delete()
    messages.info(request,"deleted successfully")
    return HttpResponseRedirect('/viewsalepdt')

def ordershop(request):
    uid=request.session["uid"]
    shop=Register_shop.objects.get(user_login=uid)
    item=Shopcart.objects.filter(status="paid",product__shop_name_id=shop.id)
    return render(request,"shop/ordershop.html",{"item":item})

def deliveryshop(request):
    id=request.GET.get("id")
    item=Shopcart.objects.filter(id=id).update(status="delivered")
    messages.info(request,"Item delivered successfully")
    return redirect("/ordershop")

def ordershophistory(request):
    uid=request.session["uid"]
    shop=Register_shop.objects.get(user_login=uid)
    item=Shopcart.objects.filter(status="delivered",product__shop_name_id=shop.id)
    return render(request,"shop/ordershophistory.html",{"item":item})

def orderclub(request):
    uid = request.session["uid"]
    club = Register_club.objects.get(user_login=uid)
    today = d.today().strftime('%Y-%m-%d')
    item = Rentcart.objects.filter(
        Q(status="paid") | Q(status="approved"), 
        product__club_name_id=club.id,
        return_date__gte=today
    )
    return render(request, "club/orderclub.html", {"item": item, "today": today})

def deliveryclub(request):
    id=request.GET.get("id")
    item=Rentcart.objects.filter(id=id).update(status="delivered")
    messages.info(request,"Item delivered successfully")
    return redirect("/orderclub")

def orderclubhistory(request):
    uid = request.session["uid"]
    club = Register_club.objects.get(user_login=uid)
    today = d.today().strftime('%Y-%m-%d')
    item = Rentcart.objects.filter(
        Q(status="delivered") | Q(status="rejected") | Q(return_date__lt=today),
        product__club_name_id=club.id
    ).exclude(status="requested")
    return render(request, "club/orderclubhistory.html", {"item": item})

def viewparticipant(request):
    uid=request.session["uid"]
    club=Register_club.objects.get(user_login=uid)
    Participant=Events.objects.filter(club_id=club) 
    return render(request,"club/viewparticipants.html",{"participant":Participant})

def viewparticipants2(request):
    id=request.GET.get("id")
    evnt=Events.objects.get(id=id)
    Participant=Participate.objects.filter(event_id=evnt) 
    return render(request,"club/viewparticipants2.html",{"participant":Participant})

def addfeedback(request):
    uid = request.session["uid"]
    user = Register_user.objects.get(user_login=uid)
    rent_cart_id = request.GET.get("rent_cart_id")
    shop_cart_id = request.GET.get("shop_cart_id")

    # Validate order belongs to user and is completed
    rent_cart_item = None
    shop_cart_item = None
    existing_feedback = None

    if rent_cart_id:
        try:
            rent_cart_item = Rentcart.objects.get(id=rent_cart_id, order__user_login=user, status__in=["paid","delivered"])
            # Rental feedback only allowed AFTER return_date has passed
            today_str = d.today().strftime('%Y-%m-%d')
            if rent_cart_item.return_date and rent_cart_item.return_date >= today_str:
                messages.error(request, "You can only leave feedback after your rental period has ended.")
                return redirect("/renthistory")
            existing_feedback = Feedback.objects.filter(rent_cart=rent_cart_item).first()
        except Rentcart.DoesNotExist:
            messages.error(request, "Invalid or incomplete rental order.")
            return redirect("/renthistory")

    elif shop_cart_id:
        try:
            # Shop feedback only allowed AFTER the shop marks the item as delivered
            shop_cart_item = Shopcart.objects.get(id=shop_cart_id, order__user_login=user, status="delivered")
            existing_feedback = Feedback.objects.filter(shop_cart=shop_cart_item).first()
        except Shopcart.DoesNotExist:
            messages.error(request, "Feedback can only be submitted after the product has been delivered.")
            return redirect("/purchasehistory")
    else:
        messages.error(request, "No order specified.")
        return redirect("/renthistory")

    if existing_feedback:
        messages.info(request, "You have already left feedback for this order. You can edit it below.")
        return redirect(f"/editfeedback?id={existing_feedback.id}")

    if request.POST:
        fb_text = request.POST.get("feedback", "").strip()
        if fb_text:
            Feedback.objects.create(
                user=user,
                feedback=fb_text,
                rent_cart=rent_cart_item,
                shop_cart=shop_cart_item,
            )
            messages.success(request, "Feedback posted successfully!")
            return redirect("/renthistory" if rent_cart_item else "/purchasehistory")
        else:
            messages.error(request, "Feedback cannot be empty.")

    context = {
        "rent_cart_item": rent_cart_item,
        "shop_cart_item": shop_cart_item,
        "rent_cart_id": rent_cart_id,
        "shop_cart_id": shop_cart_id,
    }
    return render(request, "user/addfeedback.html", context)


def editfeedback(request):
    uid = request.session["uid"]
    user = Register_user.objects.get(user_login=uid)
    id = request.GET.get("id")
    try:
        fb = Feedback.objects.get(id=id, user=user)
    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
        return redirect("/renthistory")

    if request.POST:
        fb_text = request.POST.get("feedback", "").strip()
        if fb_text:
            fb.feedback = fb_text
            fb.save()
            messages.success(request, "Feedback updated successfully!")
            return redirect("/renthistory" if fb.rent_cart else "/purchasehistory")
        else:
            messages.error(request, "Feedback cannot be empty.")

    return render(request, "user/editfeedback.html", {"fb": fb})


def deletefeedback(request):
    uid = request.session["uid"]
    user = Register_user.objects.get(user_login=uid)
    id = request.GET.get("id")
    try:
        fb = Feedback.objects.get(id=id, user=user)
        was_rent = fb.rent_cart is not None
        fb.delete()
        messages.success(request, "Feedback deleted.")
        return redirect("/renthistory" if was_rent else "/purchasehistory")
    except Feedback.DoesNotExist:
        messages.error(request, "Feedback not found.")
        return redirect("/renthistory")


def viewfeedback(request):
    fb = Feedback.objects.all().order_by('-id')
    return render(request, "admin/viewfeedback.html", {"fb": fb})


def userfeedback(request):
    uid = request.session['uid']
    user = Register_user.objects.get(user_login=uid)
    feedbacks = Feedback.objects.filter(user=user).order_by('-id')
    return render(request, "user/userfeedback.html", {"feedbacks": feedbacks})


def viewriders(request):
    user=Register_user.objects.all()
    return render(request,"admin/viewriders.html",{"user":user})

def udp(request):
    Login.objects.filter(id='44').delete()    
    return HttpResponse('zfdsfsdfsd')

def shopprofile(request):
    uid = request.session['uid']
    shop = Register_shop.objects.filter(user_login=uid)
    return render(request, "shop/shopprofile.html", {"shop": shop})

def editshop(request):
    uid = request.session['uid']
    shop = Register_shop.objects.get(user_login=uid)
    if request.POST:
        username = request.POST["username"]
        shopname = request.POST["shopname"]
        phonenumber = request.POST["phonenumber"]
        location = request.POST["location"]
        
        Register_shop.objects.filter(id=shop.id).update(
            username=username,
            shopname=shopname,
            phonenumber=phonenumber,
            location=location
        )
        messages.info(request, "Profile updated successfully")
        return redirect('/shopprofile')
    return render(request, "shop/editshop.html", {"shop": shop})

def accepteventparticipant(request):
    id=request.GET.get("id")
    Participate.objects.filter(id=id).update(status="Approved")
    messages.info(request,"Participant approved")
    # Redirect back to the event's participant list
    participation = Participate.objects.get(id=id)
    return redirect(f"/viewparticipants2?id={participation.event_id}")

def rejecteventparticipant(request):
    id=request.GET.get("id")
    Participate.objects.filter(id=id).update(status="Rejected")
    messages.info(request,"Participant rejected")
    participation = Participate.objects.get(id=id)
    return redirect(f"/viewparticipants2?id={participation.event_id}")
