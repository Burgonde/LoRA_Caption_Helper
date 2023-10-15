import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk

# Fonction pour redimensionner l'image
def resize_image(image_path, width):
    image = Image.open(image_path)
    original_width, original_height = image.size
    new_width = width
    new_height = (new_width * original_height) // original_width
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

def select_directory():
    global directory
    directory = filedialog.askdirectory()
    list_files(directory)

def list_files(directory):
    image_listbox.delete(0, tk.END)
    text_listbox.delete(0, tk.END)
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            text_listbox.insert(tk.END, filename)
        elif filename.endswith('.png') or filename.endswith('.jpg'):
            image_listbox.insert(tk.END, filename)

def show_image(event):
    selected_item = image_listbox.get(image_listbox.curselection())
    image_path = os.path.join(directory, selected_item)
    photo = resize_image(image_path, 500)
    image_label.config(image=photo)
    image_label.image = photo
    #text_editor.delete(1.0, tk.END)
    #save_button.config(state=tk.DISABLED)

def show_text(event):
    selected_item = text_listbox.get(text_listbox.curselection())
    with open(os.path.join(directory, selected_item), 'r') as file:
        content = file.read()
        text_editor.delete(1.0, tk.END)
        text_editor.insert(tk.END, content)
    #image_label.config(image='')
    save_button.config(state=tk.NORMAL)

def save_text():
    selected_item = text_listbox.get(text_listbox.curselection())
    if selected_item.endswith('.txt'):
        content = text_editor.get(1.0, tk.END)
        with open(os.path.join(directory, selected_item), 'w') as file:
            file.write(content)

app = tk.Tk()
app.title("Application de Sélection de Fichiers")
app.geometry("800x1000")

directory = ""

select_button = tk.Button(app, text="Sélectionner un Répertoire", command=select_directory)
select_button.pack()

frame = tk.Frame(app)
frame.pack()

image_listbox = tk.Listbox(frame)
image_listbox.pack(side=tk.LEFT)

text_listbox = tk.Listbox(frame)
text_listbox.pack(side=tk.RIGHT)

text_editor = tk.Text(app, wrap=tk.WORD, width=40, height=5)
text_editor.pack()

save_button = tk.Button(app, text="Enregistrer", command=save_text, state=tk.DISABLED)
save_button.pack()

image_label = tk.Label(app)
image_label.pack()

image_listbox.bind("<<ListboxSelect>>", show_image)
text_listbox.bind("<<ListboxSelect>>", show_text)

app.mainloop()
