import os
import send2trash
import gspread
import tweepy

# Set up the Twitter API client
auth = tweepy.OAuth1UserHandler(
    consumer_key='consumer key',
    consumer_secret='consumer secret',
    access_token='access token',
    access_token_secret='access token secret',
)

api = tweepy.API(auth)

# Set up the Google Sheets client
gc = gspread.service_account('credentials.json')
sheet = gc.open("your sheet here").sheet1

# Get the text of the next tweet
tweet_text = sheet.acell('A1').value

# Set the folder path
folder_path = r'path\to\folder'

# Get the list of image files in the folder, sorted by the time they were added
image_files = sorted(
    [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.gif'))],
    key=lambda x: os.path.getmtime(os.path.join(folder_path, x)),
)

if image_files:
    # Use the oldest image file
    image_path = os.path.join(folder_path, image_files[0])

    with open(image_path, 'rb') as image:
        media_response = api.media_upload(filename=image_files[0], file=image)
        media_id = media_response.media_id

else:
    print("No image files found in the specified folder.")

# Post the tweet with the image
api.update_status(status=tweet_text, media_ids=[media_id])

sheet.delete_rows(1)
send2trash.send2trash(image_path)

# you can add this if you want to see which image was posted
#print(tweet_text)