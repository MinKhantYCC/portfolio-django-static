# Portfolio Website - Django Static

A modern, responsive portfolio website built with Django, featuring a clean and professional design.

## Features

- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern UI**: Clean and professional interface with smooth animations
- **Multiple Sections**: About, Experience, and Projects sections
- **Interactive Navigation**: Smooth page transitions and filtering capabilities
- **Skills Showcase**: Visual representation of technical skills with progress bars

## Technologies Used

- **Backend**: Django 6.0.1
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Ionicons
- **Database**: SQLite3

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolio-django-static
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`

## Project Structure

```
portfolio-django-static/
├── portfolio/              # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   └── ...
├── staticportfolio/       # Main Django app
│   ├── static/           # Static files (CSS, JS)
│   ├── templates/        # HTML templates
│   └── ...
├── static/               # Global static files
├── staticfiles/          # Collected static files
├── templates/            # Global templates
├── db.sqlite3           # SQLite database
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Usage

After starting the development server, you can:

- View the portfolio at the home page
- Navigate between About, Experience, and Projects sections
- Filter projects by category (AI, Web Application, Backend APIs, Chatbot)
- View detailed information about skills and experience

## Deployment

This project is configured for deployment on Vercel. The `ALLOWED_HOSTS` setting includes `.vercel.app` for Vercel deployments.

For production deployment:

1. Set environment variables:
   - `DJANGO_SECRET_KEY`: Your secret key
   - `DEBUG`: Set to `False` for production

2. Run migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

## Credits and Attribution

### Frontend Design

The HTML, CSS, and JavaScript files used in this project are based on a design by **leonam-silva-de-souza** on CodePen.

**Original Source**: [Portfolio Design by leonam-silva-de-souza](https://codepen.io/leonam-silva-de-souza/pen/vYowKqP)

The frontend code has been adapted and integrated into this Django project. All credit for the original HTML structure, CSS styling, and JavaScript functionality goes to the original creator.

## License

This project is open source and available for personal and commercial use. Please ensure you comply with the original CodePen design's license terms when using this project.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or suggestions, please open an issue on the repository.

