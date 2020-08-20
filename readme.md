# MobaHinted
This is a tool for League of Legends that will have functionality similar to
Blitz / Mobalytics primarily, with the exclusion of ads, paid features, and the
inclusion of it just actually working while having everything you need.

Made out of grief from Blitz refusing to remove ads in favor of a paid model and
both Mobalytics and Blitz commonly just not even having correct builds or
stats on matchups or even failing to import at critical moments, and completely
missing features like suggesting counter picks from your champion pool.

It won't have crazy in-depth statistics on people like Mobalytics does,
but just go use that if you want to look at someone specific - that isn't
helpful to look at in game anyway.

## Status

This is rather early on in development, and I've never made desktop GUI software before, so I'm sure there will be lots of hiccups.

You can stay tuned by Watching the project in the top right, or checking the [Todo List](https://github.com/zbee/mobahinted/projects/1).

## Setup

To spin it up you should just need Python 3.7+ and to run the following command
to set up the virtual environment and install the requirements.

`virtualenv venv
    && pip install -r requirements.txt`
    
You'll also need an `.env` file setup with the following variables.

- `riotKey` your [Riot API key](https://developer.riotgames.com/)

Then you can build the executable.

```
python build.py
```

Now you can run `main.exe`.

## What's the catch?

Nah. I play League, the clients/tools are annoying, and I want one that has all of my favorite features without the ads or anything like that.

If you want to thank me, then send me an email, report an issue, or star this repository; there is also a Sponsor option for one-off gifts, go crazy.

### Privacy

No data is automatically transmitted to me, except if you enable periodic information dumps (disabled by default) for analytics and debugging purposes, or if you include it in the feedback form. The exact data included is up to you to select.

If you opt to use data from my server instead of downloading it, then whatever data about you is available to CloudFlare and DigitalOcean, I only track occurences of data access, no user data. It's faster not to, but league data is pretty fat - particularly in its initial download.

There are also lots of API requests of course, so Riot has access to whatever data about you, too. But if you don't want them to have your data, then you'd have to not play league ... so ...

## License
This software is licensed under GPLv3, and as such can be shared freely. Crediting me is good.

"Copyright 2020 Ethan Henderson <ethan@zbee.codes>"

```
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
