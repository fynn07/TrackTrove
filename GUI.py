import tkinter as tk
from tkinter import filedialog, ttk
import os
from app import download_album, download_playlist, download_song

# CONSTANTS
BEIGE = "#efe1d1"
COLOR = BEIGE
FONT = ("Arial", 12)

# LOGIC
def download_click():
    destination = filedialog.askdirectory(title="Select A Folder")
    download_choice = radio_state.get()
    spotify_link = spotify_link_entry.get()
    
    if destination:
        progress_bar.start()
        if download_choice == 1:
            state_label.config(text="Downloading Album...", fg="black")
            success = download_album(spotify_link, destination)
        elif download_choice == 2:
            state_label.config(text="Downloading Song...", fg="black")
            success = download_song(spotify_link, destination)
        elif download_choice == 3:
            state_label.config(text="Downloading Playlist...", fg="black")
            success = download_playlist(spotify_link, destination)
        
        progress_bar.stop()
        if success == 1:
            state_label.config(text="Download successful!", fg="green")
            os.startfile(destination)
        elif success == 0:
            state_label.config(text="Invalid Link...", fg="red")
    else:
        state_label.config(text="No destination selected.", fg="red")

# Placeholder functionality for Entry widget
def on_entry_click(event):
    if spotify_link_entry.get() == 'Enter Spotify Link':
        spotify_link_entry.delete(0, "end")
        spotify_link_entry.insert(0, '')
        spotify_link_entry.config(fg='black')

def on_focusout(event):
    if spotify_link_entry.get() == '':
        spotify_link_entry.insert(0, 'Enter Spotify Link')
        spotify_link_entry.config(fg='grey')

# GUI
window = tk.Tk()
window.title("TrackTrove - A Spotify Downloader")
window.resizable(False, False)
window.config(padx=50, pady=50, bg=COLOR)

canvas = tk.Canvas(width=396, height=150, bg=COLOR, highlightthickness=0)
tracktrove_logo = tk.PhotoImage(file='resources/tracktrove logo.png')
canvas.create_image(198, 75, image=tracktrove_logo)
canvas.grid(row=0, column=1)

spotify_link_entry = tk.Entry(window, width=50, font=FONT, fg='grey')
spotify_link_entry.insert(0, 'Enter Spotify Link')
spotify_link_entry.bind('<FocusIn>', on_entry_click)
spotify_link_entry.bind('<FocusOut>', on_focusout)
spotify_link_entry.grid(pady=6, row=1, column=1)

state_label = tk.Label(text="Welcome to TrackTrove!", bg=COLOR, font=FONT)
state_label.grid(pady=10, row=2, column=1)

download_button = tk.Button(text="Download", font=FONT, command=download_click, bg="lightblue")
download_button.grid(pady=6, row=3, column=1)

radio_state = tk.IntVar()
radio_frame = tk.Frame(window, bg=COLOR)
radio_frame.grid(row=4, column=1, pady=6)

album_radiobutton = tk.Radiobutton(radio_frame, text="Album", value=1, variable=radio_state, bg=COLOR, font=FONT)
album_radiobutton.grid(row=0, column=0)
song_radiobutton = tk.Radiobutton(radio_frame, text="Song", value=2, variable=radio_state, bg=COLOR, font=FONT)
song_radiobutton.grid(row=0, column=1)
playlist_radiobutton = tk.Radiobutton(radio_frame, text="Playlist", value=3, variable=radio_state, bg=COLOR, font=FONT)
playlist_radiobutton.grid(row=0, column=2)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="indeterminate")
progress_bar.grid(row=5, column=1, pady=10)

window.mainloop()
