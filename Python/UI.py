import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x400")  # Made window taller to accommodate more fields

app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

te = customtkinter.CTkFrame(master=app)
te.place(relx=0.1, rely=0.1)



# Create labels and text fields
label1 = customtkinter.CTkLabel(master=te, text="App token:")
label1.grid(row=0, column=0, padx=10, pady=10)

entry1 = customtkinter.CTkEntry(master=te, placeholder_text="Enter text here...")
entry1.grid(row=0, column=1, padx=10, pady=10)


label2 = customtkinter.CTkLabel(master=te, text="UserToken:")
label2.grid(row=1, column=0, padx=10, pady=10)

entry2 = customtkinter.CTkEntry(master=te, placeholder_text="Enter more text...")
entry2.grid(row=1, column=1, padx=10, pady=10)



label3 = customtkinter.CTkLabel(master=te, text="Realm Name:")
label3.grid(row=2, column=0, padx=10, pady=10)

entry3 = customtkinter.CTkEntry(master=te, placeholder_text="NAME.quickbase.com")
entry3.grid(row=2, column=1, padx=10, pady=10)


def button_function():
    # Gather values from all text fields
    value1 = entry1.get()
    value2 = entry2.get()
    value3 = entry3.get()
    
    # Print the values
    print("Text Field 1:", value1)
    print("Text Field 2:", value2)
    print("Text Field 3:", value3)

options = customtkinter.CTkOptionMenu(master=app, values=["API_GetSchema", "API_GetTables"])
options.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Print Values", command=button_function)
button.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)


app.mainloop()