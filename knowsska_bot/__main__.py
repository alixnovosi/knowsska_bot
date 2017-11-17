from os import path

import botskeleton

DELAY = 3600
OUR_LOOKBACK_LIMIT = 50
THEIR_LOOKBACK_LIMIT = 40

if __name__ == "__main__":
    HERE = path.abspath(path.dirname(__file__))
    SECRETS_DIR = path.join(HERE, "SECRETS")
    BOT_SKELETON = botskeleton.BotSkeleton(SECRETS_DIR, bot_name="knowsska_bot", delay=DELAY)

    LOG = botskeleton.set_up_logging()

    LOG.info("Retrieving TARGET_ID...")
    with open(path.join(SECRETS_DIR, "TARGET_ID")) as f:
        TARGET_ID = f.read().strip()

    LOG.info("Retrieving TARGET_HANDLE...")
    with open(path.join(SECRETS_DIR, "TARGET_HANDLE")) as f:
        TARGET_HANDLE = f.read().strip()

    while True:
        # Get our statuses so we can tell if we've replied before.
        statuses = BOT_SKELETON.api.user_timeline(screen_name="knowsska_bot",
                                                  count=OUR_LOOKBACK_LIMIT)

        in_reply_to_ids = list(map(lambda x: x.in_reply_to_status_id, statuses))
        LOG.info(f"Found reply-to ids: {in_reply_to_ids}")

        # Get their last N statuses.
        statuses = BOT_SKELETON.api.user_timeline(screen_name=TARGET_HANDLE,
                                                  count=THEIR_LOOKBACK_LIMIT)

        for status in statuses:

            id = status.id

            # Make sure we haven't replied to this status before.
            if id not in in_reply_to_ids:

                # Choose our answer.
                if id % 2 == 0:
                    answer = "Yes"
                else:
                    answer = "No"

                LOG.info(f"Replying {answer} to status {id} from {TARGET_HANDLE}.")
                BOT_SKELETON.api.update_status(f"@{TARGET_HANDLE} {answer}",
                                               in_reply_to_status_id=id)

                LOG.info("Sleeping for a bit between tweets.")
                BOT_SKELETON.delay = DELAY/60
                BOT_SKELETON.nap()

            else:
                LOG.info(f"Not replying to status {id} from {TARGET_HANDLE} - we already replied.")

        LOG.info("Sleeping for longer between searches for tweets.")
        BOT_SKELETON.delay = DELAY
        BOT_SKELETON.nap()
