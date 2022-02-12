"""
MIT License

Copyright (c) 2022 Eduardo Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from disnake.ext import commands

from Aurora import AuroraClass


class On_Command_Complete(commands.Cog):
    def __init__(self, bot: AuroraClass):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        commandsbot = await self.bot.fdb.get_document("bot", "commands")
        commandsbot["number"] += 1
        await self.bot.fdb.set_data("bot", "commands", commandsbot)


def setup(bot: AuroraClass):
    bot.add_cog(On_Command_Complete(bot))
    print(
        "\033[1;95m[Events Load]\033[1;94m On Command Complete\033[1;96m carregado com sucesso !"
    )