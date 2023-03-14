#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import openai
import telebot

openai.api_key = 'openai_api_key'
bot = telebot.TeleBot('boot_api_key')

@bot.message_handler(func=lambda _: True)
def handle_message(message):
	response = openai.Completion.create(
				model="text-davinci-003",
				prompt=message.text,
				temperature=0.8,
				max_tokens=1024,
				top_p=1,
				frequency_penality=0.5,
				presence_penality=0.0,
	)
	bot.send_message(chat_id=message.from_user.id, text=response["choices"][0]["text"])

def main():
	bot.polling()

if __name__ == '__main__':
	main()
