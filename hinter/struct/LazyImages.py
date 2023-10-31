#     MobaHinted Copyright (C) 2020 Ethan Henderson <ethan@zbee.codes>    #
#  Licensed under GPLv3 - Refer to the LICENSE file for the complete text #

from typing import Union

import cassiopeia
import hinter


class Item:
    item: Union[cassiopeia.core.match.Item, None]
    filler: bool

    def __init__(self, item: Union[cassiopeia.core.match.Item, None]):
        self.item = item
        self.filler = item is None

    @property
    def lazy(self) -> str:
        if self.filler:
            return hinter.UI.filler_image

        return hinter.UI.load_image(
            f'item-{self.item.id}',
            hinter.data.constants.IMAGE_TYPE_PIL,
            self.item.image,
            size=hinter.data.constants.ICON_SIZE_ITEM,
        )


class Rune:
    rune: Union[cassiopeia.core.match.Rune, None]
    filler: bool
    secondary: bool

    def __init__(self, rune: Union[cassiopeia.core.match.Rune, None], secondary: bool = False):
        self.rune = rune
        self.filler = rune is None
        self.secondary = secondary

    @property
    def lazy(self) -> str:
        if self.filler:
            return hinter.UI.filler_image

        if self.secondary:
            return hinter.UI.load_image(
                f'rune-{self.rune.path.name}',
                hinter.data.constants.IMAGE_TYPE_PIL,
                self.rune.path,
                size=hinter.data.constants.ICON_SIZE_SECONDARY_RUNE,
            )

        return hinter.UI.load_image(
            f'rune-{self.rune.name}',
            hinter.data.constants.IMAGE_TYPE_PIL,
            self.rune.image,
            size=hinter.data.constants.ICON_SIZE_RUNE,
        )


# noinspection DuplicatedCode
class SummonerSpell:
    summoner_spell: Union[cassiopeia.core.match.SummonerSpell, None]
    filler: bool

    def __init__(self, summoner_spell: Union[cassiopeia.core.match.SummonerSpell, None]):
        self.summoner_spell = summoner_spell
        self.filler = summoner_spell is None

    @property
    def lazy(self) -> str:
        if self.filler:
            return hinter.UI.filler_image

        return hinter.UI.load_image(
            f'spell-{self.summoner_spell.name}',
            hinter.data.constants.IMAGE_TYPE_PIL,
            self.summoner_spell.image,
            size=hinter.data.constants.ICON_SIZE_SPELL,
        )


class Ban:
    ban: Union[cassiopeia.core.match.Champion, None]
    filler: bool

    def __init__(self, ban: Union[cassiopeia.core.match.Champion, None]):
        self.ban = ban
        self.filler = ban is None

    @property
    def lazy(self) -> str:
        if self.filler:
            return hinter.UI.load_image(
                'champion_ban-filler',
                hinter.data.constants.IMAGE_TYPE_PIL,
                cassiopeia.ProfileIcon(id=29, region=hinter.settings.region),
                size=hinter.data.constants.ICON_SIZE_BAN,
            )

        return hinter.UI.load_image(
            f'champion_ban-{self.ban.name}',
            hinter.data.constants.IMAGE_TYPE_PIL,
            self.ban.image,
            size=hinter.data.constants.ICON_SIZE_BAN,
        )
