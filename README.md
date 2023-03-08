<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap" rel="stylesheet">
<span style="font-family:'Playfair Display',serif;">


This is an Astronomy discord bot with various functionalities and uses; created with python 3.10 and disnake. 

## Table of contents
* [Invite](#Invite)
* [Commands](#Commands)
* [Sources](#Sources)
* [Vote](#Vote)
* [Support](#Support)
* [Targets](#Targets)
* [Creator](#Creator)



## Invite

Use the below link to invite AstroBot to your server:

https://discord.com/api/oauth2/authorize?client_id=792458754208956466&permissions=2147534848&scope=bot


## Commands
As of now, there are the following commands:
* [help](#help-or-astrobot-help)
* [daily](#daily-or-astrobot-daily)
* [daily `YYYY-MM-DD`](#daily-yyyy-mm-dd-or-astrobot-daily-yyyy-mm-dd)
* [daily random](#daily-random-or-astrobot-daily-random)
* [info `<query>`](#info-query-or-astrobot-info-query)
* [iss ](#iss-or-astrobot-iss)
* [channel](#channel-or-astrobot-channel)
* [remove](#remove-or-astrobot-remove)
* [fact](#fact-or-astrobot-fact)
* [weather `<location>`](#weather-location-or-astrobot-weather-location)
* [sky `<location>`](#sky-location-or-astrobot-sky-location)
* [phase `<location>`](#phase-location-or-astrobot-phase-location)
* [webb](#webb-or-astrobot-webb)
* [in_space](#in_space)




#### `/help` or `@AstroBot help`
Returns the same list of commands that are listed below.

#### `/daily` or `@AstroBot daily`
Gives the NASA APOD picture for the day. 

Made using the discord embeds and the APOD api.

#### `/daily <YYYY-MM-DD>` or `@AstroBot daily <YYYY-MM-DD>`
Gives the NASA picture for a specific date given by a user. Any valid date after 1995-6-16 is accepted.
For eg. `/daily 2005-6-7` or `@AstroBot daily 2005-6-7`

#### `/daily random` or `@AstroBot daily random`
Gives a random NASA APOD picture from archives. Including all pictures from 1996.

#### `/info <query>` or `@AstroBot info <query>`
Ask about ANYTHING related to astronomy and astronomical bodies. It gives data and pictures related to the given query.

This uses Solar system Open Api and Wikpedia's API in a discord embed.

#### `/iss` or `@AstroBot iss`
Find the live location of the international space station with respect to the Earth.
This uses the reverse_geocoder python library and the WhereTheIssAt API.
#### `/channel` or `@AstroBot channel`
Subscribe to the daily APOD service and get the daily picture as soon as it is released on the channel in which this command is posted.

#### `/remove` or `@AstroBot remove`
Remove a channel from the APOD subscription.

#### `/fact` or `@AstroBot fact`
Get a random astronomy fact from the fact library.

#### `/weather <location>` or `@AstroBot weather <location>`
Get the real-time weather at any location

#### `/phase <location>` or `@AstroBot phase <location>`
Get the phase of the moon at a user specified location

#### `/sky <location>` or `@AstroBot sky <location>`
Get a map of the sky at a user specified location

#### `/webb` or `@AstroBot webb`
Get the current state of the James Webb Space Telescope.

#### `/in_space`
Get info about the people currently in space in the ISS or in other stations.

## Sources

Given below is the list of APIs/Sources Astrobot uses for its commands
1. [AstronomyAPI](https://github.com/AstronomyAPI/Samples)
2. [Geopy Library](https://github.com/geopy/geopy)
3. [NASA's Astronomy Picture of The Day](https://github.com/nasa/apod-api)
4. [OpenWeatherMap API](https://openweathermap.org/api)
5. [reverse_geocode library](https://github.com/thampiman/reverse-geocoder)
6. [Wikimedia API](https://api.wikimedia.org/wiki/Main_Page)
7. [WhereTheISSAt api](https://wheretheiss.at/w/developer)

## Vote

You can vote for the bot so as to get more exposure at - 

https://top.gg/bot/792458754208956466/vote

https://discordbotlist.com/bots/astrobot-2515/upvote

## Support

Join this discord server for any queries/problems/suggestions:
 
https://discord.gg/ZtPU67wVa5

## Targets
1. [ ] Add mars rover cam images

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
</span>
