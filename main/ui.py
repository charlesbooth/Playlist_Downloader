import tkinter as tk
from tkinter import filedialog
from downloader import download_media

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_var.set(directory)

def start_download():
    link = link_entry.get().strip()
    file_format = file_format_var.get()
    save_path = directory_var.get()
    if not link:
        status_var.set("Error: Please enter a valid YouTube link")
        return
    if not file_format:
        status_var.set("Error: Please select a file format")
        return
    if not save_path:
        status_var.set("Error: Please select a download directory")
        return
    status_var.set("Download started")
    download_media(link, save_path, file_format)
    status_var.set("Done!")

root = tk.Tk()
root.title("YouTube Downloader")

link_label = tk.Label(root, text="YouTube Link:")
link_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

link_entry = tk.Entry(root)
link_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")

file_format_label = tk.Label(root, text="File Format:")
file_format_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

file_format_var = tk.StringVar()
file_format_mp4 = tk.Radiobutton(root, text=".mp4", variable=file_format_var, value="mp4")
file_format_mp4.grid(row=1, column=1, padx=5, pady=5, sticky="w")
file_format_mp3 = tk.Radiobutton(root, text=".mp3", variable=file_format_var, value="mp3")
file_format_mp3.grid(row=1, column=1, padx=5, pady=5, sticky="e")

directory_label = tk.Label(root, text="Download Directory:")
directory_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

directory_var = tk.StringVar()
directory_entry = tk.Entry(root, textvariable=directory_var)
directory_entry.grid(row=2, column=1, padx=5, pady=5, sticky="we")

directory_button = tk.Button(root, text="Select Directory", command=select_directory)
directory_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=3, column=1, padx=5, pady=5, sticky="we")

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var)
status_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="we")

root.mainloop()
