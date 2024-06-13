from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, GroupSerializer, CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_user_to_group(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    group_name = request.data.get('group')
    if not group_name:
        return Response({'error': 'Group name is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    user.groups.add(group)
    user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({"error": "Only admin can add categories."}, status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def menuitem_list(request):
    if request.method == 'GET':
        menuitems = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuitems, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response({"error": "Only admin can add menu items."}, status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def menuitem_detail(request, pk):
    try:
        menuitem = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MenuItemSerializer(menuitem)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not request.user.groups.filter(name='Managers').exists():
            return Response({"error": "Only managers can edit menu items."}, status=status.HTTP_403_FORBIDDEN)
        serializer = MenuItemSerializer(menuitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not request.user.groups.filter(name='Managers').exists():
            return Response({"error": "Only managers can delete menu items."}, status=status.HTTP_403_FORBIDDEN)
        menuitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def cart_list(request):
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def delivery_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, delivery_crew=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found or not assigned to this delivery crew'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_crew_orders(request):
    orders = Order.objects.filter(delivery_crew=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_menuitems(request, category_id):
    menuitems = MenuItem.objects.filter(category_id=category_id)
    serializer = MenuItemSerializer(menuitems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def paginate_menuitems(request):
    page_size = int(request.query_params.get('page_size', 10))
    page_number = int(request.query_params.get('page_number', 1))
    menuitems = MenuItem.objects.all()[(page_number-1)*page_size:page_number*page_size]
    serializer = MenuItemSerializer(menuitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def sort_menuitems_by_price(request):
    menuitems = MenuItem.objects.order_by('price')
    serializer = MenuItemSerializer(menuitems, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_order_to_delivery_crew(request, order_id):
    if not request.user.groups.filter(name='Managers').exists():
        return Response({"error": "Only managers can assign orders to the delivery crew."}, status=status.HTTP_403_FORBIDDEN)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    delivery_crew_id = request.data.get('delivery_crew_id')
    if not delivery_crew_id:
        return Response({'error': 'Delivery crew ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        delivery_crew = User.objects.get(pk=delivery_crew_id)
    except User.DoesNotExist:
        return Response({'error': 'Delivery crew not found'}, status=status.HTTP_404_NOT_FOUND)

    if not delivery_crew.groups.filter(name='Delivery Crew').exists():
        return Response({'error': 'User is not part of the delivery crew'}, status=status.HTTP_400_BAD_REQUEST)

    order.delivery_crew = delivery_crew
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_item_of_the_day(request, menuitem_id):
    if not request.user.groups.filter(name='Managers').exists():
        return Response({"error": "Only managers can update the item of the day."}, status=status.HTTP_403_FORBIDDEN)

    try:
        menuitem = MenuItem.objects.get(pk=menuitem_id)
    except MenuItem.DoesNotExist:
        return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

    # Assuming we have a field `is_item_of_the_day` in MenuItem model
    MenuItem.objects.all().update(featured=False)
    menuitem.featured = True
    menuitem.save()

    serializer = MenuItemSerializer(menuitem)
    return Response(serializer.data, status=status.HTTP_200_OK)

