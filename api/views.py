from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import books,Carts
from api.serializers import bookSerializer,bookModelSerializer,UserSerializer,CartSerializer,ReviewSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action




class bookView(APIView):
    def get(self,request,*args,**kw):

        qs=books.objects.all()
        serializer=bookSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def post(self,request,*args,**kw):

        serializer=bookSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            books.objects.create(**serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class bookDetailView(APIView):


    def get(self,request,*args,**kw):
       print(kw)
       id=kw.get('id')
       qs=books.objects.get(id=id)
       serializer=bookSerializer(qs)
       return Response(data=serializer.data)
    
    def put(self,request,*args,**kw):
        serializer=bookSerializer(data=request.data)
        if serializer.is_valid():
            id=kw.get('id')
            books.objects.filter(id=id).update(**request.data)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        return Response(data='item successfully updated')
         
    
    
    def delete(self,request,*args,**kw):
        id=kw.get('id')
        books.objects.filter(id=id).delete()
        return Response(data='item deleted')

class bookViewsetView(ModelViewSet): 
    serializer_class=bookModelSerializer
    queryset=books.objects.all()  
                                    
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]
    
    @action(methods=["GET"],detail=False)
    def categories(self,request,*args,**kw):
        qs=books.objects.values_list('category',flat=True).distinct()
        return Response(data=qs)
    
    @action(methods=["POST"],detail=True)
    def add_cart(self,request,*args,**kw):
        user=request.user
        id=kw.get('pk')
        item=books.objects.get(id=id)
        user.carts_set.create(books=item)
        return Response(data="item successfully added to cart")

    @action(methods=["POST"],detail=True)
    def add_review(self,request,*args,**kw):
        user=request.user
        bid=kw.get('pk')
        books=self.queryset.get(id=bid)
        ser=ReviewSerializer(data=request.data)
        if ser.is_valid():
            ser.save(books=books,user=user)
            return Response(data=ser.data,status=status.HTTP_201_CREATED)
        return Response(data=ser.errors,status=status.HTTP_400_BAD_REQUEST)


class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()



