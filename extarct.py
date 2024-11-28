import requests

# Replace these values with your actual access token and post ID
access_token = 'EAAoJBWEF2vcBO19T8pjb5lSYGaNStgCyMjnsiYe7eUOjqZBeC7tnH3UNSuxcYZBASafdaIjWPB66cmHpfUj3ZBE9e2TQgxA0QKoZCMYaLpUqSG13suLPDDFcOBEZCF4AFk4eydZCMKhsgxdKZBcpPE7OOoWfUTvPIOUNtu5KwUKY9JJNrVZAZCu7dkZCh5YtuNDg54zXp8jUKiaZA4PjsHS0QZDZD'
post_id = '597243659339276'  # e.g., '1234567890123456'

# Construct the URL
url = f'https://graph.facebook.com/{post_id}?access_token={access_token}'

# Make the request
response = requests.get(url)
data = response.json()

# Print the post data
print(data)
