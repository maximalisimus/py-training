#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import openai
import telebot

openai.api_key = 'openai_api_key'
bot = telebot.TeleBot('boot_api_key')

@bot.message_handler(func=lambda _: True)
def handle_message(message):
	completion = openai.Completion.create(
		engine="text-davinci-003",
		prompt=message.text,
		max_tokens=3096,
		temperature=0.5,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0
	)
	bot.send_message(chat_id=message.from_user.id, text=completion["choices"][0]["text"])

def main():
	bot.polling()

if __name__ == '__main__':
	main()
