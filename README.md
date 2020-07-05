# Mitsuku (Kuki) Chatbot

This is a Python3 implementation made to interact with the Chatbot Mutsuku or Kuki.

https://pandorabots.com/mitsuku/

The implementation is made to be able to change the name of the bot and to be able to interact with it in any language.

## Installation

Just install dependences:
```sh
$ pip3 install requests
$ pip3 install googletrans
$ pip3 install translate
```
## Usage Example

```python3
# Create an instance
mk = PandoraBot(
    bot_name="David",  # Set the bot name
    is_male=True,      # Set the gender
    bot_lang='es',     # Set the bot language
    verbose=False)
    
# Interact with the Chatbot
resp_text = mk.get_response('Hello')
print(resp_text)
```
