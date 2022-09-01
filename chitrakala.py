
import io
import warnings
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import tkinter
import customtkinter
from PIL import Image, ImageTk
from tkinter import messagebox

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    APP_NAME = "CHITRAKAALA"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aivalue = 0
        self.prompt = None
        self.img = ImageTk.PhotoImage(Image.open("dream.png"))
        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.bind("<Command-q>", self.on_closing)
        # self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=50, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="AI MAGIC",
                                                command=self.ai)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="PROMPT ENG",
                                                command=self.prompteng)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============o

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.label_1 = tkinter.Label(master=self.frame_right, image=self.img)
        self.label_1.grid(row=1, rowspan=1, column=0, columnspan=3, padx=(0, 0), pady=(0, 0))
        self.label_1.image = self.img
        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Type your Dream")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        # self.entry.entry.bind("<Return>", self.prompt_value)
        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="IMAGINE",
                                                width=90,
                                                command=self.imaginei)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

    def ai(self):
        self.prompt = self.entry.get()

        if (self.prompt is None) or (self.prompt == ""):
            messagebox.showerror("Error", "Please Enter a prompt")

        else:
            self.prompt = self.prompt + ", 4k, ray-tracing, highly detailed, trending on artstation, high quality render"
            self.aivalue = 1

    def prompteng(self):
        messagebox.INFO("Coming soon")

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def imaginei(self, event=None):

        if self.aivalue == 0:
            self.prompt = self.entry.get()

        if (self.prompt is None) or self.prompt == "":
            messagebox.showerror("Prompt error", "Sorry we Cannot imagine without your prompt")
        else:

            mykey = 'sk-PI1ZoMBPo9VKtIibsTQC0O82EplLfZEjeX0NQbTxzN1gQnEK'

            stability_api = client.StabilityInference(
                key=mykey,
                verbose=True,
            )

            answers = stability_api.generate(
                prompt=self.prompt

            )
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed."
                            "Please modify the prompt and try again.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img2 = Image.open(io.BytesIO(artifact.binary))
                        img2.save(self.prompt+".jpg")
                        img3 = ImageTk.PhotoImage(Image.open(self.prompt+".jpg"))
                        self.label_1.config(image=img3)
                        self.label_1.image = img3

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
