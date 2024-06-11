from rest_framework import mixins, status

from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Customer, Account, Action, Transaktion, Transfer
from .serializers import CustomerSerializer, AccountSerializer, ActionSerializer, TransferSerializer
from .service import make_transfer


class CustomerList(generics.ListCreateAPIView):
    """
    Get a list, put and patch methods are not allowed.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        """
        Return object for current authenticated user only
        """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """

        """
        return self.queryset.filter(user=self.request.user)


class CustomerViewSet(viewsets.ModelViewSet):
    """

    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AccountViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()



    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ActionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Action.objects.all()


    def get_queryset(self):
        """
        Return objects for current authenticated user only
        """
        accounts = Account.objects.filter(user=self.request.user)

        return self.queryset.filter(account__in=accounts)

    def perform_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            account = Account.objects.filter(user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            print(e)

            content = {'Error': 'No such account'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(account=account)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





class TransaktionViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = ActionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Action.objects.all()


    def get_queryset(self):
        """
        Return objects for current authenticated user only
        """
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(account__in=accounts)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)

        try:
            account = Account.objects.filter(user=self.request.user).get(pk=self.request.data['account'])
        except Exception as e:
            content = {'Error': 'Not such account'}
            return Response(content, status.HTTP_400_BAD_REQUEST)

        try:
            Transaktion.make_transaction(**serializer.valited_data)
        except ValueError:
            content = {'Error': 'Not enough money'}
            return Response(content, status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED, headers=headers)



class TransferViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):
    serializer_class = TransferSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Transfer.objects.all()

    def get_queryset(self):
        """
        Return objects for current authenticated user only
        """
        accounts = Account.objects.filter(user=self.request.user)
        return self.queryset.filter(from_account__in=accounts)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            make_transfer(**serializer.validated_data)
        except ValueError:
            content = {'Error': 'Not enough money'}
            return Response(content, status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED, headers=headers)





