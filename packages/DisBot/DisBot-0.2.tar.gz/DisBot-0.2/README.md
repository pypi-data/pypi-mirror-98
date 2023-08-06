# Disbot

[Disbot](https://pypi.org/project/DisBot/) is a simple discord py app template generator which helps you to concentrate on implementing the actual commands rather than handling abstraction of commands.

## Commands

For now this only supports creating a quick bot. But in future releases, It will cover the other commands which makes it easier to host (probably in Heroku by default) etc. Please feel free to suggest your requirements through an issue in this project github repo.

To create a new bot, simply use the below command
```
disbot-admin createbot <name-of-the-bot>
```

You can also start with 
```
disbot-admin --help
```

**NOTE** : It is very much advisable that you pip install this package in a virtual environment rather than directly into your local machine.



# Scenes after generating a quick bot

## How to run?

- Create a bot application under your discord developer portal and copy the TOKEN.
- Create a .env in the root of your bot directory with DISCORD_TOKEN="your-token"
- python3 Main.py
- You can start with !!disbot command in your server (where you have invited this bot)


## How to create a bot application under developer portal?

- [Developer Portal](https://discord.com/developers/applications) -> New Application -> Fill up NAME -> CREATE -> Bot section under menu -> Add Bot -> 'Yes,do it!' -> Copy TOKEN -> Check-in 'PRESENCE INTENT' and 'SERVER MEMBERS INTENT'. (Only if its required!)