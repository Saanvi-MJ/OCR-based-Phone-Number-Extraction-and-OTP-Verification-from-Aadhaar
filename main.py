import cv2
import pytesseract
import re
from twilio.rest import Client
import random
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_phone_number(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        return "Error: Unable to load the image. Check the file path or format."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    phone_pattern = r'\b[6-9]\d{9}\b'
    phone_numbers = re.findall(phone_pattern, text)

    if phone_numbers:
        return phone_numbers[0]  
    else:
        return None

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone_number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "---")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "---")
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER", "---")  

   
    otp = generate_otp()
    
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=twilio_phone_number,
        to=f"+91{phone_number}"
    )
    return otp, message.sid

image_path = r"Aadhaar card.jpg"
phone_number = extract_phone_number(image_path)

if phone_number:
    print(f"Extracted Phone Number: {phone_number}")
    try:
        otp, message_sid = send_otp(phone_number)
        print(f"OTP sent successfully! OTP: {otp}, Message SID: {message_sid}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
else:
    print("No phone number found in the image.")
