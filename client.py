import socket # use for client server interaction
import threading # use for running multiple tasks at one time (multiple clietns)
import tkinter as tk # GUI
from tkinter import scrolledtext, simpledialog, messagebox #More gui sheet
from deep_translator import GoogleTranslator #use for translation

#function to translate text into target lang from source lang
def translate_text(text, target_lang):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)

# Client details
HOST = '3.136.97.57'
PORT = 5000        

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application with Translation")

        #Ask for username from user base
        self.username = simpledialog.askstring("Username", "Please enter a username", parent=self.master)
        if not self.username:
            messagebox.showerror("Username Error", "Username cannot be empty.")
            master.destroy()
            return

        #GUI Components
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state='disabled')

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.pack(padx=20, pady=5)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=20, pady=5)

        #Language selection
        self.lang_label = tk.Label(master, text="Your Language (e.g., en, es, fr):")
        self.lang_label.pack(pady=5)

        self.lang_entry = tk.Entry(master)
        self.lang_entry.pack(pady=5)
        self.lang_entry.insert(0, 'en') # default to ingles

        #Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((HOST, PORT))
        except Exception as e: # error handling
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
            master.destroy()
            return

        # Start the thread to receive messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    #method to decode received socket and translate into curr language / display text
    #receiving methods from the server
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    translated_text = translate_text(message, self.lang_entry.get())
                    self.display_message(f"{message} -> {translated_text}") # translate text
            except:
                self.client_socket.close()
                break
    # method to send messages to server encoding in utf8
    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message:
            try:
                #Translate to English before sending
                translated = translate_text(message, 'en')
                send_text = f"{self.username}: {translated}"

                #Display the message immediately in the client's chat area (original user sending)
                self.display_message(f"{self.username}: {message}")

                #Send the message to the server
                self.client_socket.send(send_text.encode('utf-8'))
                self.msg_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Send Error", f"Unable to send message: {e}")
                self.client_socket.close()
                self.master.destroy()
    #method to display chat in the chatbox
    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

#Run the client application
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
