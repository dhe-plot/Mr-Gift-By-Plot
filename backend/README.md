# Mr. Gift Backend (Flask)

## Setup

1. Install dependencies:
   ```bash
   pip install flask flask-cors flask-mail
   ```

2. Set environment variables for email (Gmail example):
   - `MAIL_USERNAME`: Your Gmail address (e.g. myemail@gmail.com)
   - `MAIL_PASSWORD`: Your Gmail app password (not your main password; see below)

   On Windows PowerShell:
   ```powershell
   $env:MAIL_USERNAME="myemail@gmail.com"
   $env:MAIL_PASSWORD="your-app-password"
   ```

   **How to get a Gmail app password:**
   - Go to your Google Account > Security > App passwords
   - Generate an app password for "Mail"
   - Use that as `MAIL_PASSWORD`

3. Run the backend:
   ```bash
   python app.py
   ```

The backend will run on `http://localhost:4000` and send confirmation emails to new sellers. 

### Note from colleague:
Your Seller Dashboard page has been fully updated to match the attached design!

#### What was changed:
- **SellerDashboard.jsx**: Now includes a sidebar with navigation, profile section, dashboard stats, a sales trends section (with chart placeholder), and a recent orders table with sample data.
- **SellerDashboard.css**: Added for a modern dark theme, matching the style in your screenshot.

#### How to use:
1. Make sure this line is present in your `SellerDashboard.jsx`:
   ```jsx
   import "./SellerDashboard.css";
   ```
2. The dashboard will now look and feel like your attached design, including layout, colors, and table styles.

If you want to connect this to real data or add interactivity (like navigation or a real chart), let me know!