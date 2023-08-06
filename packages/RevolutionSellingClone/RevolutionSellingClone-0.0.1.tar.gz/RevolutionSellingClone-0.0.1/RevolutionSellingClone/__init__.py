class new_bot(Client):
    def __init__(self, client: Client):
        self.client = client
        @client.on_message(filters.private & filters.command('start'))
        async def start(client, message):
            await message.reply_text("ciao", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("test", callback_data = "test")]]))
        @client.on_message(filters.private & filters.command('aa'))
        async def aa(client, message):
            await message.reply_text("ciao")
        @client.on_callback_query()
        async def callback(client, query):
            if query.data == "test":
                await query.message.edit("test")
    def start(self):
        self.client.run()