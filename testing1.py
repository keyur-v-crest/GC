from twilio.rest import Client

twillio_sid = "ACf5c9d0593e0a7dcec603f169b646baa9"
twillio_token = "285248a81def867954e6438b8f1a0862"
twillio_number = "+12192584349"

client = Client(twillio_sid, twillio_token)
message = client.messages.create(
    body="Your otp is sdfhjsdfhjsa",
    from_=twillio_number, 
    to="+916354757251"
)

print(message.sid)