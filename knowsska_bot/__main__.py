import random
from os import path

import botskeleton

DELAY = 3600
OUR_LOOKBACK_LIMIT = 50
THEIR_LOOKBACK_LIMIT = 40

def main():
    """main"""
    HERE = path.abspath(path.dirname(__file__))
    SECRETS_DIR = path.join(HERE, "SECRETS")
    BOT_SKELETON = botskeleton.BotSkeleton(SECRETS_DIR, bot_name="knowsska_bot", delay=DELAY)

    LOG = BOT_SKELETON.log

    LOG.info("Retrieving BIRDSITE_TARGET_HANDLE...")
    with open(path.join(SECRETS_DIR, "BIRDSITE_TARGET_HANDLE")) as f:
        BIRDSITE_TARGET_HANDLE = f.read().strip()

    LOG.info("Retrieving MASTODON_TARGET_HANDLE...")
    with open(path.join(SECRETS_DIR, "MASTODON_TARGET_HANDLE")) as f:
        MASTODON_TARGET_HANDLE = f.read().strip()

    while True:
        BOT_SKELETON.perform_batch_reply(
            callback=choose_answer,
            lookback_limit=20,
            target_handles={
                "birdsite": BIRDSITE_TARGET_HANDLE,
                "mastodon": MASTODON_TARGET_HANDLE,
            })

        BOT_SKELETON.nap()


def choose_answer(*, message, message_id, **kwargs):
    # the format we're trying to reverse-engineer and pull stuff out of is
    # "Is {album_name} by {artist_name} ska?"
    identifying_chunk = message[3:]

    index = identifying_chunk.find("ska?")
    identifying_chunk = identifying_chunk[:index-1]

    # choose our answer.
    random.seed(message_id)
    if random.random() < 0.15:
        if identifying_chunk is not None:
            answer = f"Yes, {identifying_chunk} is ska!"
        else:
            answer = "Yes, that's ska!"
    else:
        if identifying_chunk is not None:
            answer = f"No, {identifying_chunk} is definitely not ska!"
        else:
            answer = "No, that isn't ska!"

    return answer


if __name__ == "__main__":
    main()
