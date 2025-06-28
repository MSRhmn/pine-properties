# 🏡 Pine Properties — Real Estate Web Application

A responsive, easy-to-use real estate platform built with Django and Bootstrap. Showcase property listings, highlight property details, and handle contact inquiries via a simple, secure contact form.


## Features

- Property listings with images  
- Dedicated property detail pages  
- Responsive Bootstrap-based frontend  
- Contact form with email integration  
- Admin panel for property management  
- Environment variables for secure credentials  
- Minimal project structure  


## Setup Instructions

### 1️. Clone the Repository

  `git clone https://github.com/your-username/pine-properties.git`<br>

  `cd pine-properties`


### 2. Create a Virtual Environment

  `python -m venv venv`<br>
  
  `source venv/bin/activate`  # On Windows: venv\Scripts\activate


### 3. Install Dependencies

  `pip install -r requirements.txt`

### 4. Configure Environment Variables

Copy the example environment file and edit .env file with your own email credentials to perform functional contact form:

  `cp .env.example .env`



  - EMAIL_HOST_USER=your-email@example.com
  - EMAIL_HOST_PASSWORD=your-password
  - CONTACT_EMAIL=recipient@example.com


### 4. Apply Migrations

  `python manage.py migrate`

### 5. Run the Development Server

  `python manage.py runserver`
