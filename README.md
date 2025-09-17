# Nicky G. Computers - E-commerce Website

A Django-based e-commerce platform for Nicky G. Computers, located in Wa, Upper West Region, Ghana. The website features product sales, service bookings, and integrated WhatsApp communication.

## Features

- **Product Catalog**: Browse computers, phones, and accessories
- **Service Booking**: Computer repairs, internet cafe, WAEC registration, passport photos, document typing, and mobile money services
- **Shopping Cart**: Add products and place orders with Mobile Money payment
- **Smart WhatsApp Integration**: Context-aware messaging for inquiries and orders
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Professional UI**: SVG icons and smooth user experience

## Tech Stack

- **Backend**: Django 5.2.6
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Render
- **Static Files**: WhiteNoise

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create sample data (optional):
   ```bash
   python create_sample_data.py
   ```
7. Start development server:
   ```bash
   python manage.py runserver
   ```

## Deployment to Render

### Prerequisites
- GitHub repository with your code
- Render account

### Steps

1. **Connect Repository**: Link your GitHub repo to Render

2. **Configure Web Service**:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn nickyg_computers.wsgi:application`
   - **Environment**: Python 3

3. **Set Environment Variables** in Render dashboard:
   ```
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

4. **Database**: Render will automatically provide `DATABASE_URL` for PostgreSQL

5. **Deploy**: Render will automatically build and deploy your app

### Important Notes

- The app uses WhiteNoise for static file serving
- Database migrations run automatically during build
- Static files are collected during build process
- HTTPS is enforced in production

## Business Information

- **Location**: In-between GCB Ltd and La France, Near New OA Station, Wa, Upper West Region, Ghana
- **Phone**: +233 24 764 4599 / +233 20 428 8305
- **Email**: nickygcomputers@gmail.com
- **WhatsApp**: 0204288305
- **Mobile Money**: 0597427569

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Development key |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `DATABASE_URL` | Database connection string | SQLite (auto-provided by Render) |
| `EMAIL_HOST_USER` | Email account for sending notifications | `nickygcomputers@gmail.com` |
| `EMAIL_HOST_PASSWORD` | App password for email account | Required for production |
| `ADMIN_EMAIL` | Email to receive admin notifications | `nickygcomputers@gmail.com` |

## Email Notifications

The system automatically sends email alerts for:

- **New Orders**: Detailed order information with customer details and items
- **Contact Form Submissions**: Customer inquiries and messages
- **Low Stock Alerts**: Products running low on inventory (via management command)

### Setting Up Gmail for Email Notifications

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password as `EMAIL_HOST_PASSWORD`

### Running Low Stock Checks

```bash
# Check for products with 5 or fewer items
python manage.py check_low_stock

# Custom threshold
python manage.py check_low_stock --threshold 10
```

## License

© 2025 Nicky G. Computers. All rights reserved.
