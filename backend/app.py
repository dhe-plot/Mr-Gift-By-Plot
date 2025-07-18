from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_mail import Mail, Message
import os
import stripe
import jwt
import requests
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Flask
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Clerk configuration
CLERK_SECRET_KEY = os.environ.get('CLERK_SECRET_KEY')
CLERK_PUBLISHABLE_KEY = os.environ.get('CLERK_PUBLISHABLE_KEY')

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401

        token = auth_header.split(' ')[1]
        try:
            # Verify the JWT token with Clerk
            # In production, you should verify the token signature with Clerk's public key
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            g.user_id = decoded_token.get('sub')
            g.user_email = decoded_token.get('email')
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated_function

# In-memory mock seller data (for demo purposes)
mock_sellers = [
    {
        "name": "Sarah Seller",
        "email": "sarah@example.com",
        "business": "Sarah's Gifts",
        "products": [
            {"id": 1, "name": "Luxury Spa Set", "desc": "Indulge in relaxation with our spa set", "img": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80"},
            {"id": 2, "name": "Gourmet Chocolate Box", "desc": "A sweet treat for any occasion", "img": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80"},
            {"id": 3, "name": "Personalized Jewelry", "desc": "Custom-made jewelry for a personal touch", "img": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80"}
        ]
    },
    # Add more mock sellers as needed
]

def find_seller(email):
    return next((s for s in mock_sellers if s["email"] == email), None)

@app.route('/api/sellers', methods=['POST'])
def register_seller():
    name = request.form.get('name')
    email = request.form.get('email')
    business = request.form.get('business')
    # You can handle CSV and product image here if needed

    # Send confirmation email
    try:
        if not email:
            return jsonify({'message': 'Email is required.'}), 400
        confirm_link = f'http://localhost:5173/seller-profile?email={email}'  # Updated to profile link
        msg = Message(
            subject='Confirm your Seller Registration - Mr. Gift',
            recipients=[email],
            body=f"""
Hi {name},

Thank you for registering as a seller on Mr. Gift!

Click the link below to access your seller profile:
{confirm_link}

On your profile, you can access your products, get market fit suggestions, and use the search optimization icon to pay for a top search spot!

Best regards,
Mr. Gift Team
            """
        )
        mail.send(msg)
        return jsonify({'message': 'Registration successful! Confirmation email sent.'}), 200
    except Exception as e:
        print('Email send error:', e)
        return jsonify({'message': 'Registration successful, but failed to send confirmation email.'}), 500

@app.route('/api/seller', methods=['GET'])
def get_seller():
    email = request.args.get('email')
    seller = find_seller(email)
    if seller:
        return jsonify(seller), 200
    else:
        return jsonify({"message": "Seller not found"}), 404

@app.route('/api/seller/update', methods=['POST'])
def update_seller():
    data = request.get_json() or {}
    email = data.get('email')
    seller = find_seller(email)
    if not seller:
        return jsonify({'message': 'Seller not found'}), 404
    seller['name'] = data.get('name', seller['name'])
    seller['business'] = data.get('business', seller['business'])
    return jsonify({'message': 'Profile updated', 'seller': seller}), 200

@app.route('/api/seller/add-product', methods=['POST'])
def add_product():
    data = request.get_json() or {}
    email = data.get('email')
    seller = find_seller(email)
    if not seller:
        return jsonify({'message': 'Seller not found'}), 404
    new_product = {
        'id': max([p['id'] for p in seller['products']] + [0]) + 1,
        'name': data.get('name'),
        'desc': data.get('desc'),
        'img': data.get('img')
    }
    seller['products'].append(new_product)
    return jsonify({'message': 'Product added', 'product': new_product, 'products': seller['products']}), 200

@app.route('/api/seller/remove-product', methods=['POST'])
def remove_product():
    data = request.get_json() or {}
    email = data.get('email')
    product_id = data.get('id')
    seller = find_seller(email)
    if not seller:
        return jsonify({'message': 'Seller not found'}), 404
    seller['products'] = [p for p in seller['products'] if p['id'] != product_id]
    return jsonify({'message': 'Product removed', 'products': seller['products']}), 200

# Stripe Payment Endpoints
@app.route('/api/create-payment-intent', methods=['POST'])
@require_auth
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get('amount')  # Amount in cents
        currency = data.get('currency', 'usd')
        product_name = data.get('productName', 'Product')

        # Create a PaymentIntent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata={
                'product_name': product_name,
                'user_id': g.user_id,
                'user_email': g.user_email
            }
        )

        return jsonify({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        print(f"Payment succeeded: {payment_intent['id']}")
        # You can add logic here to update your database, send confirmation emails, etc.

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(port=4000, debug=True) 