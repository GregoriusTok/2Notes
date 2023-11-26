#!!THIS IS THE POST HACKATHON VERSION!!
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from datetime import date

relfolderpath = "Notes"
current_file_path = str(date.today()) + "-" + relfolderpath + "-"

def update_filebox(folderpath):
  filebox.delete(0, tk.END)
  nfilelist = os.listdir(folderpath)
  for item in nfilelist:
    filebox.insert(tk.END, item)

def save_file():
  global current_file_path

  if ".txt" not in file_bar_entry.get():
    file_bar_entry.insert(tk.END, ".txt")
  current_file_path = relfolderpath + "\\" + file_bar_entry.get()

  if current_file_path:
    def get_format_markers(marker):
        ranges = list(text_entry.tag_ranges(marker))
        return [(text_entry.get(start, end), (start, end)) for start, end in zip(ranges[0::2], ranges[1::2])]

    bolded = get_format_markers("bold")
    italiced = get_format_markers("italic")
    undered = get_format_markers("underline")

    content = text_entry.get("1.0", tk.END)

    for text, (start, end) in bolded:
        content = content.replace(text, f"<^B^>{text}<^B^>", 1)
    for text, (start, end) in italiced:
        content = content.replace(text, f"<^I^>{text}<^I^>", 1)
    for text, (start, end) in undered:
        content = content.replace(text, f"<^U^>{text}<^U^>", 1)

    with open(current_file_path, "w") as file:
        file.write(content)
  
  update_filebox(relfolderpath)
    
def FolderQ():
  global relfolderpath
  global current_file_path
  try:
    lfolderpath = filedialog.askdirectory()
    relfolderpath = os.path.relpath(lfolderpath)
    folderButton.config(text="Folder: " + relfolderpath)
    update_filebox(relfolderpath)
  except ValueError:
    pass

  filename()

def fileselection(event):
  global current_file_path

  selected_file = filebox.get(filebox.curselection()[0])
  current_file_path = os.path.join(relfolderpath, selected_file)
  file_bar_entry.delete("0", tk.END)
  file_bar_entry.insert(tk.END, current_file_path.replace(relfolderpath + "\\", ""))

  with open(relfolderpath + "\\" + filebox.get(filebox.curselection()[0])) as file:
    content = file.read()

    #Remove Bold Mark
    boldsplit = content.split("<^B^>")
    boldsect = boldsplit[1::2]
    content = "".join(boldsplit)

    #Remove Italic Mark
    italicsplit = content.split("<^I^>")
    italicsect = italicsplit[1::2]
    content = "".join(italicsplit)

    #Remove Underline Mark
    undersplit = content.split("<^U^>")
    undersect = undersplit[1::2]
    content = "".join(undersplit)

    text_entry.delete("1.0", tk.END)  # Clear existing text
    text_entry.insert(tk.END, content)
  
  #Check Bolded
  for i in boldsect:
    start_index = text_entry.search(i, "1.0", tk.END)
    if start_index:
        end_index = f"{start_index}+{len(i)}c"
        text_entry.tag_add("bold", start_index, end_index)
  
  #Check Italics
  for i in italicsect:
    start_index = text_entry.search(i, "1.0", tk.END)
    if start_index:
        end_index = f"{start_index}+{len(i)}c"
        text_entry.tag_add("italic", start_index, end_index)
  
  #Check Underline
  for i in undersect:
    start_index = text_entry.search(i, "1.0", tk.END)
    if start_index:
        end_index = f"{start_index}+{len(i)}c"
        text_entry.tag_add("underline", start_index, end_index)

def toggle_bold():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "bold" in text:
      text_entry.tag_remove("bold", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("bold", tk.SEL_FIRST, tk.SEL_LAST)
  except:
    pass

def toggle_italic():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "italic" in text:
      text_entry.tag_remove("italic", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("italic", tk.SEL_FIRST, tk.SEL_LAST)
      
  except:
    pass

def toggle_underline():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "underline" in text:
      text_entry.tag_remove("underline", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("underline", tk.SEL_FIRST, tk.SEL_LAST)
      
  except:
    pass
  
def resize_image(event):
  def delayed_resize():
    new_width = event.width
    new_height = event.height
    resized_image = og_image.resize((new_width, new_height))
    updated_photo = ImageTk.PhotoImage(resized_image)
    background_label.configure(image=updated_photo)
    background_label.image = updated_photo
  window.after(10, delayed_resize)

def filename():
  global current_file_path
  current_file_path = str(date.today()) + "-" + relfolderpath + "-"
  file_bar_entry.delete("0", tk.END)
  file_bar_entry.insert("0", current_file_path)

# Create the main window
window = tk.Tk()
window.title("Two Note")
window.geometry("500x300")

# Load the PNG image
og_image = Image.open("Mondstat.png")
resized_image = og_image.resize((500,300))
photo = ImageTk.PhotoImage(resized_image)

# set background
background_label = tk.Label(window, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create Scrollbar
scrollbar = tk.Scrollbar(window, orient="vertical")
scrollbar.grid(column = 2, row=0, padx=(0,40), sticky="ns", pady=(31,0))

# Create an Entry widget for text input
text_entry = tk.Text(window, wrap="word", height=10, width=40, yscrollcommand=scrollbar.set)
text_entry.tag_configure("bold", font=("Helvetica", 9, "bold"))
text_entry.tag_configure("italic", font=("Helvetica", 9, "italic"))
text_entry.tag_configure("underline", underline=True)
text_entry.grid(column=0, row=0, columnspan=2, pady=(30, 0), padx=(50, 0), sticky="nsew")
scrollbar.config(command=text_entry.yview)

#File name bar
file_bar_label = tk.Button(window, text="File: ", command=filename)
file_bar_label.grid(column=0, row=0, columnspan=1, pady=(5,0), padx=(50,0), sticky="nw")
file_bar_entry = tk.Entry(window, text=current_file_path)
file_bar_entry.insert(tk.END, current_file_path)
file_bar_entry.grid(column=0, row=0, columnspan=2, pady=(10,0), padx=(85,0), sticky="new")

# text formatting tool bar for bold/italics/underline
formatting_toolbar = tk.Frame(window)
formatting_toolbar.grid(column=0, row=1, sticky="nw", padx=(50,0), pady=(0,10))

bold_button = tk.Button(formatting_toolbar, text="B", command=toggle_bold)
bold_button.grid(column=0, row=0, padx=(0,0), pady=(0,0))

italic_button = tk.Button(formatting_toolbar, text="I", command=toggle_italic)
italic_button.grid(column=1, row=0, padx=(0,0), pady=(0,0))

underline_button = tk.Button(formatting_toolbar, text="U", command=toggle_underline)
underline_button.grid(column=2, row=0, padx=(0,0), pady=(0,0))

#Save Buttons
save_button = tk.Button(window, text="Save", command=save_file)
save_button.grid(column=3, row=1, sticky="ne", padx=(0, 0))

#Folder Button
folderButton = tk.Button(window, text="Folder: " + relfolderpath, command=FolderQ)
folderButton.grid(column=3, row=0, sticky="nwe", pady=(10, 0))

#Listbox For Files
filelist = os.listdir(relfolderpath)
filevar = tk.StringVar(value=filelist)
filebox = tk.Listbox(window, listvariable=filevar)
filebox.grid(row=0, column=3, sticky="nes", padx=(0,0), pady=(32,0))
filebox.bind("<Double-1>", fileselection)

#Making things resizable
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=4)
window.columnconfigure(2, weight=0)
window.columnconfigure(3, weight=0)
window.rowconfigure(0, weight=5)
window.rowconfigure(1, weight=1)
# window.rowconfigure(2, weight=1)

# Bind the resize_image function to the window resizing event
window.bind("<Configure>", resize_image)

# Run the Tkinter event loop
window.mainloop()
