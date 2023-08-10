# Misko Terapija

Misko Terapija is a web application built with Django that allows users to reserve their stay and make payments. It includes a moderator system for managing all models, a gallery feature for showcasing photos, and a reservation filtering feature.

## Features

- Reservation system
- Payment processing
- User dashboard to manage reservations
- Admin dashboard to manage reservations and users
- Moderator system for managing models: House, Gallery
- Gallery feature for showcasing photos
- Reservation filtering for easy search and navigation of unreserved houses

## Installation

1. **Upload the Database**: Since the application relies on a database, you need to upload the database file. 

2. Change into the project directory:

   ```shell
   cd misko-terapija
   ```

3. Create a virtual environment:

    ```shell
    python -m venv venv
    ```

4. Activate the virtual environment:
    For macOS/Linux:

    ```shell
    source venv/bin/activate
    ```
    For Windows:

    ```
    venv\Scripts\activate
    ```

5. Install the dependencies:

    ```shell
    python manage.py migrate
    ```

6. Create a superuser:

    ```shell
    python manage.py createsuperuser
    ```

7. Start the development server:

    ```shell
    python manage.py runserver
    ```

8. Access the admin dashboard in your browser at http://localhost:8000/admin. Use the superuser credentials created in the previous step to log in.

## Usage

- As an admin, you can manage reservations and users through the admin dashboard.
- As a moderator, you have access to the moderator system where you can manage models as: House, Gallery and delete Reservations.
- The reservation filtering feature allows users to search and navigate through available reservations easily.
- Users can filter houses based on chosen dates to view houses that are available for reservation on those specific dates.
