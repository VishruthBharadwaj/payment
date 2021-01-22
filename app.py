import razorpay
import json

from flask import Flask, render_template, request

from flask import Flask, render_template, jsonify, request
import paypalrestsdk


app = Flask(__name__,static_folder = "static", static_url_path='')
razorpay_client = razorpay.Client(auth=("rzp_test_LXZbf5QmXLLIq2", "CXeN9K371rB14bQeEvy4OxES"))


@app.route('/')
def app_create():
    return render_template('my_index.html')
@app.route('/form')
def front_page():
    return render_template('form.html')

@app.route('/charge', methods=['POST'])
def app_charge():
    amount = 100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))






paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AVxod3JVIhmEeQORX3sxKAhYwymRvPdAPmrI5jsb9NB_OvGx2M1adSyNJS5hVJAPC-hcuPlli-7Dc3ko",
  "client_secret": "EFHjxLZro0RQtPgGwEBZmLD0HfMyRDkScZszQvlDz8hxHRTGTHwxp5af_iDO2Qm_ZMaYZpIL2oWaTeot" })


@app.route('/payment', methods=['POST'])
def payment():

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": "1000.00",
                    "currency": "INR",
                    "quantity": 1}]},
            "amount": {
                "total": "1000.00",
                "currency": "INR"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})


if __name__ == '__main__':
    app.run()
