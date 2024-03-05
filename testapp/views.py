# import all necessary modules
import razorpay
from .models import Payment
from app.models import Customer,Cart
from django.shortcuts import render

#######################################################################################################################################

# razorpay key details
RAZOR_KEY_ID='rzp_test_tjijojzPmDq26B'
RAZOR_KEY_SECRET='Tk5hOfoAFTjRdHKMdMNDY3eJ'


# method to create an order id
def payment(request):
    client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount+shipping_amount

    order = client.order.create({'amount': totalamount * 100, 'currency': 'INR', 'payment_capture': '1'})
    p=Payment(name=request.user,amount=totalamount,order_id=order['id'])
    p.save()
    return render(request, 'testapp/payment_form.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount,'payment':order})

####################################################################################################################################################

# method for verifying a signature
def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        Payment =Payment.objects.get(order_id=response['razorpay_order_id'])
        Payment.razorpay_payment_id = response['razorpay_payment_id']
        Payment.paid = True
        Payment.save()
        return render(request, 'testapp/payment_status.html', {'status': True})
    except:
        return render(request, 'testapp/payment_status.html', {'status': False})
    
#############################################################################################################################################