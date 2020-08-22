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

This is rather early on in development, and I've never made desktop GUI software
before, so I'm sure there will be lots of hiccups.

You can stay tuned by Watching the project in the top right, or checking the
[Todo List](https://github.com/zbee/mobahinted/projects/1).

## Setup

To spin it up you should just need Python 3.7+ and to run the following command
to set up the virtual environment and install the requirements.

`virtualenv venv
    && pip install -r requirements.txt`
    
You'll also need an `.env` file setup with the following variables.

- `RIOT_API_KEY` your [Riot API key](https://developer.riotgames.com/)

Then you can build the executable.

```
python build.py
```

Now you can run `main.exe`.

## What's the catch?

Nah. I play League, the clients/tools are annoying, and I want one that has all
of my favorite features without the ads or anything like that.

### Privacy

No data is automatically transmitted to me, except if you enable periodic
information dumps (disabled by default) for analytics and debugging purposes,
or if you include it in the feedback form.
The exact data included is up to you to select.

Your API requests are proxied through my server for caching and better rate
limiting, I'm just log accesses, but CloudFlare and DigitalOcean will have
access to your data.

If you prefer, you can set up an environment variable as described in the Setup
section above, and then your API requests won't be proxied, but then Riot will
have all that data; though you're already playing League ... so ...

## Contributing

The biggest contribution would be trying it out, and opening an issue if you
find one.

If you want to code on this, try fixing an issue, or implementing something from
the ToDo list, and opening a pull request. If it all works out fine, we can talk
about adding you as a contributor.

If you want to thank me, then send me an email, report an issue, or star this
repository; there is also a Sponsor option on the Github page for one-off gifts,
go crazy.

## License
This software is licensed under GPLv3, and as such can be shared freely.
Crediting me is good.

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

### Attribution

MobaHinted isn't endorsed by Riot Games and does not reflect the views or
opinions of Riot Games or anyone officially involved in producing or managing
League of Legends.
League of Legends and Riot Games are trademarks or registered trademarks of
Riot Games, Inc. League of Legends (c) Riot Games, Inc.

---

[Cassiopeia](https://github.com/meraki-analytics/cassiopeia), 
Copyright (c) 2017 Rob Rua, Jason Maldonis - 
Licensed under the MIT License

[Requests](https://github.com/psf/requests), 
Copyright 2019 Kenneth Reitz - 
Licensed under the Apache License (Version 2.0)

[python-dotenv](https://github.com/theskumar/python-dotenv), 
Copyright (c) 2014, Saurabh Kumar - 
Licensed under the 3-Clause BSD License

[retry](https://github.com/invl/retry), 
Copyright 2014 invl -
Licensed under the Apache License (Version 2.0)
