KIKO'S KIBANDASKI HOTEL FOOD ORDERING WEBSITE

SETUP IN PYCHARM (WINDOWS)
1. Extract this ZIP file.
2. Open the extracted HotelOrderingSystem folder in PyCharm.
3. Open the PyCharm Terminal (bottom of the window).
4. Create a virtual environment (optional but recommended):
       python -m venv .venv
5. Activate it in PowerShell:
       .venv\Scripts\Activate.ps1
   If PowerShell blocks activation, use Command Prompt:
       .venv\Scripts\activate.bat
6. Install Flask:
       pip install -r requirements.txt
7. Run main.py using the green Run button, or:
       python main.py
8. Open this address in your browser:
       http://127.0.0.1:5000

FEATURES
- Account registration and login; passwords are stored as secure hashes.
- SQLite database for users, menu, orders, order items and feedback.
- Menu categories, shopping cart, checkout and order confirmation.
- Header and footer are reusable HTML partials.
- Python functionality is separated into modules/Blueprints.

IMPORTANT
- This is a learning/demo project. Payment is NOT processed. The two checkout choices
  are cash on delivery and a clearly labelled demo payment option.
- Do not enter or store real card details in this demo. A real M-Pesa/card gateway
  requires a properly configured payment provider and server-side verification.
- Change the Flask SECRET_KEY before deployment. Turn debug=False in production.
- Update the sample hotel name, contact details and social links before publishing.
- The database file is created automatically the first time the app runs.
