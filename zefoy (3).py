import os
import discord
from discord.ext import commands
from os import system
from colorama import init, Fore
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import chromedriver_autoinstaller

# Spécifiez le chemin local de l'exécutable chromedriver
local_chromedriver_path = "/home/container/chromedriver-win64/chromedriver"

if not os.path.isfile(local_chromedriver_path):
    # Si le fichier chromedriver n'est pas un fichier régulier
    print(f"Chromedriver not found at {local_chromedriver_path}")
else:
    try:
        print("Trying to initialize Chrome...")
        uc.Chrome(executable_path=local_chromedriver_path)
        print("Chrome initialized successfully.")
    except Exception as e:
        print(f"Error initializing Chrome: {e}")
        exit()

init(autoreset=True)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ... (le reste du code reste inchangé)

if __name__ == "__main__":
    bot.run("YOUR_BOT_TOKEN")



class TikTokBot:
    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        self.printBanner()

        print(Fore.YELLOW + "[~] Loading driver, please wait...")

        try:
            self.driver = uc.Chrome()
        except:
            print(Fore.RED + "[!] No internet connection")
            exit()

        print(Fore.GREEN + "[+] Driver loaded successfully")
        print()

        self.url = "https://zefoy.com"
        self.captcha_xpath = "/html/body/div[5]/div[2]/form/div/div/div/div/button"
        self.services = {
            "followers": {
                "title": "Followers",
                "xpath": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
                "status": None,
            },
            "hearts": {
                "title": "Hearts",
                "xpath": "/html/body/div[6]/div/div/2/div/div/div[3]/div/button",
                "status": None,
            },
            "comment_hearts": {
                "title": "Comment Hearts",
                "xpath": "/html/body/div[6]/div/div/2/div/div/div[4]/div/button",
                "status": None,
            },
            "views": {
                "title": "Views",
                "xpath": "/html/body/div[6]/div/div/2/div/div/div[5]/div/button",
                "status": None,
            },
            "shares": {
                "title": "Shares",
                "xpath": "/html/body/div[6]/div/div/2/div/div/div[6]/div/button",
                "status": None,
            },
            "favorites": {
                "title": "Favorites",
                "xpath": "/html/body/div[6]/div/div/2/div/div/div[7]/div/button",
                "status": None,
            },
        }

    async def start(self):
        await self.bot_instance.send("Bot is starting...")
        await self.bot_instance.send("Please complete the captcha")

        self.driver.get(self.url)

        self.wait_for_xpath(self.captcha_xpath)
        print(Fore.GREEN + "[+] Captcha completed successfully")
        print()

        self.driver.minimize_window()

        self.check_services()
        for index, service in enumerate(self.services):
            title = self.services[service]["title"]
            status = self.services[service]["status"]

            print(Fore.BLUE + f"[{str(index + 1)}] {title}".ljust(20), status)

        while True:
            try:
                choice = int(await self.bot_instance.send(Fore.YELLOW + "[-] Choose an option : "))
            except ValueError:
                pass

            if choice in [1, 2, 3, 4, 5, 6]:
                break

        if choice == 1:  # followers
            div = 7
            self.driver.find_element(
                By.XPATH, self.services["followers"]["xpath"]
            ).click()
        elif choice == 2:  # hearts
            div = 8
            self.driver.find_element(By.XPATH, self.services["hearts"]["xpath"]).click()
        elif choice == 3:  # comment hearts
            # div = 9
            # self.driver.find_element(
            #     "xpath", self.services["comment_hearts"]["xpath"]
            # ).click()
            print()
            print(Fore.RED + "[!] Comment heart option is not yet available")
            exit()
        elif choice == 4:  # views
            div = 10
            self.driver.find_element(By.XPATH, self.services["views"]["xpath"]).click()
        elif choice == 5:  # shares
            div = 11
            self.driver.find_element(By.XPATH, self.services["shares"]["xpath"]).click()
        elif choice == 6:  # favorites
            div = 12
            self.driver.find_element(
                By.XPATH, self.services["favorites"]["xpath"]
            ).click()
        else:
            exit()

        print()
        video_url = input(Fore.MAGENTA + "[-] Video URL : ")
        print()

        await self.generate_followers(video_url)  # Appel de la nouvelle fonction

    async def start_service(self, div, video_url):
        url_input_xpath = f"/html/body/div[{div}]/div/form/div/input"
        search_btn_xpath = f"/html/body/div[{div}]/div/form/div/div/button"

        input = self.driver.find_element(By.XPATH, url_input_xpath)
        input.clear()
        input.send_keys(video_url)

        self.driver.find_element(By.XPATH, search_btn_xpath).click()

        sleep(3)
        sleep_duration, can_proceed = self.check_submit(div)

        if not can_proceed:
            print(Fore.YELLOW + f"[~] Sleeping for {sleep_duration} seconds")
            sleep(sleep_duration)
            self.driver.find_element(By.XPATH, search_btn_xpath).click()

        send_btn_xpath = f"/html/body/div[{div}]/div/div/div[1]/div/form/button"
        self.wait_for_xpath(send_btn_xpath)
        self.driver.find_element(By.XPATH, send_btn_xpath).click()

        success_message_xpath = f"/html/body/div[{div}]/div/div/span[2]"
        self.wait_for_xpath(success_message_xpath)
        print(Fore.GREEN + "[+] Sent successfully")
        await self.start_service(div, video_url)

    def check_submit(self, div):
        remaining_time_xpath = f"/html/body/div[{div}]/div/div/span[1]"

        try:
            element = self.driver.find_element(By.XPATH, remaining_time_xpath)

            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration = int(minutes) * 60 + int(seconds) + 5

            return sleep_duration, False
        except:
            return None, True

    def check_services(self):
        for service in self.services:
            xpath = self.services[service]["xpath"]
            element = self.driver.find_element(By.XPATH, xpath)

            if element.is_enabled():
                self.services[service]["status"] = Fore.GREEN + "[WORKING]"
            else:
                self.services[service]["status"] = Fore.RED + "[OFFLINE]"

    def wait_for_xpath(self, xpath):
        while True:
            try:
                _ = self.driver.find_element(By.XPATH, xpath)
                return True
            except NoSuchElementException:
                pass

    async def generate_followers(self, video_url):
        followers_generation_url = "URL_DE_GENERATION_DES_FOLLOWERS"  # Remplacez par l'URL réelle
        await self.bot_instance.send(f"Generating followers for video: {video_url}")
        
        response = requests.post(followers_generation_url, data={"video_url": video_url})

        if response.status_code == 200:
            print(Fore.GREEN + "[+] Followers generated successfully")
        else:
            print(Fore.RED + f"[!] Failed to generate followers. Status code: {response.status_code}")

        # Continue with the rest of your logic, such as interacting with the generated followers
        # ...

    def printBanner(self):
        print(
            """
████████╗██╗██╗░░██╗████████╗░████╗░██╗░  ██████╗░░█████╗░████████╗
╚══██╔══╝██║██║░██╔╝╚══██╔══╝██╔══██╗██║░██╔╝  ██╔══██╗██╔══██╗╚══██╔══╝
░░░██║░░░██║█████═╝░░░░██║░░░██║░░██║█████═╝░  ██████╦╝██║░░██║░░░██║░░░
░░░██║░░░██║██╔═██╗░░░░██║░░░██║░░██║██╔═██╗░  ██╔══██╗██║░░██║░░░██║░░░
░░░██║░░░██║██║░╚██╗░░░██║░░░╚█████╔╝██║░╚██╗  ██████╦╝╚█████╔╝░░░██║░░░
░░░╚═╝░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝  ╚═════╝░░╚════╝░░░░╚═╝░░░

Made by : Simon Farah
Github  : https://github.com/simonfarah/tiktok-bot

------------------------------------------------------------------------
"""
        )

@bot.event
async def on_ready():
    system("cls || clear")
    TikTokBot(bot)
    await bot.change_presence(activity=discord.Game(name="!start"))
    print(Fore.GREEN + f"[+] Bot is ready as {bot.user.name}")

if __name__ == "__main__":
    bot.run("YOUR_BOT_TOKEN")