# MobaHinted
This is a tool for League of Legends that will have functionality similar to
Blitz / Mobalytics primarily, with the exclusion of ads, paid features, and the
inclusion of it just actually working while having everything you need.

Made out of grief from Blitz refusing to remove ads (I'd pay for that) and
both Mobalytics and Blitz commonly just not even having correct builds or
stats on matchups and completely missing features like suggesting counter
picks from your champion pool.

It won't have crazy in-depth statistics on people like Mobalytics does,
but just go use that if you want to look at someone specific - that isn't
helpful to look at in game anyway.

## Setup

To spin it up you should just need Python 3.7 and to run the following command
to set up the virtual environment and install the requirements.

`virtualenv --no-site-packages --distribute .env
    && source .env/bin/activate
    && pip install -r requirements.txt`