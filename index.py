from os import environ
import json
import requests
import random
channel=environ['channel']
class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)
    def callbackquery(self,chat_id,m_id,data):
      f=0
      met='editMessagetext'
      if data=='1':
        f=1
        
       # par=notifying(chat_id,m_id)
      else:
        f=0
        method='kickchatmember'
        para={'chat_id':channel,'user_id':int(data)}
        requests.post(self.api_url+method,para)
        print('succesfully kicked')
      if f==0:
        params={'chat_id': chat_id,'message_id': m_id,'text':'User kicked succesfully.'}
      else:
        params={'chat_id': chat_id,'message_id': m_id,'text':'Approved succesfully.'}
       
      print('hello')
      responses=requests.post(self.api_url + met, params)
      
      return responses
    def restrict(self,first_chat_id,first_user_id):
      method='restrictChatMember'
      key=json.dumps({'ChatPermissions':{'can_send_messages':False ,'can_send_media_messages':False,'can_send_polls':False,'can_send_other_messages':False,'can_invite_users':False}})
      
      para={'chat_id':first_chat_id,'user_id':first_user_id,'permissions':key}
      
      resp=requests.post(self.api_url + method, para)

    def send_notify(self,chat_id,m_id,text,first_user_id):
         '''met='sendchataction'
         para={'chat_id':chat_id ,'action' : 'typing'}
         respons=requests.post(self.api_url + met, para)'''
         
         key={'inline_keyboard':[[{'text': 'Yes','callback_data':first_user_id }],[{'text': 'No','callback_data':'1'}]]}
         keyys=json.dumps(key)
         params = {'chat_id': chat_id, 'text': text,'parse_mode':'HTML','reply_markup':keyys}
         method = 'sendMessage'
         resp = requests.post(self.api_url + method, params)
       

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
  
    def send_message(self, chat_id,m_id,text):
        t_day=d()
        met='sendchataction'
        para={'chat_id':chat_id ,'action' : 'typing'}
        respons=requests.post(self.api_url + met, para)
        params = {'chat_id': chat_id,'reply_to_message_id' : m_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = environ['token']
niloner_bot = BotHandler(token)
ID= [750862502,1694702126,1568399157]
#userid=['']
#username=['']
def main():
    new_offset = 0
    print('Launching the bot...')

    while True:
        
        all_updates=niloner_bot.get_updates(new_offset)
        
        if len(all_updates) > 0:
           for current_update in all_updates:
              print(current_update)
              first_update_id = current_update['update_id']
              if 'callback_query' in current_update :
                  print('call_back')
                  first_update_id = current_update['update_id']
                  if 'data' in current_update['callback_query']:
                    data_r=current_update['callback_query']['data']
                  m_id=current_update['callback_query']['message']['message_id']
                  chat_id=current_update['callback_query']['message']['chat']['id']
                  
                  
                  niloner_bot.callbackquery(chat_id,m_id,data_r)
                  new_offset=first_update_id+1
                  print(data_r,chat_id,m_id)
              elif 'message' in current_update :
                m_id = current_update['message']['message_id']
        
                if 'text' not in current_update['message'] :
                    first_chat_text='New member'
                    #new_offset=first_update_id+1
                else:
                  first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                    user_id=current_update['message']['from']['id']
                    print(user_id)
                else:
                    first_chat_name = "unknown"
                    
                if 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['first_name']
                   # first_chat_username=current_update['message']['chat']['username']
                    first_user_id=current_update['message']['new_chat_member']['id']
                   # niloner_bot.restrict('@'+first_chat_username,first_user_id)
                    niloner_bot.send_notify(ID[0],m_id,'Do you want to kick '+first_chat_name+ '?',first_user_id)
                    
                    niloner_bot.send_notify(1694702126,m_id,'Do you want to kick '+first_chat_name+ '?',first_user_id)
                    
                    niloner_bot.send_notify(1568399157,m_id,'Do you want to kick '+first_chat_name+ '?',first_user_id)
               
                    new_offset = first_update_id + 1
         
                if first_chat_text=='/start':
                  #niloner_bot.administrator('@'+first_chat_username)
                  new_offset = first_update_id + 1
                else:
                  new_offset = first_update_id + 1
                  
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
