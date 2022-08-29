# Sauce bot
#### All in one Music Discord player bot

## Feature
#### Self hosted lavaplayer
No need to connect or tap-in to laggy public lavaplayer server. self hosted and enjoy high quality audio without charge

#### Autoplay command feature *[Youtube v3 api required]
Enjoy infinite listening with autoplay command using the `$auto`

#### Readable ui 
Know what music next or know the queues by simple ui

## Setup
Clone this repository on your local computer or cloud hosting (Free : Heroku, repl.it or Paid : AWS, Azure...)
```
git clone https://github.com/johnyjohny20/sauce.git
```
Install all necessary dependencies by running `pip install -r requirements.txt` on your virtual environments or etc.. Incase the version of lavalink is 3.xx simply reinstall again with
`pip install git+https://github.com/Devoxin/Lavalink.py.git`



Now create a `.env` file using the `.env.example`  example on the repo
For local hosting, simply add any password you want, the type node simply add `default-node` and country e.g `us`

leave other fields `""` if you are not planning to host your private lavaplayer server on Heroku or tapping in public hosted server

Now the most important part, edit the `config.py` located on `settings` folder

If you are hosting with seperate lavaplayer, simply set the `run_withplayer = False` 
If you want host the whole bot with player, simply set the `run_withplayer = True`

To run the app locally set the `service = "local"` (except if you are planning to connect on such public hosted lavaplayer set the `service = "web"`)


