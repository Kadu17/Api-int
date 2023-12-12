
import decimal
from random import randint
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Card, Address, Contacts, Account, Loan, Transaction, BankStatement, LoanPayment, Deposit
from .serializers import CardSerializer, AddressSerializer, ContactsSerializer, AccountSerializer, LoanPaySerializer, LoanSerializer, TransactionSerializer, BankStateSerializer, DepositSerializer
from users import models
from rest_framework.response import Response

class Card(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def retrieve(self, request, pk=None):
        print("hhh")
        return Response({"message": "created"},
                            status=status.HTTP_201_CREATED)

class Address(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class Contacts(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class Loan(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class LoanPayment(viewsets.ModelViewSet):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaySerializer

class Accounts(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class Transaction(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        recipient = Account.objects.get(pk=self.request.data['recipient'])
        sender = Account.objects.get(pk=self.request.data['sender'])
        transfer_amount = decimal.Decimal(self.request.data['value'])

        # Check if sender has sufficient balance
        if sender.balance < transfer_amount:
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # Update balances
        recipient.balance += transfer_amount
        sender.balance -= transfer_amount

        update_recipient = {'balance': recipient.balance, 'number': recipient.number, 'agency': recipient.agency,
                            'client': recipient.client.pk}
        update_sender = {'balance': sender.balance, 'number': sender.number, 'agency': sender.agency,
                         'client': sender.client.pk}

        serializer_sender = AccountSerializer(sender, data=update_sender)
        serializer_recipient = AccountSerializer(recipient, data=update_recipient)

        if serializer_sender.is_valid() and serializer_recipient.is_valid():
            serializer_sender.save()
            serializer_recipient.save()
            return super().create(request, *args, **kwargs)
        else:
            print(serializer_sender.errors)
            print(sender.client)
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

class Deposit(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

    def create(self, request, *args, **kwargs):
        acc = Account.objects.get(pk = self.request.data['account'])

        acc.balance += decimal.Decimal(self.request.data['value'])

        updateAccount = {'balance':acc.balance, 'number':acc.number,'agency':acc.agency,'client': acc.client.pk}

        serializerAcc = AccountSerializer(acc, data = updateAccount)

        if serializerAcc.is_valid():
            serializerAcc.save()
            return super().create(request, *args, **kwargs)
        else:
            print(serializerAcc.errors)
            print(acc.client)
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

class BankStatement(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all()
    serializer_class = BankStateSerializer