from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
# Create your models here.
class Login(AbstractUser):
    usertype=models.CharField(max_length=100,null=True)
    viewpassword=models.CharField(max_length=100,null=True)

class Register_user(models.Model):
    username=models.CharField(max_length=100,null=True)
    ridername=models.CharField(max_length=100,null=True)
    gender=models.CharField(max_length=100,null=True)
    DOB=models.DateField(auto_now_add=True,null=True)
    user_login=models.ForeignKey(Login,on_delete=models.CASCADE,max_length=100,null=True)
    email=models.EmailField(null=True)
    phonenumber=models.CharField(max_length=15,null=True)
    address=models.CharField(max_length=15,null=True)
    images=models.ImageField(null=True)
    bio=models.CharField(max_length=1000,null=True)

class Register_club(models.Model):
    username=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    clubname=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    user_login=models.ForeignKey(Login,on_delete=models.CASCADE,max_length=100,null=True)
    about=models.CharField(null=True,max_length=100)
    
    image = models.FileField(upload_to="file/", null= True)
    
    phonenumber=models.CharField(max_length=15,null=True)

class Register_shop(models.Model):
    username=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    phonenumber=models.CharField(max_length=15,null=True)
    shopname=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    user_login=models.ForeignKey(Login,on_delete=models.CASCADE,max_length=100,null=True)

class Product_sell(models.Model):
    shop_name=models.ForeignKey(Register_shop,on_delete=models.CASCADE,max_length=100,null=True)
    productname=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True)
    images=models.ImageField(null=True)
    stock=models.IntegerField(null=True)

class Product_rent(models.Model):
    club_name=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)
    productname=models.CharField(max_length=100,null=True)
    rent=models.IntegerField(null=True)
    images=models.ImageField(null=True)
    
class Shoporder(models.Model):
    user_login=models.ForeignKey(Register_user,on_delete=models.CASCADE,max_length=100,null=True)
    club_login=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)
    total=models.IntegerField(null=True)
    date=models.DateField(auto_now=True,null=True)
    status=models.CharField(max_length=100,null=True,default="pending")
    
class Shopcart(models.Model):
    product=models.ForeignKey(Product_sell,on_delete=models.CASCADE,max_length=100,null=True)
    quantity=models.IntegerField(null=True)
    total=models.IntegerField(null=True)
    order=models.ForeignKey(Shoporder,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,null=True,default="pending")

class Rentorder(models.Model):
    user_login=models.ForeignKey(Register_user,on_delete=models.CASCADE,max_length=100,null=True)
    club_login=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)
    total=models.IntegerField(null=True)
    file=models.FileField(null=True)
    orderdate=models.DateField(auto_now=True,null=True)
    status=models.CharField(max_length=100,null=True,default="pending")
    
class Rentcart(models.Model):
    product=models.ForeignKey(Product_rent,on_delete=models.CASCADE,max_length=100,null=True)
    rented_date=models.CharField(null=True,max_length=100)
    return_date=models.CharField(max_length=100,null=True)
    days=models.CharField(max_length=100,null=True,default="1")
    total=models.IntegerField(null=True)
    order=models.ForeignKey(Rentorder,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,null=True,default="pending")

class Events(models.Model):
    name=models.CharField(max_length=100,null=True)
    club_id=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)
    date=models.DateField(null=True)
    starting_location=models.CharField(max_length=100,null=True)
    destination=models.CharField(max_length=100,null=True)
    estimated_cost=models.CharField(max_length=100,null=True)
    route=models.CharField(max_length=1000,null=True)

class Article(models.Model):
    articlename=models.CharField(max_length=100,null=True)
    articles=models.CharField(max_length=100000,null=True)
    club_login=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)

class Posts(models.Model):
    club_login=models.ForeignKey(Register_club,on_delete=models.CASCADE,max_length=100,null=True)
    images=models.ImageField(null=True)
    date=models.DateField(auto_now=True,null=True)

class Requests(models.Model):
    user_login=models.ForeignKey(Register_user,on_delete=models.CASCADE,null=True)
    club_name=models.ForeignKey(Register_club,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,null=True)

class Participate(models.Model):
    user=models.ForeignKey(Register_user,on_delete=models.CASCADE,null=True)
    event=models.ForeignKey(Events,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,null=True)

class Feedback(models.Model):
    user=models.ForeignKey(Register_user,on_delete=models.CASCADE,null=True)
    feedback=models.CharField(max_length=10000,null=True)
   



    
    



    


