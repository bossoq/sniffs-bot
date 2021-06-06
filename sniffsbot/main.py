from bot_init import bot_init, client_init
from player_db_function import player_db_function


bot, nick, channel = bot_init()
client = client_init()
db_fn = player_db_function()


@bot.event
async def event_ready():
    print(f'Ready | {nick} | {channel}')


@bot.event
async def event_message(ctx):
    print(f'[{ctx.timestamp}] {ctx.author.name}: {ctx.content}')
    # print(f'Mod: {ctx.author.is_mod} | Sub: {ctx.author.is_subscriber}')
    await bot.handle_commands(ctx)


async def get_chatters():
    chatters = await client.get_chatters(channel)
    return chatters.all


@bot.event
async def event_raw_data(data):
    print(data)


@bot.event
async def event_usernotice_subscription(metadata):
    print(metadata)


@bot.event
async def event_userstate(user):
    print(user)


# @bot.command(name='test')
# async def test(ctx):
#     if ctx.author.name.lower() == 'bossoq':
#         await ctx.send(f'Hello {ctx.author.name}!')


@bot.command(name='payday')
async def payday(ctx):
    if ctx.author.name.lower() == channel or ctx.author.name.lower() == 'bosssoq':  # only allow admin to execute
        argument = ctx.content.split()
        try:
            coin = int(argument[1])
        except:
            coin = 1
        user_list = await get_chatters()
        await db_fn.player_payday(user_list, coin)
        await ctx.send(f'ผู้ชมทั้งหมด {len(user_list)} คน ได้รับ {coin} sniffscoin')


@bot.command(name='coin')
async def coin(ctx):
    # if ctx.author.is_subscriber == 1 or ctx.author.is_mod or ctx.author.name.lower() == channel:  # only allow sub, mod, admin now
        user_stat = db_fn.check_cur_userstat(ctx.author.name.lower())
        if user_stat:
            name, coin = user_stat['username'], user_stat['coin']
            print(f'User: {name} | Coin: {coin}')
            await ctx.send(f'{ctx.author.name.lower()} มี {coin} sniffscoin')
        else:
            print(f'User: {ctx.author.name.lower()} | Coin: 0')
            await ctx.send(f'{ctx.author.name.lower()} มี 0 sniffscoin')


if __name__ == "__main__":
    bot.run()
