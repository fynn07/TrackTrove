import tkinter
import os
from tkinter import filedialog
from app import download_album, download_playlist, download_song

#CONSTANTS
BEIGE = "#efe1d1"
COLOR = BEIGE
FONT = "arial"

#LOGIC
def download_click():
    destination = filedialog.askdirectory(title="Select A Folder")
    download_choice = radio_state.get()
    spotify_link = spotify_link_entry.get()
    if download_choice == 1:
        state_label.config(text="Downloading Album...")
        success = download_album(spotify_link, destination)
        if success == 1:
            state_label.config(text="The album has successfully downloaded.")
            os.startfile(destination)
        elif success == 0:
            state_label.config(text="Invalid Link...")

    elif download_choice == 2:
        success = download_song(spotify_link, destination)
        if success == 1:
            state_label.config(text="The Song has successfully downloaded.")
            os.startfile(destination)
        elif success == 0:
            state_label.config(text="Invalid Link...")

    elif download_choice == 3:
        success = download_playlist(spotify_link, destination)
        if success == 1:
            state_label.config(text="The playlist has successfully downloaded.")
            os.startfile(destination)
        elif success == 0:
            state_label.config(text="Invalid Link...")

#GUI
window = tkinter.Tk()
window.title("TrackTrove - A Spotify Downloader")
window.resizable(False, False)
window.config(padx=50, pady=50, bg=COLOR)

canvas = tkinter.Canvas(width=396, height=150, bg=COLOR, highlightthickness=0)
tracktrove_logo = tkinter.PhotoImage(file='resources/tracktrove logo.png')
canvas.create_image(196, 75, image=tracktrove_logo)
canvas.grid(row=0, column=1)

spotify_link_entry = tkinter.Entry(width=50, font=FONT)
spotify_link_entry.insert(tkinter.END, "Enter Spotify Link")
spotify_link_entry.grid(pady=6, row=1, column=1)

state_label = tkinter.Label(text="Welcome to TrackTrove!", bg=COLOR, font=FONT)
state_label.grid(pady=10, row=2, column=1)

download_button = tkinter.Button(text="Download", font=FONT, command=download_click)
download_button.grid(pady=6, row=3, column=1)

radio_state = tkinter.IntVar()
album_radiobutton = tkinter.Radiobutton(text="Album", value=1, variable=radio_state, bg=COLOR, font=FONT)
song_radiobutton = tkinter.Radiobutton(text="Song", value=2, variable=radio_state, bg=COLOR, font=FONT)
playlist_radiobutton = tkinter.Radiobutton(text="Playlist", value=3, variable=radio_state, bg=COLOR, font=FONT)
album_radiobutton.grid(row=4, column=0)
song_radiobutton.grid(row=4, column=1)
playlist_radiobutton.grid(row=4, column=2)



window.mainloop()