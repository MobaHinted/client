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