This is an Astronomy discord bot (now verified!) with various functionalities and uses; created with python 3.10.3 version involving the discord.py module.

### Note : The bot will be moving to slash commands effective 1 May hence all users are required to reinvite the bot (no need to kick) so as to give slash command permissions. Use the link below. Ignore if invited after 5 April or done already.

## Table of contents
* [Invite](#Invite)
* [Commands](#Commands)
* [Sources](#Sources)
* [Vote](#Vote)
* [Targets](#Targets)
* [Creator](#Creator)



## Invite

Use the below discord invitation link to bring AstroBot to your server/guild:

https://discord.com/api/oauth2/authorize?client_id=792458754208956466&permissions=2147544064&scope=bot%20applications.commands



## Commands
As of now, there are the following commands:
* [.help](#help)
* [.daily](#daily)
* [.daily `YYYY-MM-DD`](#daily-yyyy-mm-dd)
* [.daily random](#daily-random)
* [.info `<query>`](#info-query)
* [.iss ](#iss)
* [.channel](#channel)
* [.remove](#remove)
* [.fact](#fact)
* [.weather `<location>`](#weather-location)
* [.sky `<location>`](#sky-location)
* [.phase `<location>`](#phase-location)
* [.webb](#webb)

#### `.help`
Returns the same list of commands that are listed below.

#### `.daily`
Gives the NASA APOD picture for the day. 

Made using the discord embeds and the APOD api.

#### `.daily <YYYY-MM-DD>`
Gives the NASA picture for a specific date given by a user. Any valid date after 1995-6-16 is accepted.
For eg. `.daily 2005-6-7`

#### `.daily random`
Gives a random NASA APOD picture from archives. Including all pictures from 1996.

#### `.info <query>`
Ask about ANYTHING related to astronomy and astronomical bodies. It gives data and pictures related to the given query.

This uses Solar system Open Api and Wikpedia's API in a discord embed.

#### `.iss`
Find the live location of the international space station with respect to the Earth.
This uses the reverse_geocoder python library and the WhereTheIssAt API.
#### `.channel`
Subscribe to the daily APOD service and get the daily picture as soon as it is released on the channel in which this command is posted.

#### `.remove`
Remove a channel from the APOD subscription.

#### `.fact`
Get a random astronomy fact from the fact library.

#### `.weather <location>`
Get the real-time weather at any location

#### `.phase <location>`
Get the phase of the moon at a user specified location

#### `.sky <location>`
Get a map of the sky at a user specified location

#### `.webb`
Get the current state of the James Webb Space Telescope.
## Sources

Given below is the list of APIs/Sources Astrobot uses for its commands (list incomplete)

1. NASA's Astronomy Picture of The Day service
2. Wikipedia API

## Vote

You can vote for the bot so as to get more exposure at - 

https://top.gg/bot/792458754208956466/vote

https://discordbotlist.com/bots/astrobot-2515/upvote

## Targets
1. [ ] Improve `.iss` to have the names of people in the ISS - using OpenNotify and https://awesomeopensource.com/project/corquaid/international-space-station-APIs

2. [ ] Integrate tools like SunCalc and MoonCalc

3. [ ] Improve `.info` to give only data and bring in `.image` to give images (50% done)

4. [ ] Possibly use SpaceFlight News API

5. [ ] Add video demos to README file

6. [ ] Use NASA's PDS Search API

## Creator

This bot has been created with blood, sweat and tears by Advaith GS.

Find me on: https://advaithgs.repl.co <br>
Discord: `AdvaithGS#6700` <br>
email : advaith.gs4@gmail.com <br>


And that's it !
