Before running this bot, make sure you set the discord_api_key and
weather_api_key to your bot's token and the token from your
openweathermap.org api key, respectively. example:

[APIdata]
weather_api_key = *your key here*
discord_api_key = *your key here*

if this is not done, the bot WILL raise errors.

currently uses the following external python libraries:

requests (command: pip install requests)
discord (command: pip install discord)

If you want this bot to have role moderation capabilities, you will have 
to give it a role one higher than every other user on the discord. This is optional 
(if you don't need this functionality). The only perm the role needs is the 
'manage roles' perm.
