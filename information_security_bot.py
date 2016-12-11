# import sys
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

from person_info_retriever import PersonInfoRetriever

# Logging
import logging

logging.basicConfig(filename='log.log', filemode='a',
                    format='%(asctime)s %(message)s', datefmt='%H:%M:%S',
                    level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


class InformationSecurityBot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(InformationSecurityBot, self).__init__(*args, **kwargs)
        self.person_info_retriever = PersonInfoRetriever()

        with open('message_templates/start_message.txt') as fin:
            self.start_message = fin.read()

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            text = msg['text']
            logging.info('Chat id: {} | Message: {}'.format(chat_id, text))

            if text == '/start start' or text == '/start':
                self.sender.sendMessage(self.start_message)
            else:
                answer = self.person_info_retriever.get_person_info_by_full_name(text)
                self.sender.sendMessage(answer)


if __name__ == '__main__':
    with open('.information_security_bot_token') as fin:
        token = fin.read().strip()

    bot = telepot.DelegatorBot(token, [
        pave_event_space()(
            per_chat_id(), create_open, InformationSecurityBot, timeout=86400),
    ])

    bot.message_loop(run_forever='Listening ...')
