
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RecordSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(branch=self.request.user.branch)

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        client = serializer.validated_data['client']
        amount = serializer.validated_data['quantity']
        total_price = serializer.validated_data['total_price']
        payed = serializer.validated_data['payed']
        loan = total_price - payed

        if product.amount >= amount:
            product.amount -= amount
            product.save()
            client.debt += loan
            client.save()
            serializer.save(loan=loan)
