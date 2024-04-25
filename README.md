**NEWSLETTER AUTOMATION **

This Python mini-project involves creating a newsletter subscription form using Flask. The main.py file includes routes for form submission, validation, writing emails to a CSV file, and success message rendering. The Index.html file contains the newsletter subscription form with email validation and styling. The example.py file fetches news articles using an API, generates an HTML newsletter, and sends it as an email to subscribers listed in a CSV file. The Bootstrap code at the end is a snippet from Bootstrap v4.5.2 defining functionality for alerts and buttons, enhancing user interaction on web pages.

This project demonstrates a Flask-based newsletter automation system that collects user emails, generates a newsletter from external news sources, and sends the newsletter to registered users via email. The project consists of two main components:

**Flask Web Application**: The web application uses Flask to create a simple registration form for users to submit their email addresses. It uses Flask-WTF for form validation and CSV files to store the registered emails. The application has two routes: one for the registration form and another for a success message after registration.

**Newsletter Generation and Sending**: This script fetches news articles from a news API and generates an HTML-based newsletter containing article titles, descriptions, and links for further reading. The newsletter is sent to registered users using SMTP, ensuring secure communication. Email addresses are read from a CSV file, allowing flexibility and scalability in managing subscriber lists.

Overall, this project aims to automate the process of creating and distributing a daily newsletter. It leverages Flask for user interaction and SMTP for email communication, providing an efficient solution for sending regular newsletters to a list of registered subscribers.
