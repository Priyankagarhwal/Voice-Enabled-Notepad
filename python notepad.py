import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
file = None

def newFile():
    
    global file
    if file is None:
        save_confirmation = messagebox.askyesnocancel("Save Confirmation", "Do you want to save changes before creating a new file?")
        if save_confirmation is True:
            saveFile()
        elif save_confirmation is None:
            return
    root.title("Untitled - Notepad")
    file = None
    textarea.delete(1.0, tk.END)

def openFile():
    global file
    if file is not None:
        save_confirmation = messagebox.askyesnocancel("Save Confirmation", "Do you want to save changes before opening a file?")
        if save_confirmation:
            saveFile()
        elif save_confirmation is None:
            return
    file = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All files", "."), ("Text Documents", "*.txt")])
    if file:
        root.title(f"{file} - Notepad")
        textarea.delete(1.0, tk.END)
        with open(file, "r") as f:
            textarea.insert(1.0, f.read())

def saveFile():
  
    global file
    if file is None:
        file = filedialog.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt",
                                            filetypes=[("All Files", "."), ("Text Documents", "*.txt")])
        if file == "":
            return
    with open(file, "w") as f:
        f.write(textarea.get(1.0, tk.END))
    root.title(f"{file} - Notepad")


def exitApp():
    if file is not None:
        save_confirmation = messagebox.askyesnocancel("Save Confirmation", "Do you want to save changes before exiting?")
        if save_confirmation:
            saveFile()
        elif save_confirmation is None:
            return
    root.destroy()

def cut():
    if textarea.tag_ranges(tk.SEL):  
        textarea.delete(1.0, tk.END)  
    else:
        messagebox.showinfo("Cut", "No text selected.")

def copy():
    if textarea.tag_ranges(tk.SEL):  
        textarea.event_generate("<<Copy>>")  
    else:
        messagebox.showinfo("Copy", "No text selected.")

def paste():
    clipboard_content = root.clipboard_get()
    if clipboard_content:  
        textarea.event_generate("<<Paste>>")  
    else:
        messagebox.showinfo("Paste", "Clipboard is empty.")

def select_all():
    if len(textarea.get("1.0", tk.END)) > 1:  
        textarea.tag_add(tk.SEL, "1.0", tk.END)  
        textarea.mark_set(tk.INSERT, "1.0")  
        textarea.see(tk.INSERT)  
    else:
        messagebox.showinfo("Select All", "No text to select.")

def select_line():
    try:
        current_index = textarea.index(tk.INSERT)
        current_line, _ = current_index.split('.')
        start_index = f"{current_line}.0"
        end_index = f"{current_line}.end"
        textarea.tag_remove(tk.SEL, "1.0", tk.END)
        textarea.tag_add(tk.SEL, start_index, end_index)
    except tk.TclError:
        messagebox.showinfo("Select Line", "Text area is empty.")

def about():
    about_message = (
       
        "This is a simple text editor application built using Tkinter.\n"
        "It allows you to create, open, save, and edit text files.\n"
        "You can also use voice commands for various actions.\n"
        "Enjoy using Notepad!"
    )
    messagebox.showinfo("About Notepad", about_message)

def execute_command(command):
    if 'new' in command:
        newFile()
    elif 'open' in command:
        openFile()
    elif 'save' in command:
        saveFile()
    elif 'exit' in command:
        exitApp()
    elif 'cut' in command:
        cut()
    elif 'copy' in command:
        copy()
    elif 'paste' in command:
        paste()
    elif 'about' in command:
        about()
    elif 'select' in command:
        select_all()
    else:
        textarea.insert(tk.END, command + ' ')


def write():
    print("Start writing...")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='en-in').lower()
                if 'stop writting' in text:
                    print("Voice control stopped")
                    break
                else:
                    textarea.insert(tk.END, text + ' ')
                    textarea.see(tk.END)  # Scroll to the end of the text area
                    root.update_idletasks()  # Update the GUI
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
                
def start_listening():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        while True:
            try:
                audio = recognizer.listen(source)
                query = recognizer.recognize_google(audio, language='en-in').lower()
                print(f"User said: {query}")
                if 'start writing' in query:
                    write()
                elif 'stop listening' in query:
                    print("Voice control stopped")
                    break
                else:
                    execute_command(query)
                # execute_command(query)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Speech Recognition service: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

root = tk.Tk()
root.title("Untitled - Notepad")
root.geometry("644x766")

textarea = tk.Text(root, font="lucida 13")
textarea.pack(fill=tk.BOTH, expand=True)

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newFile)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_command(label="Save", command=saveFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exitApp)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=cut)
editmenu.add_command(label="Copy", command=copy)
editmenu.add_command(label="Paste", command=paste)
editmenu.add_command(label="Select Line", command=select_line)
editmenu.add_command(label="Select All", command=select_all)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About Notepad", command=about)
menubar.add_cascade(label="Help", menu=helpmenu)

voice_menu = tk.Menu(menubar, tearoff=0)
voice_menu.add_command(label="Voice Control", command=start_listening)
menubar.add_cascade(label="Voice", menu=voice_menu)

root.config(menu=menubar)
root.mainloop()