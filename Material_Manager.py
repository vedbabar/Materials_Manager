import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os  # Import os module for path operations
import math  # Import math module for log
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the Excel data
try:
    df = pd.read_excel("sample_material_data.xlsx")
except FileNotFoundError:
    messagebox.showerror("Error",
                         "sample_material_data.xlsx not found. Please make sure the file is in the same directory.")
    exit()

# Create the main window
root = tk.Tk()
root.title("Material Data")
root.geometry("1250x750")
root.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style(root)
style.theme_use('clam')

style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=25,
    fieldbackground="white",
    font=('Segoe UI', 10)
)

style.map(
    'Treeview',
    background=[('selected', '#347083')],
    foreground=[('selected', 'white')]
)

style.configure(
    "Treeview.Heading",
    font=('Segoe UI', 11, 'bold'),
    background="#4a7abc",
    foreground="white"
)

# Button styles for material type toggling
style.configure('Material.TButton', background='#f0f0f0', foreground='black')
style.configure('SelectedMaterial.TButton', background='#87ceeb', foreground='black')

# Add Data Button Style
style.configure('AddData.TButton', background='#28a745', foreground='white', font=('Segoe UI', 10, 'bold'))
style.map('AddData.TButton', background=[('active', '#218838')])

# Download Button Style
style.configure('Download.TButton', background='#ADD8E6', foreground='white', font=('Segoe UI', 10, 'bold'))
style.map('Download.TButton', background=[('active', '#0056b3')])

# --------- Main Frame Setup ---------
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill='both', expand=True)

# --------- Search & Filter Frame ---------
search_filter_add_frame = ttk.Frame(main_frame)
search_filter_add_frame.pack(fill='x', pady=(0, 10))

# Search & Filter controls sub-frame (to group them on the left)
search_filter_controls_frame = ttk.Frame(search_filter_add_frame)
search_filter_controls_frame.pack(side='left', fill='x', expand=True)

# Search by Material
ttk.Label(search_filter_controls_frame, text="Search Material:", font=('Segoe UI', 11)).pack(side='left', padx=(0, 5))

search_var = tk.StringVar()
search_entry = ttk.Entry(search_filter_controls_frame, textvariable=search_var, font=('Segoe UI', 11), width=20)
search_entry.pack(side='left', padx=(0, 10))

# Sorting dropdown
ttk.Label(search_filter_controls_frame, text="Sort by:", font=('Segoe UI', 11)).pack(side='left')

sort_var = tk.StringVar()
sort_options = ["None", "UTS", "Yield strength", "Endurance Strength"]

sort_combobox = ttk.Combobox(
    search_filter_controls_frame,
    textvariable=sort_var,
    values=sort_options,
    state='readonly',
    width=15,
    font=('Segoe UI', 10)
)
sort_combobox.set("Select a column")
sort_combobox.pack(side='left', padx=(0, 10))

# Manufacturing Process Filter
ttk.Label(search_filter_controls_frame, text="Filter Mfg. Process:", font=('Segoe UI', 11)).pack(side='left')

mfg_process_var = tk.StringVar()
mfg_process_options = ["All"] + sorted(df['Manufacturing process'].dropna().unique().tolist())

mfg_process_combobox = ttk.Combobox(
    search_filter_controls_frame,
    textvariable=mfg_process_var,
    values=mfg_process_options,
    state='readonly',
    width=15,
    font=('Segoe UI', 10)
)
mfg_process_combobox.set("All")
mfg_process_combobox.pack(side='left', padx=(0, 10))

# Applications Filter
ttk.Label(search_filter_controls_frame, text="Filter Applications:", font=('Segoe UI', 11)).pack(side='left')

applications_var = tk.StringVar()
applications_options = ["All"] + sorted(df['Applications'].dropna().unique().tolist())

applications_combobox = ttk.Combobox(
    search_filter_controls_frame,
    textvariable=applications_var,
    values=applications_options,
    state='readonly',
    width=15,
    font=('Segoe UI', 10)
)
applications_combobox.set("All")
applications_combobox.pack(side='left')

# --------- Treeview Widget Setup ---------
tree = ttk.Treeview(main_frame, columns=list(df.columns), show='headings')

for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=110, anchor='center')

vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

vsb.pack(side='right', fill='y')
tree.pack(fill='both', expand=True)

# --------- Material Type Buttons Frame (Above horizontal scrollbar) ---------
material_type_frame = ttk.Frame(main_frame)
material_type_frame.pack(fill='x', pady=(10, 5))

ttk.Label(material_type_frame, text="Filter by Material Type:", font=('Segoe UI', 11, 'bold')).pack(side='left',
                                                                                                    padx=(0, 10))

material_type_filter = tk.StringVar(value="")  # No filter initially

material_types = ["Steel", "Aluminum", "Cast Iron"]
selected_material_button = None  # To track which button is selected


def material_type_button_clicked(mat):
    global selected_material_button
    current = material_type_filter.get()

    if current == mat:
        # Deselect if same button clicked again
        material_type_filter.set("")
        if selected_material_button:
            selected_material_button.configure(style='Material.TButton')
            selected_material_button = None
    else:
        # Select new button and update styles
        material_type_filter.set(mat)

        if selected_material_button:
            selected_material_button.configure(style='Material.TButton')

        for btn in material_type_buttons:
            if btn['text'] == mat:
                btn.configure(style='SelectedMaterial.TButton')
                selected_material_button = btn
                break

    update_view()


material_type_buttons = []
for mat in material_types:
    btn = ttk.Button(
        material_type_frame,
        text=mat,
        width=12,
        style='Material.TButton',
        command=lambda m=mat: material_type_button_clicked(m)
    )
    btn.pack(side='left', padx=5)
    material_type_buttons.append(btn)

hsb.pack(side='bottom', fill='x')  # Horizontal scrollbar at bottom


# --------- Function to Display Data in Treeview ---------
def display_data(dataframe):
    tree.delete(*tree.get_children())
    for i, (_, row) in enumerate(dataframe.iterrows()):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=list(row), tags=(tag,))
    tree.tag_configure('evenrow', background='white')
    tree.tag_configure('oddrow', background='#e6f2ff')


# Initial load of all data
display_data(df)


# --------- Update View on Filters/Search/Sort ---------
def update_view(*args):
    global df  # Ensure we use the global df

    filtered_df = df.copy()

    # Filter by Material search text
    search_text = search_var.get().strip().lower()
    if search_text:
        filtered_df = filtered_df[filtered_df['Material'].str.lower().str.contains(search_text, na=False)]

    # Filter Manufacturing Process
    mfg_value = mfg_process_var.get()
    if mfg_value != "All":
        filtered_df = filtered_df[filtered_df['Manufacturing process'] == mfg_value]

    # Filter Applications
    app_value = applications_var.get()
    if app_value != "All":
        filtered_df = filtered_df[filtered_df['Applications'] == app_value]

    # Filter Material Type from buttons
    mat_type = material_type_filter.get()
    if mat_type:
        filtered_df = filtered_df[filtered_df['Material'].str.contains(mat_type, case=False, na=False)]

    # Sort data if valid column selected
    sort_column = sort_var.get()
    if sort_column and sort_column in sort_options and sort_column != "None":
        try:
            # Convert to numeric for proper sorting if applicable
            if sort_column in ["Youngs modulus", "Poissons ratio", "UTS", "Yield strength", "Endurance Strength"]:
                # Ensure the column exists before attempting to sort
                if sort_column in filtered_df.columns:
                    filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
                    # Use a custom sort key to handle mixed types by coercing to numeric,
                    # placing non-numeric values (NaN after coerce) at the end.
                    filtered_df[sort_column] = pd.to_numeric(filtered_df[sort_column], errors='coerce')
                    filtered_df = filtered_df.sort_values(by=sort_column, ascending=True, na_position='last')
                else:
                    messagebox.showwarning("Column Not Found",
                                           f"Sorting column '{sort_column}' not found in current data.")
            else:
                filtered_df = filtered_df.sort_values(by=sort_column, ascending=True)
        except Exception as e:
            messagebox.showerror("Sorting Error", f"Could not sort by {sort_column}: {e}")

    display_data(filtered_df)
    check_download_button_state()  # Update download button state after view update


# Bind events to trigger filtering and sorting
search_var.trace_add('write', update_view)
sort_combobox.bind('<<ComboboxSelected>>', update_view)
mfg_process_combobox.bind('<<ComboboxSelected>>', update_view)
applications_combobox.bind('<<ComboboxSelected>>', update_view)


# --------- Add Data Functionality ---------
def add_data():
    add_window = tk.Toplevel(root)
    add_window.title("Add New Material Data")
    add_window.geometry("500x600")
    add_window.transient(root)  # Make it appear on top of the main window
    add_window.grab_set()  # Disable interaction with the main window

    form_frame = ttk.Frame(add_window, padding=20)
    form_frame.pack(fill='both', expand=True)

    entries = {}
    for i, col in enumerate(df.columns):
        ttk.Label(form_frame, text=f"{col}:", font=('Segoe UI', 10)).grid(row=i, column=0, sticky='w', pady=5, padx=5)
        entry = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
        entry.grid(row=i, column=1, sticky='ew', pady=5, padx=5)
        entries[col] = entry

    def submit_new_data():
        global df
        new_row_data = {}
        for col, entry_widget in entries.items():
            value = entry_widget.get().strip()
            # Basic type conversion for numeric columns, handle errors gracefully
            if col in ["Youngs modulus", "Poissons ratio", "UTS", "Yield strength", "Endurance Strength",
                       "%EL"]:  # Changed %elongation to %EL
                try:
                    new_row_data[col] = float(value) if value else None  # Convert to float, None if empty
                except ValueError:
                    messagebox.showerror("Input Error", f"Please enter a valid number for '{col}'.")
                    return
            else:
                new_row_data[col] = value if value else None  # Store None for empty strings

        # Create a new DataFrame from the new row
        new_row_df = pd.DataFrame([new_row_data])

        # Append the new row to the main DataFrame
        df = pd.concat([df, new_row_df], ignore_index=True)

        # Save the updated DataFrame back to Excel
        try:
            df.to_excel("sample_material_data.xlsx", index=False)
            messagebox.showinfo("Success", "New data added successfully and saved to Excel.")
            update_view()  # Refresh the Treeview
            add_window.destroy()  # Close the add data window
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data to Excel: {e}")

    submit_button = ttk.Button(
        form_frame,
        text="Add Data",
        command=submit_new_data,
        style='AddData.TButton'
    )
    submit_button.grid(row=len(df.columns), column=0, columnspan=2, pady=20)


# --------- Download Data Functionality ---------
def download_selected_row_details():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a row to download details.")
        return

    # Get the values of the selected row
    values = tree.item(selected_item, 'values')

    # Create a dictionary of the selected row data using column names
    selected_row_dict = dict(zip(df.columns, values))

    # --- Extract required properties ---
    material_name = selected_row_dict.get('Material', 'N/A')
    mfg_process = selected_row_dict.get('Manufacturing process', 'N/A')
    applications = selected_row_dict.get('Applications', 'N/A')
    density = selected_row_dict.get('Density', 'N/A')

    # Convert extracted values to float, handling potential missing or non-numeric data
    try:
        yield_strength = float(selected_row_dict.get('Yield strength')) if selected_row_dict.get(
            'Yield strength') is not None else None
        uts = float(selected_row_dict.get('UTS')) if selected_row_dict.get('UTS') is not None else None
        # Changed from '%elongation' to '%EL'
        percent_elongation = float(selected_row_dict.get('%EL')) if selected_row_dict.get('%EL') is not None else None
        youngs_modulus = float(selected_row_dict.get('Youngs modulus')) if selected_row_dict.get(
            'Youngs modulus') is not None else None
    except ValueError:
        messagebox.showerror("Data Error",
                             "Could not convert one or more required properties to numbers. Please check the data in the Excel file.")
        return

    # --- Perform Calculations ---
    calculated_values = []
    calculation_errors = []

    # 1) Nominal strain at yield = yield strength / young's modulus
    if yield_strength is not None and youngs_modulus is not None and youngs_modulus != 0:
        nominal_strain_at_yield = yield_strength / youngs_modulus
        calculated_values.append(f"Nominal strain at yield: {nominal_strain_at_yield:.9f}")
    else:
        nominal_strain_at_yield = None
        calculation_errors.append(
            "Nominal strain at yield: Missing Yield Strength or Young's Modulus or Young's Modulus is zero.")

    # 2) Nominal strain at UTS = %elongation/100
    if percent_elongation is not None:
        nominal_strain_at_uts = percent_elongation / 100.0
        calculated_values.append(f"Nominal strain at UTS: {nominal_strain_at_uts:.9f}")
    else:
        nominal_strain_at_uts = None
        calculation_errors.append("Nominal strain at UTS: Missing %EL.")  # Changed message

    # 3) At yield engineering strain = Nominal strain at yield
    at_yield_engg_strain = nominal_strain_at_yield
    if at_yield_engg_strain is not None:
        calculated_values.append(f"At yield engineering strain: {at_yield_engg_strain:.9f}")
    else:
        calculated_values.append("At yield engineering strain: Not calculable (see above).")

    # 4) At yield true strain = log base e (1+at yield engineering strain)
    if at_yield_engg_strain is not None and (1 + at_yield_engg_strain) > 0:
        at_yield_true_strain = math.log(1 + at_yield_engg_strain)
        calculated_values.append(f"At yield true strain: {at_yield_true_strain:.5f}")
    else:
        at_yield_true_strain = None
        calculation_errors.append("At yield true strain: Cannot calculate log (1+engg strain <= 0).")

    # 5) At yield true stress = yield strength*(1 + at yield engg strain)
    if yield_strength is not None and at_yield_engg_strain is not None:
        at_yield_true_stress = yield_strength * (1 + at_yield_engg_strain)
        calculated_values.append(f"At yield true stress: {at_yield_true_stress:.2f}")
    else:
        at_yield_true_stress = None
        calculation_errors.append("At yield true stress: Missing Yield Strength or At yield engineering strain.")

    # 6) At UTS true strain = log base e ( 1+ %elongation/100)
    if nominal_strain_at_uts is not None and (1 + nominal_strain_at_uts) > 0:
        at_uts_true_strain = math.log(1 + nominal_strain_at_uts)
        calculated_values.append(f"At UTS true strain: {at_uts_true_strain:.9f}")
    else:
        at_uts_true_strain = None
        calculation_errors.append("At UTS true strain: Cannot calculate log (1+nominal strain at UTS <= 0).")

    # 7) At UTS true stress = UTS * (1+%elongation/100)
    if uts is not None and nominal_strain_at_uts is not None:
        at_uts_true_stress = uts * (1 + nominal_strain_at_uts)
        calculated_values.append(f"At UTS true stress: {at_uts_true_stress:.2f}")
    else:
        at_uts_true_stress = None
        calculation_errors.append("At UTS true stress: Missing UTS or Nominal strain at UTS.")

    # 8) Plastic strain at yield = At yield true strain - (At yield true stress/youngs modulus)
    if at_yield_true_strain is not None and at_yield_true_stress is not None and youngs_modulus is not None and youngs_modulus != 0:
        plastic_strain_at_yield = at_yield_true_strain - (at_yield_true_stress / youngs_modulus)
        calculated_values.append(f"Plastic strain at yield: {plastic_strain_at_yield:.9f}")
    else:
        plastic_strain_at_yield = None
        calculation_errors.append(
            "Plastic strain at yield: Missing required values for calculation or Young's Modulus is zero.")

    # 9) Plastic strain at UTS = At UTS true strain-(at UTS true stress/youngs modulus)
    if at_uts_true_strain is not None and at_uts_true_stress is not None and youngs_modulus is not None and youngs_modulus != 0:
        plastic_strain_at_uts = at_uts_true_strain - (at_uts_true_stress / youngs_modulus)
        calculated_values.append(f"Plastic strain at UTS: {plastic_strain_at_uts:.5f}")
    else:
        plastic_strain_at_uts = None
        calculation_errors.append(
            "Plastic strain at UTS: Missing required values for calculation or Young's Modulus is zero.")

    # --- Construct Output Content ---
    #my code




    #.inp file format 
    #*****START*****
    output_content = f"**\n"
    output_content += f"**HMNAME MATS          1 {material_name}     3\n"
    output_content += f"*MATERIAL, NAME={material_name}\n"
    output_content += f"DENSITY\n"
    output_content += f"{density},0.0 \n"
    output_content += f"*ELASTIC, TYPE = ISOTROPIC\n"
    output_content += f"{youngs_modulus}  ,{percent_elongation/100.00}      ,0.0 \n"
    output_content += f"*PLASTIC\n"
    output_content += f"{yield_strength:.2f}	  ,0.00000   ,0.0\n"
    output_content += f"{at_yield_true_stress:.2f}	  ,{at_yield_true_strain:.5f}   ,0.0\n"
    output_content += f"{at_uts_true_stress:.2f}	  ,{plastic_strain_at_uts:.5f}   ,0.0\n"
    output_content += f"*****\n"
    #*****END*****








    #my code
    # output_content += f"Material: {material_name}\n"
    # output_content += f"Manufacturing Process: {mfg_process}\n"
    # output_content += f"Applications: {applications}\n\n"

    # output_content += "--- Input Properties (from selected row) ---\n"
    # output_content += f"Yield strength: {yield_strength if yield_strength is not None else 'N/A'}\n"
    # output_content += f"UTS: {uts if uts is not None else 'N/A'}\n"
    # output_content += f"%EL: {percent_elongation if percent_elongation is not None else 'N/A'}\n"  # Changed %elongation to %EL
    # output_content += f"Young's modulus: {youngs_modulus if youngs_modulus is not None else 'N/A'}\n\n"

    # output_content += "--- Calculated Mechanical Properties ---\n"
    # output_content += "\n".join(calculated_values)

    if calculation_errors:
        output_content += "\n\n--- Calculation Warnings/Errors ---\n"
        output_content += "\n".join(calculation_errors)

    # Open a file dialog to choose where to save the file
    initial_filename = f"NL_{material_name.replace(' ', '_')}.inp"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".inp",
        filetypes=[("INP files", "*.inp"), ("All files", "*.*")],
        initialfile=initial_filename
    )

    if file_path:
        try:
            with open(file_path, "w") as f:
                f.write(output_content)
            messagebox.showinfo("Download Complete", f"Calculated details saved to:\n{os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to save file: {e}")



#**********BDF file Generator***************

def download_bdf_files():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("No Selection", "Please select at least one row to download .bdf files.")
        return

    for item in selected_items:
        values = tree.item(item, 'values')
        selected_row_dict = dict(zip(df.columns, values))

        material_name = selected_row_dict.get('Material', 'UNKNOWN')
        youngs_modulus = selected_row_dict.get("Youngs modulus", "0.0")
        poissons_ratio = selected_row_dict.get("Poissons ratio", "0.0")
        density = selected_row_dict.get("Density", "0.0")

        try:
            youngs_modulus = float(youngs_modulus)
        except:
            youngs_modulus = 0.0
        try:
            poissons_ratio = float(poissons_ratio)
        except:
            poissons_ratio = 0.0
        try:
            density = float(density)
        except:
            density = 0.0

        # Construct BDF content
        bdf_content = ""
        bdf_content += f'$HMNAME MAT                    1"{material_name}" "MAT1"\n'
        bdf_content += f"$HWCOLOR MAT                   1       3\n"
        exp_density = f"{density:.2e}"       # e.g., '1.12e+09'
        mantissa, exponent = exp_density.split('e')  # '1.12', '+09'
        sign = '+' if int(exponent) >= 0 else '-'    # get sign based on exponent
        bdf_density = f"{mantissa}{sign}{abs(int(exponent)):02d}"  # '1.12+09' or '1.12-09'

        bdf_content += f"MAT1    1       {youngs_modulus:<10.1f}      {poissons_ratio:<6.2f}  {bdf_density}\n"
        bdf_content += f"$2345678$2345678$2345678$2345678$2345678$2345678\n"
        bdf_content += f"| material name |  ID(1)   |  Young's modulus| blank | poissons ratio|density|\n"

        # Save file
        initial_filename = f"{material_name.replace(' ', '_')}.bdf"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bdf",
            filetypes=[("BDF files", "*.bdf"), ("All files", "*.*")],
            initialfile=initial_filename
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(bdf_content)
                messagebox.showinfo("Download Complete", f".bdf file saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Download Error", f"Failed to save .bdf file: {e}")



# Function to enable/disable download button based on selection
def check_download_button_state(*args):
    if tree.selection():
        download_menu_button.config(state='normal')
    else:
        download_menu_button.config(state='disabled')


# Bind the Treeview selection event to the state checker
tree.bind('<<TreeviewSelect>>', check_download_button_state)

# --------- Add Data Button to Main Window ---------
add_data_button = ttk.Button(
    search_filter_add_frame,  # Placed in the combined search/filter/add frame
    text="Add Data",
    command=add_data,
    style='AddData.TButton'
)
add_data_button.pack(side='right', padx=(10, 5))  # Pack it to the right of controls


#*******graphs for comparison************
def show_stress_strain_plot(mat1, mat2):
    compare_window = tk.Toplevel(root)
    compare_window.title("Stress-Strain Curve Comparison")
    compare_window.geometry("800x600")

    fig, ax = plt.subplots(figsize=(8, 5))

    for mat in [mat1, mat2]:
        # Elastic line: from (0, 0) to (ε_yield, σ_yield)
        x1 = [0, mat['yield_strain']]
        y1 = [0, mat['yield_strength']]

        # Plastic line: from (ε_yield, σ_yield) to (ε_final, σ_uts)
        x2 = [mat['yield_strain'], mat['elongation']]
        y2 = [mat['yield_strength'], mat['uts']]

        ax.plot(x1 + x2, y1 + y2, label=mat['name'], linewidth=2)

    ax.set_title("Stress-Strain Comparison")
    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (MPa)")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=compare_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def compare_selected_materials():
    selected = tree.selection()
    if len(selected) != 2:
        messagebox.showwarning("Invalid Selection", "Please select exactly two rows to compare.")
        return

    materials = []
    for item in selected:
        values = tree.item(item, 'values')
        material = dict(zip(df.columns, values))
        try:
            youngs = float(material.get('Youngs modulus'))
            yield_strength = float(material.get('Yield strength'))
            uts = float(material.get('UTS'))
            elongation = float(material.get('%EL')) / 100.0
        except (ValueError, TypeError):
            messagebox.showerror("Invalid Data", "Selected materials must have numeric mechanical properties.")
            return

        # Calculate yield strain
        yield_strain = yield_strength / youngs
        stress_strain_data = {
            'name': material['Material'],
            'youngs': youngs,
            'yield_strength': yield_strength,
            'yield_strain': yield_strain,
            'uts': uts,
            'elongation': elongation
        }
        materials.append(stress_strain_data)

    show_stress_strain_plot(materials[0], materials[1])


compare_button = ttk.Button(
    search_filter_add_frame,
    text="Compare",
    command=compare_selected_materials,
    style='AddData.TButton'
)
compare_button.pack(side='right', padx=(10, 5))


# --------- Download Data Button to Main Window ---------
# --------- Download Dropdown Menu ---------
download_menu_button = ttk.Menubutton(
    search_filter_add_frame,
    text="Download",
    style='Download.TButton'
)
download_menu = tk.Menu(download_menu_button, tearoff=0)
download_menu_button["menu"] = download_menu

def download_inp_for_selected():
    for item in tree.selection():
        tree.selection_set(item)
        download_selected_row_details()

def download_bdf_for_selected():
    download_bdf_files()

download_menu.add_command(label="Download .inp file", command=download_inp_for_selected)
download_menu.add_command(label="Download .bdf file", command=download_bdf_for_selected)

download_menu_button.pack(side='right', padx=(5, 10))


# Initial check for download button state
check_download_button_state()

root.mainloop()