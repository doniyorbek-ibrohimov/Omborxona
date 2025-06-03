from pkgutil import read_code

from django.core.files.uploadhandler import load_handler
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import *
from django.contrib.auth  import logout,login,authenticate

measure=[('Dona','Dona'),
         ('Kg','Kg'),
         ('Tonna','Tonna'),
         ('Metr','Metr'),
         ('Cm','Cm'),
         ]

class IndexView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'bolimlar.html',)
        return redirect('login')

class ProductView(View):
    def get(self,request):
        if request.user.is_authenticated:
            products=Product.objects.all().filter(branch=request.user.branch)
            branches=Branch.objects.all()
            context={
                'products':products,
                'measure':measure,
                'branches':branches
            }
            return render(request,'mahsulotlar.html',context)
        return redirect('login')
    def post(self,request):
        if request.user.is_authenticated:
            Product.objects.create(
                name=request.POST.get('pr_name'),
                brand=request.POST.get('pr_brand'),
                branch=get_object_or_404(Branch,id=request.POST.get('pr_branch')),
                measure=request.POST.get('measure'),
                in_price=request.POST.get('pr_price_in'),
                out_price=request.POST.get('pr_price_out'),
                amount=request.POST.get('pr_amount')
            )
            return redirect('mahsulotlar')
        return redirect('login')


class ClientView(View):
    def get(self,request):
        if request.user.is_authenticated:
            clients=Client.objects.all()
            branches=Branch.objects.all()
            context={
                'clients':clients,
                'branches':branches
            }
            return render(request,'mijozlar.html',context)
        return redirect('login')
    def post(self,request):
        if request.user.is_authenticated:
            Client.objects.create(
                name=request.POST.get('client_name'),
                phone=request.POST.get('client_phone'),
                address=request.POST.get('client_address'),
                store_name=request.POST.get('store_name'),
                branch=Branch.objects.get(id=request.POST.get('branch')),
                debt=request.POST.get('c_debt')
            )
            return redirect('mijozlar')
        return redirect('login')

class ClientUpdateView(View):
    def get(self,request,pk):
        client=get_object_or_404(Client,pk=pk)
        context={
            'client':client
        }
        return render(request,'mijoz-tahrirlash.html',context)
    def post(self,request,pk):
        Client.objects.filter(pk=pk).update(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            store_name=request.POST.get('store_name'),
            debt=request.POST.get('debt'),
        )
        return redirect('mijozlar')


class RecordView(View):
    def get(self,request):
        if request.user.is_authenticated:
            records=Record.objects.all()
            products=Product.objects.all()
            clients=Client.objects.all()
            context={
                'records':records,
                'products':products,
                'clients':clients
            }
            return render(request,'statistikalar.html',context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            total_price = float(request.POST.get('total_price'))
            payed = float(request.POST.get('payed'))
            product = get_object_or_404(Product, id=request.POST.get('product'))
            client = get_object_or_404(Client, id=request.POST.get('client'))

            Record.objects.create(
                product=product,
                client=client,
                date=request.POST.get('sana'),
                quantity=int(request.POST.get('amount')),
                total_price=total_price,
                payed=payed,
                loan=total_price - payed
            )
            loan=total_price - payed
            if product.amount >int(request.POST.get('amount')):
                product.amount -=int(request.POST.get('amount'))
            client.debt+=loan
            client.save()
            return redirect('stats')
        return redirect('login')

class RecordUpdate(View):
    def get(self,request,pk):
        record=Record.objects.get(id=pk)
        products = Product.objects.all()
        clients = Client.objects.all()
        context = {
            'products': products,
            'clients': clients,
            'record':record
        }
        return render(request, 'stat-tahrirlash.html', context)
    def post(self,request,pk):
        record=Record.objects.get(id=pk)
        product=Product.objects.get(id=request.POST.get('product'))
        print("id", request.POST.get('client'))
        client=Client.objects.get(id=request.POST.get('client'))

        client = get_object_or_404(Client, id=request.POST.get('client'))
        print("client:",client)
        client.debt-=record.loan
        client.save()
        # Record.objects.filter(id=pk).update(
        #     product=product,
        #     client=client,
        #     quantity=request.POST.get('amount'),
        #     total_price=request.POST.get('total_price'),
        #     payed=request.POST.get('payed'),
        # )
        record.product.amount+=record.amount
        record.product.amount.save()



        record.product=product
        record.client=client
        record.amount=int(request.POST.get('amount'))
        record.total_price=float(request.POST.get('total_price'))
        record.payed=float(request.POST.get('payed'))
        record.loan=float(request.POST.get('total_price'))-float(request.POST.get('payed'))

        record.save()

        product.amount -=record.amount
        product.save()
        client.debt+=record.loan
        client.save()

        return redirect('/stats/')



class ProductUpdateView(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            product=get_object_or_404(Product,pk=pk,branch=request.user.branch)
            context={
                'product':product
            }
            return render(request,'mahsulot-tahrirlash.html',context)
        return redirect('login')
    def post(self,request,pk):
        if request.user.is_authenticated:
            product=get_object_or_404(Product,pk=pk)
            product.name=request.POST.get('name')
            product.brand=request.POST.get('brand')
            product.in_price=request.POST.get('in_price')
            product.out_price=request.POST.get('out_price')
            product.amount=request.POST.get('amount')
            product.save()
            return redirect('mahsulotlar')
        return redirect('login')
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('index')
        return redirect('login')


def LogoutView(request):
    logout(request)
    return redirect('login')
