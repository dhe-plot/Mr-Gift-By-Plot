# MR GIFT Setup Guide

This guide will help you set up the MR GIFT application with authentication and payment processing.

## Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- Git

## Environment Setup

### 1. Clerk Authentication Setup

1. Go to [Clerk Dashboard](https://dashboard.clerk.com)
2. Sign up for a free account
3. Create a new application
4. Copy your publishable key and secret key
5. Update the environment files:
   - Frontend: `mr-gift-app/.env`
   - Backend: `backend/.env`

### 2. Stripe Payment Setup

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Sign up for a free account
3. Switch to test mode (toggle in the top right)
4. Go to Developers > API keys
5. Copy your publishable key and secret key
6. Update the environment files with your test keys

### 3. Email Configuration (Optional)

For seller registration emails:
1. Use a Gmail account
2. Enable 2-factor authentication
3. Generate an app password
4. Update `MAIL_USERNAME` and `MAIL_PASSWORD` in `backend/.env`

## Installation

### Frontend Setup

```bash
cd mr-gift-app
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

## Testing

### 1. Start the Application

**Backend:**
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd mr-gift-app
npm install
npm run dev
```

### 2. Test Authentication Flow

1. Navigate to `http://localhost:5173`
2. Click "Sign In" in the top right
3. Test sign-up flow:
   - Click "Sign up" in the modal
   - Create a new account with email/password
   - Complete the onboarding process
4. Test sign-in flow:
   - Sign out and sign back in
   - Verify user profile appears in header

### 3. Test Payment Integration

1. Make sure you're signed in
2. Scroll to "Featured Gifts" section
3. Click "Buy Now" on any gift
4. Fill out payment form with test card:
   - Card: 4242 4242 4242 4242
   - Expiry: Any future date
   - CVC: Any 3 digits
5. Complete payment and verify success message

### 4. Test Story Features

1. View featured stories in the feed
2. Test story interactions:
   - Like/unlike stories
   - Save/unsave stories
   - View user profiles
   - Follow suggestions

## Features Implemented

- ✅ Clerk Authentication (Sign In/Sign Up)
- ✅ User Onboarding Flow
- ✅ Stripe Payment Integration
- ✅ Featured Stories Feed
- ✅ User Profiles with Gifting Stats
- ✅ Seller Registration System

## Troubleshooting

### Common Issues

1. **"Missing Publishable Key" Error**
   - Make sure you've copied your environment files from `.env.example`
   - Verify your Clerk publishable key is set in `mr-gift-app/.env`

2. **Payment Form Not Loading**
   - Check that your Stripe publishable key is correct
   - Ensure both frontend and backend are running
   - Verify CORS is enabled in the backend

3. **Authentication Not Working**
   - Verify Clerk keys are correct in both frontend and backend
   - Check browser console for errors
   - Make sure you're using the correct environment (test vs production)

4. **Backend Connection Issues**
   - Ensure backend is running on port 4000
   - Check that `VITE_API_URL` in frontend `.env` matches backend URL
   - Verify CORS configuration in backend

## Next Steps

- Configure your actual Clerk and Stripe keys
- Test the complete user flow
- Customize the branding and styling
- Add more gift categories and products
- Set up a production database (currently using in-memory storage)
- Configure email settings for seller notifications
- Add more payment methods and currencies
