# Messengers for Olymplan project

 * [Requirements](#requirements)
 * [Usage](#usage)

# <a id="requirements"></a> Requirements
You must have python 3 to run whatsapp and vk bots and python 2 to run telegram bot.
you can install requirements using pip:

    $ pip install -r requirements.txt
  
# <a id="usage"></a> Usage
### Telegram bot

Set Telegram API tokens:

    $ export OLYMPLAN_TG_TOKEN=YOUR_TOKEN

Launch bot

    $ python ./telegram/main.py

### VK bot
Set VK API tokens:

    $ export OLYMPLAN_VK_TOKEN=YOUR_TOKEN
    $ export OLYMPLAN_VK_CTOKEN=YOUR_CONFIRMATION_TOKEN

Launch bot:

    $ python ./vk/main.py PORT

Notice that VK API requires bot to run on default port, so you will either have to run it as sudo with PORT = 80 (not recommended) or forward 80 port to desired one.
  
### Whatsapp bot
  It's complicated!
  
  ![](https://pbs.twimg.com/media/DCxyjicV0AAKUDI.jpg)
