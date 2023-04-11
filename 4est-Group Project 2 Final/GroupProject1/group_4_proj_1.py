'''Create a UI for an employee database'''
import csv
import tkinter as tk
from tkinter import messagebox
import random

def main():
    '''Main loop'''
    list_of_csv = []

    # Open a csv file with read mode
    try:
        with open('survey.csv','r',encoding='ascii') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Store the csv file into a list of lists
            list_of_csv = list(csv_reader)
    #In case the file is not found, initialize an empty list
    except FileNotFoundError:
        list_of_csv = []

    # Initialize tkinter
    root = tk.Tk()
    root.title("Employee Database")

    # Create a frame for the UI elements
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    # Create a label for the menu
    menu_label = tk.Label(frame, text="Please choose one service below:")
    menu_label.grid(row=0, column=0, columnspan=2)

    # Define the function for searching the database
    def search_csv():
        '''Search the data based on user input'''
        #Get the search condition from the search box
        target = search_entry.get()
        #If there is no search term, tell the user to enter a search term
        if not target:
            results_text.delete("1.0", tk.END)
            results_text.insert(tk.END, "please enter a search term.")
            return
        #If there is a serch term, clear the results box
        #to prepare for showing results
        results_text.delete("1.0", tk.END)
        results_text.insert(tk.END, "Results:\n\n")
        #Set flag so we can show if no data is found
        #after checking
        found = False
        #Go through each record in the list of lists
        for row in list_of_csv:
            #If the search term is anywhere within the list
            if any(target.lower() in field.lower() for field in row):
                #Print out that record
                results_text.insert(tk.END, row)
                results_text.insert(tk.END, "\n")
                #Flag that we have found at least one match
                found = True
        #If no record is found at all
        if not found:
            #Print out to user that no data is found
            results_text.insert(tk.END, "No matching data found.")
        #Clear the search bar
        search_entry.delete(0, tk.END)

    # Create a label and entry for searching the database
    search_label = tk.Label(frame, text="Search through our database:")
    search_label.grid(row=1, column=0)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=1, column=1)
    search_button = tk.Button(frame, text="Search", command=search_csv)
    search_button.grid(row=1, column=2)

    # Create a text box for displaying search results
    results_text = tk.Text(frame, width=50, height=10)
    results_text.grid(row=2, column=0, columnspan=3)

    # Define the function for adding a new employee
    def add_data():
        '''Create the window to add an employee to the list'''
        #Create the add employee box
        add_window = tk.Toplevel(root)
        add_window.title("Add Employee")
        add_frame = tk.Frame(add_window, padx=10, pady=10)
        add_frame.pack()
        #Create a list of all different desired fields
        fields = ["Name", "Position", "SSN", "Address", "Email", "Phone Number", "Skill", "ID"]
        #Create dictionary to hold all entries
        entries = {}
        #Enumerate through the fields, creating an entry box for each and label
        for i, field in enumerate(fields):
            label = tk.Label(add_frame, text=field + ":")
            label.grid(row=i, column=0)
            entry = tk.Entry(add_frame)
            entry.grid(row=i, column=1)
            #Add the entry fields to the dictionary so that
            #we can access them later
            entries[field] = entry
        #Create the submit button
        submit_button = tk.Button(add_frame, text="Add Employee",
                                  command=lambda: add_employee(entries, True))
        submit_button.grid(row=len(fields), column=0, columnspan=2)

    def add_employee(entries, user):
        '''Add the employee to the list'''
        #If we are getting from the user, not testing
        if user:
        # Check if all fields have been filled out
            if not all(entries[field].get() for field in entries):
                messagebox.showerror("Error", "Please fill out all fields.")
                return
            # Filter out unwanted characters from entries
            name = filter_characters(entries["Name"].get())
            position = filter_characters(entries["Position"].get())
            ssn = filter_characters(entries["SSN"].get())
            address = filter_characters(entries["Address"].get())
            email = filter_characters(entries["Email"].get())
            phone_number = filter_characters(entries["Phone Number"].get())
            skill = filter_characters(entries["Skill"].get())
            empl_id = filter_characters(entries["ID"].get())
        else:
            # Filter out unwanted characters from entries
            name = filter_characters(entries["Name"])
            position = filter_characters(entries["Position"])
            ssn = filter_characters(entries["SSN"])
            address = filter_characters(entries["Address"])
            email = filter_characters(entries["Email"])
            phone_number = filter_characters(entries["Phone Number"])
            skill = filter_characters(entries["Skill"])
            empl_id = filter_characters(entries["ID"])
        #shows an error when the user input the wrong format of SSN
        if not ssn.isdigit() or len(ssn) != 9:
            messagebox.showerror("Error", "Invalid SSN. Please enter a 9-digit number.")
            return
        #shows an error when the user input does not include @
        if "@" not in email:
            messagebox.showerror("Error", "Invalid email address.\
                                  Please enter a valid email address.")
            return
        #shows an error if users input is not 10 digits phone number
        if not phone_number.isdigit() or len(phone_number) !=10:
            messagebox.showerror("Error", "Invalid Phone Number.\
                                  Please enter a 10-digit phone number.")
            return
        #Check if the user's input already exsit
        for row in list_of_csv:
            if ssn == row[2] or email == row[4] or phone_number == row[5] or empl_id == row[7]:
                messagebox.showerror("Error", "The data you entered already exist.")
                return
        if user:
            #Clear each entry box
            for field in entries:
                entries[field].delete(0, tk.END)
            #Show the user that the employee has been added
            messagebox.showinfo("Success", "Employee added!")
        #Add the new employee info to the prior list
        list_of_csv.append([name, position, ssn, address, email, phone_number, skill, empl_id])

    def filter_characters(given):
        '''Filter out unwanted characters from a string and return it'''
        #For every character in the string
        for i in given:
            #If the character is one of the unwanted characters
            if i in "#$%<>^&|*()!":
                #Filter out the character
                given = given.replace(i,'')
        #Return the filtered string
        return given

    # Create a button for adding a new employee
    add_button = tk.Button(frame, text="Add Employee", command=add_data)
    add_button.grid(row=3, column=0)

    # Define the function for deleting an employee
    def delete_data():
        '''Delete an entry from the employee list'''
        #Get the delete target from the user
        target = delete_entry.get()
        #If there is no entry in the delete box,
        #tell the user to enter one
        if not target:
            messagebox.showerror("Error", "Please enter a target string.")
            return
        # Flag to indicate whether data has been deleted
        deleted = False
        #Copy the list_of_csv into list_copy so we can
        #iterate through it
        list_copy = copy_list()
        #Go through each entry in the list of lists
        for row in list_copy:
            #Go through each element in the list,
            #searching for the desired element
            for i in row:
                #If we find a match
                if target.lower() in i.lower():
                    #Delete the record and show it has been deleted
                    list_of_csv.remove(row)
                    deleted = True
                    break
                if deleted:
                    break
        #If data has been deleted, show the user
        if deleted:
            messagebox.showinfo("Success", "Data deleted!")
        #Otherwise, show the user that no matching data was found
        else:
            messagebox.showerror("Error", "No matching data found.")
        #Clear the delete text box
        delete_text.config(text="")
        delete_entry.delete(0, tk.END)

    #Function to return a copy of a list
    def copy_list():
        '''Return a copy of the list of employees'''
        return list_of_csv

     #Function to send in random test data
    def test_data():
        '''Function to send in test data'''
        #Create 50 different random employees to test
        num = 0
        while num < 50:
            #Create lists to use in generating random names
            first_name = random.choice(['Tyler','Sa&m','Matt','Bob',
                                        'Dean','Sarah','Emily','Bridget','Ca$ssie','Mary'])
            last_name = random.choice(['Houston','Trevor','Si<nger','Fitter',
                                    'Tremain', 'Buss*er','McDonald','King','War!ms','Foreman'])
            name = first_name + " " + last_name
            #Create list for random positions
            position = random.choice(['Manager','Software Engineer',
                                    'Project Lead','Customer Service','HR Rep'])
            #Create random SSN
            ssn = ""
            while len(ssn) < 9:
                ssn += str(random.randint(0,9))
            #Create random email
            email = ""
            while len(email) < 10:
                email += str(random.choice('abcdefghijklmnopqrstuvwxyz&$#'))
            email += "@gmail.>com"
            #Create random phone number
            phone_num = ""
            while len(phone_num) < 10:
                phone_num += str(random.randint(0,9))
            phone_num += "$$"
            #Create random address
            add = ""
            while len(add) < 5:
                add += str(random.randint(0,9))
            add += " My S#treet"
            #Create random employee ID
            empl_id = ""
            while len(empl_id) < 5:
                empl_id += str(random.randint(0,9))
            #Create random skill list
            skill = random.choice(['C++','Java','C','Leadership'])
            #Place these in the correct fields
            entries = {"Name":name,"Position":position, "SSN":ssn,"Address":add,
                        "Email":email,"Phone Number":phone_num, "Skill":skill, "ID":empl_id}
            #print(entries)
            add_employee(entries, False)
            num += 1


    # Create a label and entry for deleting data
    delete_label = tk.Label(frame, text="Delete data from our database:")
    delete_label.grid(row=4, column=0, padx=20, pady=10)
    delete_entry = tk.Entry(frame)
    delete_entry.grid(row=4, column=1, padx=20, pady=10)
    delete_button = tk.Button(frame, text="Delete", command=delete_data)
    delete_button.grid(row=4, column=2, padx=20, pady=10)

    delete_text = tk.Label(frame, text="")
    delete_text.grid(row=5, column=0, columnspan=3)

    #Create button to load data
    load_button = tk.Button(frame, text="Load Data", command=test_data)
    load_button.grid(row=6, column = 0, padx = 20, pady = 20)

    # Create a mainloop for the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
