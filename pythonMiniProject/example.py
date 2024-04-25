import smtplib
import requests
from email.message import EmailMessage
import csv
import time
import datetime
import os


SENDER_EMAIL= os.environ.get('SENDER_EMAIL')
RECIEVER_EMAIL= os.environ.get('RECEIVER_EMAIL')
EMAIL_PASSWORD= os.environ.get('EMAIL_PASSWORD')
API_KEY= os.environ.get('API_KEY')
def fetch_news(api_key, country='us', category='technology', page_size=5):
    url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&pageSize={page_size}&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['articles']

def create_newsletter(articles):
    newsletter = "<!DOCTYPE html>"
    newsletter += "<html lang='en'>"
    newsletter += "<head>"
    newsletter += "<meta charset='UTF-8'>"
    newsletter += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    newsletter += "<title>Email Newsletter</title>"
    newsletter += "<style>"
    newsletter += "body { font-family: Arial, sans-serif; background-color: #f7f7f7; margin: 0; padding: 0; }"
    newsletter += ".container { max-width: 600px; margin: 0 auto; padding: 20px; background-color: #E1F5FE; border-radius: 10px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); }"
    newsletter += "h1, h2, h3 { color: #333333; }"
    newsletter += "p { color: #666666; line-height: 1.6; }"
    newsletter += ".button { display: inline-block; padding: 10px 20px; background-color: #FFCDD2; color: #ffffff; text-decoration: none; border-radius: 5px; }"
    newsletter += ".button:hover { background-color: #ff8000; }"
    newsletter += "</style>"
    newsletter += "</head>"
    newsletter += "<body>"
    newsletter += "<div class='container'>"
    newsletter += "<h1 align='center'>Welcome to TechBytes!</h1>"

    for article in articles:
        title = article['title']
        description = article['description']
        url = article['url']

        newsletter += f"<h2>{title}</h2>"
        newsletter += f"<p>{description}</p>"
        newsletter += f"<a href='{url}' class='button'>Read More</a>"
        newsletter += "<hr>"

    newsletter += "</div>"
    newsletter += "</body>"
    newsletter += "</html>"
    return newsletter



def send_email(sender_email, password, receiver_email, subject, body):
    with open('Pyemail.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                receiver_email = row[0]  # Assuming email addresses are in the first column of the CSV
                if "@" in receiver_email:  # Check if the extracted value appears to be a valid email address
                    msg = EmailMessage()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = subject
                    unsubscribe_link = f'{{ url_for("unsubscribe") }}={receiver_email}'
                    body_with_unsubscribe = body.replace("{email}", unsubscribe_link)
                    msg.add_alternative(body_with_unsubscribe, subtype='html')

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender_email, password)
                        smtp.send_message(msg)
                else:
                    print(f"Invalid email address found: {receiver_email}. Skipping...")
            else:
                print("Empty row found. Skipping...")

def send_weekly_newsletter():
    # Your News API key
    api_key = API_KEY

    # Fetch news articles
    articles = fetch_news(api_key)

    # Generate newsletter body
    newsletter_body = create_newsletter(articles)

    # Email details
    sender_email = SENDER_EMAIL
    password = EMAIL_PASSWORD
    receiver_email = RECIEVER_EMAIL
    subject = 'Tech News Digest'

    # Send email
    send_email(sender_email, password, receiver_email, subject, newsletter_body)

# Function to calculate time until next weekday at given time
def time_until_next_weekday():
    today = datetime.date.today()
    next_thursday = today + datetime.timedelta((3 - today.weekday()) % 7)  # Calculate the next Thursday
    next_thursday_time = datetime.datetime.combine(next_thursday, datetime.time(10,00 ))  # Combine with time
    now = datetime.datetime.now()
    time_difference = next_thursday_time - now
    return time_difference.total_seconds()

# Run the task every weekday at given time
while True:
    time_difference = time_until_next_weekday()
    if time_difference > 0:
        time.sleep(time_difference)
        send_weekly_newsletter()
    else:
        # If it's already past given weekday, schedule for next week
        time.sleep(7 * 24 * 60 * 60)  # Wait for 7 days