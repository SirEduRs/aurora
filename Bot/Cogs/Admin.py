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

from datetime import timedelta
from typing import Any

import disnake
from disnake.ext import commands

from Aurora import AuroraClass
from Utils import ViewerAdmin
from Utils.Utilidades import EmbedDefault as Embed
from Utils.Utilidades import convert_time


class Admin(commands.Cog, name=":tools: Administração"):  # type: ignore
    """docstring for Admin"""
    def __init__(self, bot):
        super(Admin, self).__init__()
        self.bot = bot

    @commands.command(
        name="ban",
        description="Bane um membro por ID | Menção",
        usage="ban <ID | Menção>",
        aliases=["banir"]
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def _ban(
        self,
        ctx: commands.Context[AuroraClass],
        userb: disnake.Member = None,
        *,
        reason: str = ''
    ):
        reason = reason or "Nenhum motivo especificado."
        if userb is not None:
            if userb.id == ctx.author.id:
                return await Embed(ctx, "Você não pode banir a si mesmo.")
            elif userb.id == ctx.guild.owner.id:
                return await Embed(
                    ctx, "Você não pode banir o dono do servidor."
                )
            else:
                await ctx.send(
                    embed=disnake.Embed(
                        colour=0x0101DF,
                        description=
                        f"Você tem certeza que deseja banir o membro {userb.mention} ?"
                    ),
                    view=ViewerAdmin(
                        action="ban",
                        member=userb,
                        reason=reason,
                        guild=ctx.guild,
                        ctx=ctx
                    )
                )
        else:
            return await Embed(ctx, "Você precisa dizer alguém para eu banir.")

    @commands.command(
        name="kick",
        description="Expulsa um membro por ID | Menção",
        usage="kick <ID | Menção>",
        aliases=["expulsar"]
    )
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def _kick(
        self,
        ctx: commands.Context[AuroraClass],
        userk: disnake.Member = None,
        *,
        reason: str = ''
    ):
        reason = reason or "Nenhum motivo especificado."
        if userk is not None:
            if userk == ctx.author.id:
                await Embed(ctx, "Você não pode expulsar a si mesmo.")
            elif userk.id == ctx.guild.owner.id:
                await Embed(
                    ctx, "Você não pode expulsar o dono(a) do servidor."
                )
            else:
                await ctx.send(
                    embed=disnake.Embed(
                        colour=0x0101DF,
                        description=
                        f"Você tem certeza que deseja expulsar o membro {userk.mention} ?"
                    ),
                    view=ViewerAdmin(
                        action="kick",
                        member=userk,
                        reason=reason,
                        guild=ctx.guild,
                        ctx=ctx
                    )
                )
        else:
            await Embed(ctx, "Você precisa dizer alguém para eu expulsar.")

    @commands.command(
        name="unban",
        description="Desbane um membro por ID",
        usage="unban <ID>",
        aliases=["desbanir"]
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def _unban(
        self,
        ctx: commands.Context[AuroraClass],
        useru: disnake.User = None,
        *,
        reason: str = ''
    ):
        reason = reason or "Nenhum motivo especificado."
        if useru is not None:
            await ctx.send(
                embed=disnake.Embed(
                    colour=0x0101DF,
                    description=
                    f"Você tem certeza que deseja desbanir o membro {useru.user.mention} ?"
                ),  # type: ignore
                view=ViewerAdmin(
                    action="unban",
                    member=useru,
                    reason=reason,
                    guild=ctx.guild,
                    ctx=ctx
                )
            )
        else:
            await Embed(ctx, "Você precisa dizer alguém para eu desbanir.")

    @commands.command(
        name="lock",
        description="Bloqueia o canal de texto para os membros.",
        usage="lock [channel]",
        aliases=["bloquear"]
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _lock(
        self,
        ctx: commands.Context[AuroraClass],
        channel: disnake.TextChannel = None
    ):
        channel = channel or ctx.channel
        txt = "Este canal foi bloqueado." if channel == ctx.channel else f"O canal {channel.mention} foi bloqueado."
        everyone_perms = channel.overwrites_for(ctx.guild.default_role)
        everyone_perms.send_messages = False
        everyone_perms.use_slash_commands = False
        await channel.set_permissions(
            ctx.guild.default_role, overwrite=everyone_perms
        )
        await Embed(ctx, txt)

    @commands.command(
        name="unlock",
        description="Desbloqueia o canal de texto para os membros.",
        usage="unlock [channel]",
        aliases=["desbloquear"]
    )
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _unlock(self, ctx, channel: disnake.TextChannel = None):
        channel = channel or ctx.channel
        txt = "Este canal foi desbloqueado." if channel == ctx.channel else f"O canal {channel.mention} foi desbloqueado."
        everyone_perms = channel.overwrites_for(ctx.guild.default_role)
        everyone_perms.send_messages = None
        everyone_perms.use_slash_commands = None
        await channel.set_permissions(
            ctx.guild.default_role, overwrite=everyone_perms
        )
        await Embed(ctx, txt)

    @commands.slash_command()
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.guild_only()
    async def mute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        time: Any = "Máximo",
        reason: str = ''
    ):
        """Mute um membro por um tempo específico.

		Parameters
		----------
		member: Membro do servidor.
		time: Tempo. Exemplo: 30s, 1m, 1h, 1d, 1w, 1M, 1y.
		reason: Motivo do mute.
		"""
        time = time.lower()
        if time == "Máximo":
            time = 2419200
        else:
            timer = convert_time("segundos", time)
            if timer == time:
                return await Embed(inter, "Tempo inválido.")

        if member.id == inter.user.id:  # type: ignore
            return await Embed(
                inter, "Você não pode mutar a si mesmo.", ephemeral=True
            )
        elif member.id == inter.guild.owner.id:  # type: ignore
            return await Embed(
                inter,
                "Você não pode mutar o dono(a) do servidor.",
                ephemeral=True
            )
        elif member.id == inter.me.id:
            return await Embed(inter, "Você não pode me mutar.", ephemeral=True)
        elif member.top_role.position >= inter.me.top_role.position:  # type: ignore
            return await Embed(
                inter,
                "Eu não posso mutar este membro. Ele possui um cargo igual ou maior que o meu.",
                ephemeral=True
            )

        duration = timedelta(seconds=timer)

        if reason is None:
            reason = f"Author: **{inter.user}**. Nenhum motivo especificado."
        else:
            reason = f"Author: **{inter.user}**. Motivo: **{reason}**."

        await member.timeout(duration=duration, reason=reason)
        return await Embed(
            inter,
            f"O membro {member.mention} foi mutado por {time}.",
            ephemeral=True
        )

    @commands.slash_command()  # type: ignore
    @commands.has_guild_permissions(moderate_members=True)
    @commands.bot_has_guild_permissions(moderate_members=True)
    @commands.guild_only()
    async def unmute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reason: str = ''
    ):
        """Desmuta um membro.

		Parameters
		----------
		member: Membro do servidor.
		reason: Motivo do unmute.
		"""
        if member.id == inter.user.id:  # type: ignore
            return await Embed(
                inter, "Você não pode desmutar a si mesmo.", ephemeral=True
            )
        elif member.id == inter.guild.owner.id:  # type: ignore
            return await Embed(
                inter,
                "Você não pode desmutar o dono(a) do servidor.",
                ephemeral=True
            )
        elif member.id == inter.me.id:
            return await Embed(
                inter, "Você não pode desmutar-me.", ephemeral=True
            )
        elif member.top_role.position >= inter.me.top_role.position:  # type: ignore
            return await Embed(
                inter,
                "Eu não posso desmutar este membro. Ele possui um cargo igual ou maior que o meu.",
                ephemeral=True
            )

        if reason is None:
            reason = f"Author: **{inter.user}**. Nenhum motivo especificado."
        else:
            reason = f"Author: **{inter.user}**. Motivo: **{reason}**."

        await member.timeout(duration=None, reason=reason)
        return await Embed(
            inter, f"O membro {member.mention} foi desmutado.", ephemeral=True
        )


def setup(bot: AuroraClass):
    bot.add_cog(Admin(bot))
    print(
        "\033[1;92m[Cog Load]\033[1;94m Admin\033[1;96m carregado com sucesso !"
    )