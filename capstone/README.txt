---

# CS50W Capstone: Portfolio Website

## Overview

This project is a **Portfolio Website** built using **Django**, **JavaScript**, and **Tailwind CSS**. It highlights my work, skills, and achievements as a software developer with a focus on creating dynamic and immersive web applications.

The portfolio includes:
- Sections for my **resume**, **projects**, and a detailed **About Me** page.
- A two-level **JavaScript cipher game** showcasing interactive problem-solving.
- Advanced features such as:
  - **Dynamic theming** with light and dark modes.
  - **Interactive project showcases** with animations and responsive grids.
  - Downloadable content like my resume.

The website ensures a seamless user experience across all devices by being fully mobile-responsive.

---

## Distinctiveness and Complexity

### Distinctiveness

This project stands out in several ways:
- **Portfolio Focus**: Unlike other course projects (social network or e-commerce site), this is a personal portfolio designed to showcase my skills and achievements.
- **JavaScript Cipher Game**: A unique two-level game that adds interactivity and engagement.
- **Dynamic Theming**: Includes robust light and dark mode implementations, dynamically adapting the design and content.

### Complexity

The project demonstrates complexity in the following areas:

#### Django Back-End:
- Custom models in the `portfolio_content` app for managing portfolio content such as projects, technologies, certificates and downloadable files.
- Advanced querysets and view logic for dynamic filtering and categorization.

#### JavaScript-Driven Front-End:
- A cipher-based mini-game with two levels, including progressively challenging puzzles.
- Dynamic content loading for a smoother user experience.
- Interactive UI elements, such as animations and responsive grids.

#### Responsive Design:
- Tailored styling for different screen sizes, ensuring accessibility on mobile, tablet, and desktop devices.
- Gradient borders and styled elements for enhanced visual appeal.

#### Custom Features:
- Integration of downloadable resume functionality and external links.
- Interactive project showcases and hover effects to elevate user engagement.

---

## File Overview

### Main Files and Their Purpose
```
Capstone/
├── manage.py               # Main Django management script
├── requirements.txt        # List of dependencies
├── README.md               # Project documentation
├── portfolio/              # Core Django project folder
│   ├── settings.py         # Django project configuration
│   ├── urls.py             # URL routing for the project
│   ├── wsgi.py             # WSGI deployment configuration
│   └── asgi.py             # ASGI deployment configuration
├── portfolio_content/      # Django app managing portfolio content
│   ├── models.py           # Defines models for projects, technologies, and media
│   ├── views.py            # Handles logic for rendering pages and processing user interactions
│   ├── urls.py             # Routes URLs specific to this app
│   ├── templates/          # HTML templates for the app
│   │   ├── project_details.html       # Displays detailed information about a project
│   │   ├── problem_set_details.html   # Detailed view for a problem set
│   │   ├── layout.html                # Base layout for consistent design
│   │   ├── lab_details.html           # Displays details for a lab
│   │   ├── level_one.html             # HTML for level 1 of the game
│   │   ├── level_two.html             # HTML for level 2 of the game
│   │   ├── index.html                 # Home page showcasing featured projects
│   │   ├── final_project_details.html # Final project showcase
│   │   ├── courses.html               # Courses listing page
│   │   ├── course_content.html        # Detailed view for a course
│   │   ├── contact.html               # Contact page
│   │   ├── about.html                 # About Me section
│   │   └── 404.html                   # Custom 404 error page
│   └── static/             # Static files (CSS, JavaScript, and images)
│       ├── css/            # Tailwind CSS styles
│       ├── js/             # JavaScript files
│       │   ├── main.js     # Handles general interactivity and theme switching
│       │   ├── level1.js   # JavaScript for Level 1 of the cipher game
│       │   └── level2.js   # JavaScript for Level 2 of the cipher game
├── theme/                  # Custom Tailwind-based styling app
│   ├── static/css/         # Tailwind CSS styles
│   ├── static/js/          # JavaScript for interactivity and theme switching
│   └── templates/          # Optional theme-specific templates
└── media/                  # Media files (uploaded images and downloadable files)
    └── resume.pdf          # Example resume file

```

---

## How to Run the Application

### Clone the Repository:
```bash
git clone https://github.com/JamisBurr/CS50-Web.git
cd CS50-Web
```

### Install Dependencies:
Ensure Python and pip are installed, then run:
```bash
pip install -r requirements.txt
```

### Set Up the Database:
Apply migrations to set up the database schema:
```bash
python manage.py migrate
```

### Create a Superuser (Optional):
If you want to access the admin panel:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username, email, and password.

### Run the Development Server:
Start the Django development server:
```bash
python manage.py runserver
```

### Access the Application:
- Open your browser and navigate to: `http://127.0.0.1:8000/`
- To play the JavaScript cipher game, visit: `http://127.0.0.1:8000/cipher_game/`

---

## JavaScript Cipher Game

The portfolio includes a **JavaScript-based cipher game** with two levels:
- **Level 1:** Introduces users to the cipher mechanics through basic challenges.
- **Level 2:** Increases difficulty with advanced decoding puzzles.
- The game showcases creativity and technical skills in JavaScript.

---

## Additional Information

### Mobile-Responsive Design:
- The application is fully responsive, providing a seamless user experience on mobile, tablet, and desktop devices.

### Dependencies:
- **Django**: Handles the back-end logic.
- **Tailwind CSS**: Provides a responsive and customizable design framework.
- **Other dependencies**: Listed in `requirements.txt`.

### Future Enhancements:
- Adding more levels to the cipher game with integrated leaderboards.
- Implementing a contact form for inquiries.
- Optimizing the website for performance and accessibility.

---

Thank you for reviewing my Portfolio Website! If you have any questions or feedback, feel free to reach out.

---