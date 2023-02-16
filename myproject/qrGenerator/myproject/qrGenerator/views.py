from web3 import Web3 as Web31
from django.shortcuts import render
from django.http import JsonResponse

from qrGenerator.models import User,Item
from qrGenerator.serializers import UserSerializer,ItemSerializer,AddLostItemSerializer,PhoneSerializer


from rest_framework.response import Response

# Create your views here.
from rest_framework import generics


from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# class UserDetail(generics.CreateAPIView):
#     http_method_names = ['get', 'put', 'delete','post']
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class UserDetail(generics.RetrieveAPIView):
    #http_method_names = ['get', 'put', 'delete','post']
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
class AddLostItemView(generics.CreateAPIView):
    serializer_class = AddLostItemSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_id = serializer.validated_data.get('item_id')
        item_name = serializer.validated_data.get('item_name')
        item_description = serializer.validated_data.get('item_description')
        item_location = serializer.validated_data.get('item_location')

        w3=Web31(Web31.HTTPProvider("http://localhost:7545"))

        if w3.isConnected():
            print("Connected to Ganache")
        else:
            print("Failed to connect to Ganache")
        block_number = w3.eth.blockNumber
        print(f"Connected to Ganache. Current block number is: {block_number}")

        with open("qrGenerator/abi.json", 'r') as abi_file:
            abi = abi_file.read()
        contract_address = "0xD176F95A9ACD625a6f21699898Cd4cAe28144544"
        if not w3.isChecksumAddress(contract_address):
            raise ValueError("Invalid contact address: {}".format(contract_address))
        contract_address = Web31.toChecksumAddress(contract_address)
        print(f"contract_address is: {contract_address}")
        print(type(contract_address))
        contract = w3.eth.contract(address=contract_address, abi=abi)
        print(contract)
        nonce = w3.eth.getTransactionCount('0xD176F95A9ACD625a6f21699898Cd4cAe28144544')
        print(nonce)

        # Build the transaction
        txn = contract.functions.addLostItem(item_id, item_name, item_description, item_location).buildTransaction({
            'gas': 1000000,
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': nonce,
        })

        # Sign the transaction
        signed_txn = w3.eth.account.signTransaction(txn, private_key='d03567b5c47c0626299402270c4c94d662fdf4c06eb960ad9d3376a68618a566')

        # Send the transaction
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        return Response({'message': 'Lost item added successfully', 'transaction_hash': txn_hash.hex()})

class GetLostItemView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        item_id = kwargs['item_id']

        # Connect to the Ethereum network using web3.py
        w3 = Web31(Web31.HTTPProvider('http://localhost:7545'))

        # Load the contract ABI
        with open("qrGenerator/abi.json", 'r') as abi_file:
            abi = abi_file.read()

        # Load the contract address
        contract_address = '0xD176F95A9ACD625a6f21699898Cd4cAe28144544'
        if not w3.Web31.isAddress(contract_address):
            raise ValueError("Invalid contact address: {}".format(contract_address))
        contract_address = w3.toChecksumAddress(contract_address)

        # Instantiate the contract
        contract = w3.eth.contract(address=contract_address, abi=abi)

        # Call the getLostItem function
        item_name, item_description, item_location=contract.functions.getLostItem(item_id).call()

        # Return the result as a JSON response
        return JsonResponse({
            'item_name': item_name,
            'item_description': item_description,
            'item_location': item_location,
            'owner': owner
        })
class SendEmailView(generics.CreateAPIView):
    #example request
    # {
    # "to_email": "recipient@example.com",
    # "subject": "Example subject",
    # "body": "Example message body"
    # }

    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        # Set the email parameters
        from_no = +18312154605
        to_no = request.data.get('to_no')
        body = request.data.get('body')
        
        # Send the email using Twilio
        account_sid = 'AC7ed87c58e198d3417b339d31cafbac19'
        auth_token = '535baf81fd6ec7e05f959702bce6b6e8'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=to_no,
            from_=from_no,
            body=body
        )
        
        # Return a response
        response = MessagingResponse()
        response.message('SMS sent successfully!')
        return Response(str(response))