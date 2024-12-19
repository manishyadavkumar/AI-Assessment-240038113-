from tkinter import *
from tkinter import ttk, messagebox
from owlready2 import *

# Load Ontology
ONTOLOGY_PATH = "/Users/gaurabshrestha/Desktop/Python Practice/intelligent_tutoring_system.owl"

# GUI Application Class
class ArithmeticTutor:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent Tutoring System - Arithmetic Operations")
        self.root.geometry("500x500")

        # Load the ontology
        self.ontology = get_ontology(ONTOLOGY_PATH).load()
        self.operations = ["Addition", "Subtraction", "Multiplication", "Division"]

        # Input Fields and Labels
        Label(root, text="Select Operation:").pack(pady=5)
        self.operation_var = StringVar()
        self.operation_menu = ttk.Combobox(root, textvariable=self.operation_var, values=self.operations, state="readonly")
        self.operation_menu.pack(pady=5)
        self.operation_menu.current(0)  # Default selection

        Label(root, text="Enter First Number:").pack(pady=5)
        self.input1 = Entry(root)
        self.input1.pack(pady=5)

        Label(root, text="Enter Second Number:").pack(pady=5)
        self.input2 = Entry(root)
        self.input2.pack(pady=5)

        # Submit Button
        self.submit_button = Button(root, text="Calculate", command=self.calculate)
        self.submit_button.pack(pady=10)

        # Output Result Label
        self.result_label = Label(root, text="Result: ", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)

    def calculate(self):
        try:
            num1 = float(self.input1.get())
            num2 = float(self.input2.get())
            operation = self.operation_var.get()

            # Perform calculations
            result = None
            if operation == "Addition":
                result = num1 + num2
                feedback = self.get_feedback("Addition")
            elif operation == "Subtraction":
                result = num1 - num2
                feedback = self.get_feedback("Subtraction")
            elif operation == "Multiplication":
                result = num1 * num2
                feedback = self.get_feedback("Multiplication")
            elif operation == "Division":
                if num2 == 0:
                    messagebox.showerror("Error", "Division by zero is not allowed!")
                    return
                result = num1 / num2
                feedback = self.get_feedback("Division")
            else:
                messagebox.showerror("Error", "Invalid operation selected!")
                return

            # Display the result
            self.result_label.config(text=f"Result: {result}\n{feedback}")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def get_feedback(self, operation_type):
        """
        Query the ontology for feedback related to the operation.
        """
        feedback = "Well done!"  # Default feedback
        for op in self.ontology.Operation.instances():
            if op.name.lower() == operation_type.lower():
                if hasattr(op, "requiresFeedback"):
                    feedback = op.requiresFeedback[0]
        return feedback

# Main Application Runner
if __name__ == "__main__":
    root = Tk()
    app = ArithmeticTutor(root)
    root.mainloop()
