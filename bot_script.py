import praw
import logging
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='reddit_bot.log', level=logging.INFO)

def main():
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )

        # Test authentication
        user = reddit.user.me()
        logging.info(f"Authenticated as {user.name}")
        print(f"Authenticated as {user.name}")

        subreddit = reddit.subreddit('germanshepherds')

        for submission in subreddit.stream.submissions(skip_existing=True):
            try:
                logging.info(f"New submission detected: {submission.title} - {submission.url}")
                print(f"New submission detected: {submission.title} - {submission.url}")

                # Check if the submission is a photo
                if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    logging.info(f"Photo post found: {submission.title}")
                    print(f"Photo post found: {submission.title}")
                    submission.reply("good dog")
                    logging.info(f"Replied to post {submission.id}")
                    print(f"Replied to post {submission.id}")
                time.sleep(10)  # Avoid hitting rate limits
            except Exception as e:
                logging.error(f"Error processing submission {submission.id}: {e}")
                print(f"Error processing submission {submission.id}: {e}")
                time.sleep(30)  # Wait before retrying on error

    except praw.exceptions.OAuthException as e:
        logging.error(f"OAuthException: {e}")
        print(f"OAuthException: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        time.sleep(60)  # Wait before retrying

if __name__ == "__main__":
    main()





