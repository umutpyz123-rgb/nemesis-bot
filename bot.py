import os
import sys
import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "nc_logo.jpg")

# --- Ticket Control Views ---
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Ticketı Kapat", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Ticket 5 saniye içinde kapatılıyor...", ephemeral=False)
        await asyncio.sleep(5)
        await interaction.channel.delete()

# --- Panel Views ---
class BuyPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ticket Aç", style=discord.ButtonStyle.danger, emoji="🎟️", custom_id="buy_ticket_btn")
    async def buy_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user
        category = interaction.channel.category

        channel_name = f"satınalım-{user.name}".lower()

        existing = discord.utils.get(guild.text_channels, name=channel_name)
        if existing:
            await interaction.response.send_message(f"Zaten açık bir satın alım ticketınız var: {existing.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason=f"CS2 Internal Satın Alım Ticket'ı: {user.name}"
        )

        embed = discord.Embed(
            title="🛒 CS2 INTERNAL — Satın Alım Ticketı",
            description=f"Merhaba {user.mention},\nSatın alım işlemi için yetkililer kısa süre içinde sizinle iletişime geçecektir.\n\nLütfen almak istediğiniz paket süresini (1 Günlük, 3 Günlük, 1 Haftalık vb.) ve tercih ettiğiniz ödeme yöntemini yazınız.",
            color=discord.Color.from_rgb(130, 20, 40)
        )
        embed.set_footer(text="Nemesis © 2026")
        
        await ticket_channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"Ticket açıldı: {ticket_channel.mention}", ephemeral=True)

    @discord.ui.button(label="Özellikler", style=discord.ButtonStyle.secondary, emoji="📌", custom_id="buy_features_btn")
    async def buy_features(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="⚡ CS2 INTERNAL — Özellikler & Detaylar",
            description=(
                "**Nemesis CS2 Internal Özellik Listesi:**\n\n"
                "• **Aimbot:** Silent Aim, Smooth Control, FOV Selection, Hitbox Selection\n"
                "• **Visuals (ESP):** Box, Skeleton, Health Bar, Weapon ESP, Chams (Visible/Hidden)\n"
                "• **Misc:** Bunnyhop, No Recoil, Rank Revealer, Radar Hack\n"
                "• **Güvenlik:** Undetected & Instant Delivery\n\n"
                "Detaylı bilgi ve satın alım için **Ticket Aç** butonuna basabilirsiniz!"
            ),
            color=discord.Color.from_rgb(130, 20, 40)
        )
        embed.set_footer(text="Nemesis © 2026")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class NormalPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Destek Ticketı Aç", style=discord.ButtonStyle.primary, emoji="🎫", custom_id="normal_ticket_btn")
    async def normal_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        user = interaction.user
        category = interaction.channel.category

        channel_name = f"destek-{user.name}".lower()

        existing = discord.utils.get(guild.text_channels, name=channel_name)
        if existing:
            await interaction.response.send_message(f"Zaten açık bir destek ticketınız var: {existing.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason=f"Genel Destek Ticket'ı: {user.name}"
        )

        embed = discord.Embed(
            title="🎧 Nemesis — Genel Destek & Yardım",
            description=f"Merhaba {user.mention},\nYardım ve sorularınız için destek talebiniz oluşturuldu.\nLütfen yaşadığınız sorunu detaylıca açıklayınız.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Nemesis © 2026")

        await ticket_channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"Destek ticketınız açıldı: {ticket_channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"NemesisBot Aktif! ({bot.user.name} - ID: {bot.user.id})")
    bot.add_view(BuyPanelView())
    bot.add_view(NormalPanelView())
    bot.add_view(CloseTicketView())

    # Clear channels and re-send clean panels
    try:
        ticket_ch = await bot.fetch_channel(1546187709385543690)
        if ticket_ch:
            print("Destek kanalı temizleniyor...")
            await ticket_ch.purge(limit=100)
            embed = discord.Embed(
                title="Nemesis | Genel Destek Merkezi",
                description=(
                    "**DESTEK VE YARDIM KANALI**\n"
                    "Teknik destek, genel sorularınız veya bilgi almak için aşağıdaki butondan ticket açabilirsiniz.\n"
                    "--------------------------------------------------\n\n"
                    "**Çalışma Saatleri:** 7/24 Aktif Destek Ekibi"
                ),
                color=discord.Color.blue()
            )
            embed.set_footer(text="Nemesis © 2026")
            await ticket_ch.send(embed=embed, view=NormalPanelView())
            print("Destek kanalı temizlendi ve panel gönderildi!")
    except Exception as e:
        print(f"Destek kanalı temizleme/gönderme hatası: {e}")

    try:
        buy_ch = await bot.fetch_channel(1545154778340794378)
        if buy_ch:
            print("Satın alım kanalı temizleniyor...")
            await buy_ch.purge(limit=100)
            embed = discord.Embed(
                title="Nemesis | Private",
                description=(
                    "**CS2 INTERNAL**\n"
                    "*Instant delivery · Secure checkout*\n"
                    "--------------------------------------------------\n\n"
                    "**PRICING**\n"
                    "**1 Günlük** — 50 TL\n"
                    "**3 Günlük** — 100 TL\n"
                    "**1 Haftalık** — 250 TL\n"
                    "**1 Hafta ve Üstü** — Ticket üzerinden iletişime geçiniz"
                ),
                color=discord.Color.from_rgb(130, 20, 40)
            )
            embed.set_footer(text="Nemesis © 2026")
            if os.path.exists(IMAGE_PATH):
                file = discord.File(IMAGE_PATH, filename="nc_logo.jpg")
                embed.set_image(url="attachment://nc_logo.jpg")
                await buy_ch.send(embed=embed, file=file, view=BuyPanelView())
            else:
                await buy_ch.send(embed=embed, view=BuyPanelView())
            print("Satın alım kanalı temizlendi ve panel gönderildi!")
    except Exception as e:
        print(f"Satın alım kanalı temizleme/gönderme hatası: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("HATA: .env dosyasında DISCORD_TOKEN bulunamadı!")
        sys.exit(1)
    bot.run(TOKEN)
