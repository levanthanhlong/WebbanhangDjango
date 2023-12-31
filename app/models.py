from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.
#models.Model là một lớp cơ sở trong Django, 
#được sử dụng để định nghĩa các lớp mô hình (model) trong kiến trúc MVC của Django

#change usercreationform django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True, blank=False)
#     #Nếu null = True, Django sẽ lưu trữ các giá trị trống dưới dạng NULL trong cột cơ sở dữ liệu. 
#     #Nếu blank = False, trường đó sẽ bắt buộc phải nhập giá trị.
#     name = models.CharField(max_length=200,null=True)
#     email = models.CharField(max_length=200,null=True)

#     def __str__(self):
#         return self.name

#Category

class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_categories',null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True,blank=False)
    image = models.ImageField(null=True, blank=True)
    detail = models.CharField(max_length= 3000, null=True, blank=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
# Đơn hàng gồm nhiều orderitem
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)#luu thong tin giao dich

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
# -> một Order có thể liên kết với nhiều OrderItem -> mối quan hệ một nhiều     
# từng mục sản phẩm trong đơn hàng, cung cấp số lượng của 1 sản phảm được mua
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

 # Thông tin ship hàng  
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    addreess = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=12, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.addreess
    