from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .models import *
from django.contrib.auth  import logout

measure=[('Dona','Dona'),
         ('Kg','Kg'),
         ('Tonna','Tonna'),
         ('Metr','Metr'),
         ('Cm','Cm'),
         ]

class BranchView(View):
    def get(self,request):
        branches=Branch.objects.all()
        context={
            'branches':branches
        }
        return render(request,'bolimlar.html',context)

class ProductView(View):
    def get(self,request):
        products=Product.objects.all()
        branches=Branch.objects.all()
        context={
            'products':products,
            'measure':measure,
            'branches':branches
        }
        return render(request,'mahsulotlar.html',context)
    def post(self,request):
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


class ClientView(View):
    def get(self,request):
        clients=Client.objects.all()
        branches=Branch.objects.all()
        context={
            'clients':clients,
            'branches':branches
        }
        return render(request,'mijozlar.html',context)
    def post(self,request):
        Client.objects.create(
            name=request.POST.get('client_name'),
            phone=request.POST.get('client_phone'),
            address=request.POST.get('client_address'),
            store_name=request.POST.get('store_name'),
            branch=Branch.objects.get(id=request.POST.get('branch'))
        )
        return redirect('mijozlar')

class RecordView(View):
    def get(self,request):
        records=Record.objects.all()
        products=Product.objects.all()
        clients=Client.objects.all()
        context={
            'records':records,
            'products':products,
            'clients':clients
        }
        return render(request,'statistikalar.html',context)

    def post(self, request):
        total_price = float(request.POST.get('total_price'))
        payed = float(request.POST.get('payed'))

        Record.objects.create(
            product=get_object_or_404(Product,id=request.POST.get('product')),
            client=get_object_or_404(Client,id=request.POST.get('client')),
            date=request.POST.get('sana'),
            quantity=int(request.POST.get('quantity')),
            total_price=total_price,
            payed=payed,
            loan=total_price - payed
        )
        return redirect('stats')


def LogoutView(request):
    logout(request)
    return redirect('/')
