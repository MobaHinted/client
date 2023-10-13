#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

import cassiopeia
import hinter


class User:
    user_exists: bool = None
    username: str = ''
    account_id: str = ''
    level: int = 0
    icon: cassiopeia.ProfileIcon = None
    # TODO: store the user's region

    def __init__(self, username: str):
        # Check user exists on Riot's side
        try:
            user: cassiopeia.Summoner = cassiopeia.Summoner(name=username, region=hinter.settings.region)

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
