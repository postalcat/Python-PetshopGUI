import ttkbootstrap as ttk
import tkinter as tk
import pandas as pd
import os.path
import csv

#constants to easily manipulate the colors and else
BASE_COST = 75

BACKGROUND_COLOR = "#CF9FFF"
BACKGROUND_COLOR2 = "white"
HEADING_TEXT_COLOR = "white"
TEXT_COLOR = "#FF00FF"

HEADING_FONT = ("Arial", 40, "bold")
SUBHEADING_FONT = ("Helvetica", 20, "bold")
TEXT_FONT = ("Helvetica", 15,"bold")
CSV_FILE = "PetshopGUI/Petshop.csv"


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dog Grooming GUI")
        self.geometry("900x350")
        self.resizable(False, False)
        self.style1 = ttk.Style()
        self.style1.configure("Header.TLabel",
                                foreground=HEADING_TEXT_COLOR,
                                background=BACKGROUND_COLOR,
                                font=HEADING_FONT)
        self.style2 = ttk.Style()
        self.style2.configure("SHeader.TLabel",
                                foreground = HEADING_TEXT_COLOR,
                                background = BACKGROUND_COLOR,
                                font=SUBHEADING_FONT)
        self.style2.configure("TLabel",
                                font = TEXT_FONT,
                                foreground=TEXT_COLOR,
                                background=BACKGROUND_COLOR)
        self.buttonstyle = ttk.Style()
        self.checkboxstyle = ttk.Style()
        self.checkboxstyle.configure("TCheckbutton",
                                        foreground=TEXT_COLOR,
                                        background=BACKGROUND_COLOR,
                                        font=TEXT_FONT)
        self.buttonstyle.configure("TButton",
                                    foreground=HEADING_TEXT_COLOR,
                                    background=TEXT_COLOR,
                                    font=TEXT_FONT)
        self.costs ={"Toe clipping":10,
            "Hair colouring":20,
            "Relaxation massage":5,
            "Teeth cleaning":15,
            "Competition prep":25
            }
        self.userpaid = tk.StringVar()
    def widget_setup(self):
        """
        sets up the widgets and functionality for the app - also holds most functions like submit
        """
        frame1 = ttk.LabelFrame(self).grid(column=0, 
                                            row=0, columnspan=2)
        frame2 = ttk.LabelFrame(self).grid(column=0, 
                                            row=1)
        frame3 = ttk.LabelFrame(self).grid(column=1, 
                                            row=1)
        frame4 = ttk.LabelFrame(self).grid(column=0, 
                                            row=2, 
                                            columnspan=2)
        ttk.Label(frame1, 
                    text="Furry Friends on Wheels", 
                    style="Header.TLabel").grid(column=0, row=0, columnspan=6)
        # Set up frame 2 (client/animal details)
        client_label = ttk.Label(frame2, 
                                    text="Client", style="SHeader.TLabel")
        client_label.grid(column=0, row=1)
        client_name_label = ttk.Label(frame2, 
                                        text="Name:")
        client_name_label.grid(column=0, row=2)
        clientname = ttk.Entry(frame2)
        clientname.grid(column=1, row=2)
        address_label = ttk.Label(frame2, 
                                    text="Address:")
        address_label.grid(column=0, row=3)
        clientadress = ttk.Entry(frame2)
        clientadress.grid(column=1, row=3)
        phone_label = ttk.Label(frame2, 
                                    text="Phone:")
        phone_label.grid(column=0, row=4)
        clientphone = ttk.Entry(frame2)
        clientphone.grid(column=1, row=4)
        animal_label = ttk.Label(frame2, 
                                    text="Animal", 
                                    style="SHeader.TLabel")
        animal_label.grid(column=0, row=5)
        animal_name_label = ttk.Label(frame2, 
                                        text="Name:")
        animal_name_label.grid(column=0, row=6)
        animalname = ttk.Entry(frame2)
        animalname.grid(column=1, row=6)
        breed_label = ttk.Label(frame2, 
                                text="Breed:")
        breed_label.grid(column=0, row=7)
        animalbreed = ttk.Entry(frame2)
        animalbreed.grid(column=1, row=7)
        payment_label = ttk.Label(frame3, 
                                    text="Payment", 
                                    style="SHeader.TLabel")
        payment_label.grid(column=3, row=1)
        additionals_label = ttk.Label(frame3, 
                                        text="Additionals", 
                                        style="SHeader.TLabel")
        additionals_label.grid(column=6, row=1)
        checkboxes = []
        checkbox_vars = []
        cost_var = tk.StringVar()
        cost_var.set("Total Cost: $0")  # Initial value of total cost
        def add_additional():
            """
            this is called when the user wants to make a custom label.
            
            params:

            Takes procedure_name (entry further down)- input by the user
            Takes procedure_cost (spinbox)
            Adds a label+checkbutton 2 rows underneath the lowest value in the additionals
            
            updates the self.costs dict custom value to the user specified cost
            then runs update_total_cost() to 
            """

            additional_name = procedure_name.get()
            additional_cost = int(procedure_cost.get())
            ttk.Label(frame3, 
                        text=f"{additional_name}: {additional_cost}$").grid(column=6, row=len(self.costs) + 2)
            checkbox_var = tk.BooleanVar()
            checkbox_var.trace("w", update_total_cost)
            checkbox = ttk.Checkbutton(frame3, 
                                        variable=checkbox_var, 
                                        command=update_total_cost)
            checkbox.grid(column=7, row=len(self.costs) + 2)
            checkboxes.append(checkbox)
            checkbox_vars.append(checkbox_var)
            procedure_name.delete(0, tk.END)
            procedure_cost.delete(0, tk.END)
            self.costs[additional_name] = additional_cost


        def update_total_cost(*args):#*args : means any amount of parameters can be passed(because if limited then we cannot count
            # the custom procedures when they are selected.)
            """
            This function serves to update the total cost displayed - a sum of the user's choosing.
            params: *args -> means any number of arguments can be passed(similar to import *... its nondescriptive allowance)
            """
            total_cost = max(BASE_COST, 75)  # cost will always be at least 75.
            for checkbox_var, (_, cost) in zip(checkbox_vars, self.costs.items()):
                if checkbox_var.get():
                    total_cost += cost
            custom_cost = procedure_cost.get()
            if custom_cost:
                total_cost += int(custom_cost)
            cost_var.set(f"Total Cost: ${total_cost}")


#placing the contents of the additions list alongside the add custom area.
        
        for i, (key, value) in enumerate(self.costs.items()):
            ttk.Label(frame3, text=f"{key}: {value}$").grid(column=6, row=2 + i)
            checkbox_var = tk.BooleanVar()
            checkbox_vars.append(checkbox_var)
            checkbox = ttk.Checkbutton(frame3, 
                                        variable=checkbox_var, 
                                        command=update_total_cost)
            checkbox.grid(column=7, row=2 + i)
            checkboxes.append(checkbox)
        ttk.Label(frame3, text="Custom Additional:", 
                    style = "SHeader.TLabel",font=("Times", 20)).grid(column=3, row=3, columnspan=3)
        procedure_name = ttk.Entry(frame3, width=10)
        procedure_name.grid(column=4, row=4)
        ttk.Label(frame3, text="Procedure:").grid(column=3, row=4)
        ttk.Label(frame3, text="Cost($):").grid(column=3, row=5)
        procedure_cost = ttk.Spinbox(frame3, from_=0, to=1000, width=3)
        procedure_cost.grid(column=4, row=5)
        ttk.Button(frame3, text="Add", command=add_additional).grid(column=4, row=6)

# setting up the final widgets: cost, paid and submit checkboxes
        ttk.Checkbutton(frame4, text="Client Paid?",
                        variable = self.userpaid).grid(column=5,row=10)
        total_cost_label = ttk.Label(frame4, 
                                    textvariable=cost_var, 
                                    style="SHeader.TLabel")
        total_cost_label.grid(column=4, row=20)
        submit = ttk.Button(frame4, 
                            text="Submit",command=lambda:submit())
        submit.grid(column=5, row=20)
        ttk.Label(text = "Date Booked:").grid(column=0, row=20)
        calendar = ttk.DateEntry(frame4)
        calendar.grid(column=1, row=20)
        update_total_cost()

        def submit():
            """
            submits the user inputs to a CSV file.
            """
            # Get user inputs
            client_name_input = clientname.get()
            address_input = clientadress.get()
            phone_number_input = clientphone.get()
            animal_name_input = animalname.get()
            breed_input = animalbreed.get()
            additional_values = []
            date = calendar.entry.get()
            for checkbox_var, (key, _) in zip(checkbox_vars, self.costs.items()):
                if checkbox_var.get():
                    additional_values.append(key)
            client_paid = True if self.userpaid.get() == "1" else False
            total_cost = cost_var.get()
            # creating a dataframe to export- using all the data we have gathered so far through the widgets.
            userdata = {
                "Client Name": str(client_name_input),
                "Address": str(address_input),
                "Phone Number": str(phone_number_input),
                "Animal Name": str(animal_name_input),
                "Breed": str(breed_input),
                "Additional Values": str(additional_values),
                "Client Paid": str(client_paid),
                "Total Cost": str(total_cost),
                "Date Booked": str(date)
            }
            print(userdata)

            # Using pandas to_csv to export data
            df = pd.DataFrame([userdata])  # Wrap userdata in a list to create a single row DataFrame
            file_exists = os.path.isfile(CSV_FILE)
            df.to_csv(CSV_FILE, index=False, mode='a', header=not file_exists)




if __name__ == "__main__":
    appinstance = GUI()
    appinstance.configure(bg=BACKGROUND_COLOR)
    appinstance.widget_setup()
    appinstance.mainloop()
