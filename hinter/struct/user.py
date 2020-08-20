import hinter


class User:
    user_exists: bool = None
    username: str = ''
    account_id: str = ''
    level: int = 0
    icon: str = ''

    def __init__(self, username: str):
        # Check user exists on Riot's side
        try:
            user = hinter.watcher.summoner.by_name(
                hinter.settings.region,
                username
            )
        except Exception as e:
            self.user_exists = False
            return

        # Load in data
        self.user_exists = True
        self.username = user['name']
        self.account_id = user['accountId']
        self.level = user['summonerLevel']
        self.icon = user['profileIconId']
