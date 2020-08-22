import cassiopeia


class User:
    user_exists: bool = None
    username: str = ''
    account_id: str = ''
    level: int = 0
    icon: cassiopeia.ProfileIcon = None

    def __init__(self, username: str):
        # Check user exists on Riot's side
        try:
            user: cassiopeia.Summoner = cassiopeia.Summoner(name=username)

            # Load in data
            self.user_exists = user.exists
            self.username = user.name
            self.account_id = user.account_id
            self.level = int(user.level)
            self.icon = user.profile_icon

        except Exception as err:
            # Actually fail out if it's a bad key issue
            response_code = int(str(err))
            if response_code == 401 or 403:
                raise Exception(err)

            # Otherwise just assume the user doesn't exist, as that'll be the
            #  most common response
            self.user_exists = False
            return
