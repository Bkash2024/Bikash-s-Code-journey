"""
Simple BMI Calculator
Standalone Windows application with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys


class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Configure style
        self.setup_styles()

        # Create main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(main_frame, text="BMI Calculator",
                         font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Unit selection
        ttk.Label(main_frame, text="Unit System:",
                 font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)

        self.unit_var = tk.StringVar(value="metric")
        unit_frame = ttk.Frame(main_frame)
        unit_frame.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Radiobutton(unit_frame, text="Metric (kg, cm)",
                       variable=self.unit_var, value="metric",
                       command=self.update_labels).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(unit_frame, text="Imperial (lb, in)",
                       variable=self.unit_var, value="imperial",
                       command=self.update_labels).pack(side=tk.LEFT, padx=5)

        # Weight input
        self.weight_label = ttk.Label(main_frame, text="Weight (kg):",
                                      font=("Arial", 10))
        self.weight_label.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(main_frame, textvariable=self.weight_var,
                                     font=("Arial", 12), width=20)
        self.weight_entry.grid(row=2, column=1, pady=10)

        # Height input
        self.height_label = ttk.Label(main_frame, text="Height (cm):",
                                      font=("Arial", 10))
        self.height_label.grid(row=3, column=0, sticky=tk.W, pady=10)

        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(main_frame, textvariable=self.height_var,
                                     font=("Arial", 12), width=20)
        self.height_entry.grid(row=3, column=1, pady=10)

        # Calculate button
        calc_button = ttk.Button(main_frame, text="Calculate BMI",
                                command=self.calculate_bmi)
        calc_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Result frame
        result_frame = ttk.LabelFrame(main_frame, text="Results", padding="15")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E),
                         pady=10)

        self.bmi_result = ttk.Label(result_frame, text="BMI: --",
                                   font=("Arial", 16, "bold"))
        self.bmi_result.pack(pady=5)

        self.category_result = ttk.Label(result_frame, text="Category: --",
                                        font=("Arial", 12))
        self.category_result.pack(pady=5)

        # BMI Categories reference
        categories_frame = ttk.LabelFrame(main_frame, text="BMI Categories",
                                         padding="10")
        categories_frame.grid(row=6, column=0, columnspan=2,
                             sticky=(tk.W, tk.E), pady=10)

        categories_text = [
            "Underweight: < 18.5",
            "Normal weight: 18.5 - 24.9",
            "Overweight: 25.0 - 29.9",
            "Obese: ≥ 30.0"
        ]

        for cat in categories_text:
            ttk.Label(categories_frame, text=cat,
                     font=("Arial", 9)).pack(anchor=tk.W, pady=2)

        # Clear button
        clear_button = ttk.Button(main_frame, text="Clear",
                                 command=self.clear_inputs)
        clear_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Bind Enter key to calculate
        self.root.bind('<Return>', lambda e: self.calculate_bmi())

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

    def update_labels(self):
        """Update labels based on selected unit system"""
        if self.unit_var.get() == "metric":
            self.weight_label.config(text="Weight (kg):")
            self.height_label.config(text="Height (cm):")
        else:
            self.weight_label.config(text="Weight (lb):")
            self.height_label.config(text="Height (in):")

    def calculate_bmi(self):
        """Calculate BMI and display results"""
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Invalid Input",
                                   "Weight and height must be positive numbers!")
                return

            # Convert to metric if imperial
            if self.unit_var.get() == "imperial":
                weight = weight * 0.453592  # lb to kg
                height = height * 2.54  # inches to cm

            # Calculate BMI (height in meters)
            height_m = height / 100
            bmi = weight / (height_m ** 2)

            # Determine category
            category = self.get_bmi_category(bmi)

            # Display results
            self.bmi_result.config(text=f"BMI: {bmi:.1f}")
            self.category_result.config(text=f"Category: {category}")

            # Color code the category
            color = self.get_category_color(category)
            self.category_result.config(foreground=color)

        except ValueError:
            messagebox.showerror("Invalid Input",
                               "Please enter valid numbers for weight and height!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_bmi_category(self, bmi):
        """Determine BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def get_category_color(self, category):
        """Get color for category"""
        colors = {
            "Underweight": "#3498db",
            "Normal weight": "#2ecc71",
            "Overweight": "#f39c12",
            "Obese": "#e74c3c"
        }
        return colors.get(category, "#000000")

    def clear_inputs(self):
        """Clear all inputs and results"""
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_result.config(text="BMI: --")
        self.category_result.config(text="Category: --", foreground="#000000")
        self.weight_entry.focus()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
