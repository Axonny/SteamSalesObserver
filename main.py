import telegram_bot


def main():
    telegram_bot.main()
    telegram_bot.bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
