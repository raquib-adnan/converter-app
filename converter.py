import tkinter as tk
from tkinter import ttk
from currency_api import convert_currency, get_currency_list

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('TCombobox', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))
        
        # Conversion factors
        self.length_factors = {
            'meter': 1,
            'kilometer': 1000,
            'centimeter': 0.01,
            'millimeter': 0.001,
            'foot': 0.3048,
            'inch': 0.0254,
            'mile': 1609.34,
            'yard': 0.9144
        }
        
        self.weight_factors = {
            'kilogram': 1,
            'gram': 0.001,
            'milligram': 0.000001,
            'pound': 0.453592,
            'ounce': 0.0283495,
            'ton': 1000
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Unit Converter", font=('Segoe UI', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Category selection
        category_frame = ttk.Frame(main_frame)
        category_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        ttk.Label(category_frame, text="Category:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, width=20)
        self.category_combo['values'] = ('Length', 'Weight', 'Temperature', 'Currency')
        self.category_combo.pack(side=tk.LEFT)
        self.category_combo.bind('<<ComboboxSelected>>', self.update_units)
        
        # Input value
        value_frame = ttk.Frame(main_frame)
        value_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(value_frame, text="Value:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(value_frame, textvariable=self.value_var, width=20)
        self.value_entry.pack(side=tk.LEFT)
        
        # Conversion frame
        conversion_frame = ttk.Frame(main_frame)
        conversion_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # From unit
        from_frame = ttk.Frame(conversion_frame)
        from_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(from_frame, text="From:", font=('Segoe UI', 10, 'bold')).pack()
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(from_frame, textvariable=self.from_var, width=15)
        self.from_combo.pack(pady=5)
        
        # To unit
        to_frame = ttk.Frame(conversion_frame)
        to_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(to_frame, text="To:", font=('Segoe UI', 10, 'bold')).pack()
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(to_frame, textvariable=self.to_var, width=15)
        self.to_combo.pack(pady=5)
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert", command=self.convert, style='Accent.TButton')
        self.convert_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Result frame
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                                    font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.result_label.pack()
        
        # Last updated timestamp
        self.timestamp_var = tk.StringVar()
        self.timestamp_label = ttk.Label(result_frame, textvariable=self.timestamp_var,
                                       font=('Segoe UI', 8), foreground='#7f8c8d')
        self.timestamp_label.pack(pady=(5, 0))
        
        # Initialize with length units
        self.update_units()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def update_units(self, event=None):
        category = self.category_var.get()
        if category == 'Length':
            units = list(self.length_factors.keys())
        elif category == 'Weight':
            units = list(self.weight_factors.keys())
        elif category == 'Temperature':
            units = ['Celsius', 'Fahrenheit', 'Kelvin']
        else:  # Currency
            units = [code for code, _ in get_currency_list()]
            
        self.from_combo['values'] = units
        self.to_combo['values'] = units
        
        if units:
            self.from_combo.set(units[0])
            self.to_combo.set(units[1] if len(units) > 1 else units[0])
            
    def convert(self):
        try:
            value = float(self.value_var.get())
            from_unit = self.from_var.get()
            to_unit = self.to_var.get()
            category = self.category_var.get()
            
            if category == 'Length':
                result = self.convert_length(value, from_unit, to_unit)
                self.timestamp_var.set('')
            elif category == 'Weight':
                result = self.convert_weight(value, from_unit, to_unit)
                self.timestamp_var.set('')
            elif category == 'Temperature':
                result = self.convert_temperature(value, from_unit, to_unit)
                self.timestamp_var.set('')
            else:  # Currency
                result, timestamp = convert_currency(from_unit, to_unit, value)
                if timestamp:
                    self.timestamp_var.set(f"Last updated: {timestamp}")
                else:
                    self.timestamp_var.set("Error fetching rates")
                    
            if result is not None:
                self.result_var.set(f"{value} {from_unit} = {result:.2f} {to_unit}")
            else:
                self.result_var.set("Conversion failed")
                
        except ValueError:
            self.result_var.set("Please enter a valid number")
            
    def convert_length(self, value, from_unit, to_unit):
        return value * (self.length_factors[from_unit] / self.length_factors[to_unit])
        
    def convert_weight(self, value, from_unit, to_unit):
        return value * (self.weight_factors[from_unit] / self.weight_factors[to_unit])
        
    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return value
            
        # Convert to Celsius first
        if from_unit == 'Fahrenheit':
            celsius = (value - 32) * 5/9
        elif from_unit == 'Kelvin':
            celsius = value - 273.15
        else:  # Celsius
            celsius = value
            
        # Convert from Celsius to target unit
        if to_unit == 'Fahrenheit':
            return celsius * 9/5 + 32
        elif to_unit == 'Kelvin':
            return celsius + 273.15
        else:  # Celsius
            return celsius

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverter(root)
    root.mainloop() 