import requests
import random
import re
import json
import hashlib

from googletrans import Translator as Translator_google
from translate   import Translator as Translator_microsoft


class PandoraBot():
    """ Clase para interactuar con bots de la pagina https://pandorabots.com
        Está pensada para ser integrada con TelegramBot para realizar pruebas preliminares."""


##    n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros  kukilp-172e9a08f54
    
    def __init__(self, user_id='rnd', bot_name='David', is_male=True, bot_lang='en', translator_api='google', verbose=False):

        botkey='n0M6dW2XZacnOgCWTp0FRYUuMjSfCkJGgobNpgPv9060_72eKnu3Yl-o1v2nFGtSXqfwJBG2Ros~'


        if user_id == 'rnd':
            user_id = random.randint(0, 100000)
            
        user_hash = hashlib.sha1(str(user_id).encode()).hexdigest()[:6]
        

        self.client_name = 'kukilp-17307' + user_hash  # ej "kukilp-172e9a04361" Identificador de usuario
        self.botkey = botkey

        self.bot_original_name = 'Kuki'

        self.verbose = verbose

        self.bot_name = bot_name
        self.bot_lang = bot_lang
        self.sessionid = 'null'

        self.translator_api = translator_api

        if translator_api not in ['google', 'microsoft']:
            raise ValueError('translator_api not in ["google", "microsoft"]')
        
        # url para los bots
        self.url = 'https://miapi.pandorabots.com/talk'


        self.chat_v = []

        # Reemplazos
        self.re_v = [ (self.bot_original_name, self.bot_name),
                      ('english', 'spanish'),
                      ]

        if is_male:
            self.re_v += [('female',  'male'),
                          ('woman',   'man'),
                          ('girl',    'boy')]


        # Inicion session ID
        self.send_post()
        return None

    def clean_xml(self, text='something <img>img_link</img>'):
        text_cleaned = re.sub("<.+>","", text)

##        if text_cleaned != text:
##            print('text_cleaned: ', text)
        return text_cleaned
        

        
    def gen_rnd(self, seed=None, bites=8):
        random.seed(seed)
        hex_str = hex(random.randint(1+int((bites-1)*'ff', 16), int(bites*'ff', 16)))[2:] 
        return hex_str

    def _text_replace(self, text):
        
        text_ = text
        for a, b in self.re_v:
            text_ = re.sub(r'\b' + a + r'\b', '&S' + b, text_, flags=re.IGNORECASE)
            text_ = re.sub(r'\b' + b + r'\b', '&S' + a, text_, flags=re.IGNORECASE)
            
        text_ = text_.replace('&S', '')
        
        return text_


    def translate(self, text, input_lang='en', output_lang='es', second_try=False):
        if second_try:
            if self.translator_api == 'google':
                translator_api = 'microsoft'
                
            elif self.translator_api == 'microsoft':
                translator_api = 'google'
                
            else:
                raise ValueError('Translator Api SecondTry')
        else:
            translator_api = self.translator_api
            
            
        if translator_api == 'google':
            translator = Translator_google()
            tr_obj = translator.translate(text, src=input_lang, dest=output_lang)
            tr_text = tr_obj.text
            
        elif translator_api == 'microsoft':
            translator = Translator_microsoft(to_lang=output_lang, from_lang=input_lang)
            tr_text = translator.translate(text)
            
        else:
            raise ValueError('Translator Api')

        if tr_text == text and not second_try:
            tr_text = self.translate(text, input_lang=input_lang, output_lang=output_lang, second_try=True)

            
        if self.verbose:
            print('TR: "{}" >> "{}"'.format(text, tr_text))
            
        return tr_text


    def send_post(self, text='xintro'):
        r = requests.post(
            self.url,
            data={
                'input':text,
                'sessionid':self.sessionid,
                'channel':'6',
                'botkey':self.botkey,
                'client_name':self.client_name},
            
            headers={'Referer':'https://www.pandorabots.com/mitsuku/'})

        r_d = json.loads( r.content.decode(errors='ignore') )

        self.sessionid = str(r_d['sessionid'])
        resp_v = r_d['responses']

        return resp_v
    

    def get_response(self, q):

        text = q
        
##        text = self._modify_name(text, name_from=self.bot_name, name_to=self.bot_original_name)
        
        if self.bot_lang != 'en':
            text = self.translate(text, input_lang=self.bot_lang, output_lang='en')

        text = self._text_replace(text)
        
        resp_v = self.send_post(text)

        if len(resp_v) > 0 and resp_v[0] != '':
            ret_text = resp_v[0]
            ret_text = self.clean_xml(ret_text)
            
        else:
            ret_text = "I am sorry, I don't have an answer"

            
        ret_text = self._text_replace(ret_text)

        if self.bot_lang != 'en':
            ret_text = self.translate(ret_text, input_lang='en', output_lang=self.bot_lang)

        self.chat_v.append( (q, ret_text) )
        return ret_text

        
    def get_chat(self):
        if self.verbose:
            for a, b in self.chat_v:
                print('you:    ', a)
                print('mitsuko:', b)
                print()
            
        return self.chat_v


    def on_start(self, q=''):
        ret_text = "Starting new chat with {}".format(self.bot_name)
        
        if self.bot_lang != 'en':
            ret_text = self.translate(ret_text, input_lang='en', output_lang=self.bot_lang)
            
        return [ret_text]

    

if __name__ == '__main__':

    mk = PandoraBot(bot_name="David", is_male=True, bot_lang='es', verbose=False)
    for i in range(10):
        text = input(' >>> ')

        print(' - ', mk.get_response(text) )

    



    
    
