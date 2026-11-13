# github.com/johnlloydpenamante

import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import pandas as pd

# Global variables
summary_df = None
frequency_tables = {}


def load_and_process_data():
    """Loads the Google Sheet, cleans data, maps questionnaire values, and computes stats."""
    global summary_df, frequency_tables

    file_path = "https://docs.google.com/spreadsheets/d/142sXSkm9F-zswkNVgv1mGMX9DhNCh6ecPv-iPXdW83k/export?format=xlsx"
    df = pd.read_excel(file_path, sheet_name="final_data")

    # Clean the data
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.drop_duplicates()

    # Mapping of values
    frequency_scale = {
        1: "Never",
        2: "Rarely",
        3: "Sometimes",
        4: "Often",
        5: "Always",
        1.0: "Never",
        2.0: "Rarely",
        3.0: "Sometimes",
        4.0: "Often",
        5.0: "Always",
    }

    concentration_scale = {
        1: "Very poor",
        2: "Poor",
        3: "Fair",
        4: "Good",
        5: "Very good",
        1.0: "Very poor",
        2.0: "Poor",
        3.0: "Fair",
        4.0: "Good",
        5.0: "Very good",
    }

    for col in df.columns:
        col_lower = col.lower()

        # 1. Sex Column
        if "sex" in col_lower:
            df[col] = df[col].replace(
                {1: "Male", 2: "Female", 1.0: "Male", 2.0: "Female"}
            )

        # 2. Frequency Likert Scale (Q8, Q12, Q20, Q22)
        elif any(
            q in col_lower
            for q in [
                "8",
                "12",
                "20",
                "22",
                "postpone",
                "sleepiness",
                "notification",
                "before sleep",
            ]
        ):
            df[col] = df[col].replace(frequency_scale)

        # 3. Concentration Rating Scale (Q21)
        elif any(q in col_lower for q in ["21", "concentrat"]):
            df[col] = df[col].replace(concentration_scale)

        else:
            # Convert remaining numeric columns: Age, Hours, Minutes, Days
            df[col] = pd.to_numeric(df[col], errors="coerce")

    frequency_tables = {}
    summary = []

    # Analyze each column
    for col in df.columns:
        data = df[col].dropna()

        # Frequency and Percentage table
        freq = (
            data.value_counts().sort_index()
            if data.dtype != "object"
            else data.value_counts()
        )
        percent = (freq / len(data)) * 100

        freq_table = pd.DataFrame({
            "Value": freq.index,
            "Frequency": freq.values,
            "Percentage (%)": percent.values,
        })
        frequency_tables[col] = freq_table.round(2)

        # Descriptive Statistics (Mean, Median, Mode, SD, Min, Max)
        if pd.api.types.is_numeric_dtype(data):
            summary.append({
                "Variable": col,
                "Mean": round(data.mean(), 2),
                "Median": round(data.median(), 2),
                "Mode": data.mode().iloc[0] if not data.mode().empty else None,
                "Standard Deviation": round(data.std(ddof=1), 2),
                "Minimum": data.min(),
                "Maximum": data.max(),
            })
        else:
            summary.append({
                "Variable": col,
                "Mean": "N/A",
                "Median": "N/A",
                "Mode": data.mode().iloc[0] if not data.mode().empty else None,
                "Standard Deviation": "N/A",
                "Minimum": "N/A",
                "Maximum": "N/A",
            })

    summary_df = pd.DataFrame(summary)


class StatisticalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Lifestyle Analytics - Statistical Tool")
        self.root.geometry("950x650")

        # Title
        title_label = tk.Label(
            root,
            text="Student Lifestyle Analytics - Statistical Tool",
            font=("Arial", 16, "bold"),
            pady=10,
        )
        title_label.pack()

        # Button Row
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="1. ALL FDT TABLES",
            bg="#007bff",
            fg="white",
            width=20,
            command=lambda: self.start_task("freq"),
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            btn_frame,
            text="2. Choose FDT",
            bg="#ffc107",
            fg="black",
            width=20,
            command=lambda: self.start_task("choose_fdt"),
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            btn_frame,
            text="3. Mean, SD, Min, Max",
            bg="#28a745",
            fg="white",
            width=22,
            command=lambda: self.start_task("stats"),
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            btn_frame,
            text="4. Run Both FDT & Stats",
            bg="#6c757d",
            fg="white",
            width=24,
            command=lambda: self.start_task("both"),
        ).grid(row=0, column=3, padx=5)

        # Dynamic Sub-bar for "Choose FDT" dropdown
        self.dropdown_frame = tk.Frame(root)
        self.dropdown_frame.pack(pady=5)

        # Output Text Area (Monospace font keeps tables aligned)
        self.output_box = scrolledtext.ScrolledText(
            root, wrap=tk.NONE, font=("Consolas", 10), padx=10, pady=10
        )
        self.output_box.pack(expand=True, fill="both", padx=15, pady=10)

        # Horizontal Scrollbar for wide tables
        h_scroll = tk.Scrollbar(
            root, orient="horizontal", command=self.output_box.xview
        )
        h_scroll.pack(fill="x", padx=15)
        self.output_box.configure(xscrollcommand=h_scroll.set)

    def log(self, text, clear=False):
        if clear:
            self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)

    def clear_dropdown_bar(self):
        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()

    def start_task(self, choice):
        self.clear_dropdown_bar()
        self.log("Loading data from Google Sheets, please wait...\n", clear=True)
        # Run in a background thread so the UI doesn't freeze while downloading
        threading.Thread(
            target=self.run_analysis, args=(choice,), daemon=True
        ).start()

    def run_analysis(self, choice):
        try:
            if summary_df is None:
                load_and_process_data()

            self.root.after(0, lambda: self.process_choice(choice))

        except Exception as e:
            self.root.after(
                0, lambda: self.log(f"Error occurred:\n{str(e)}", clear=True)
            )

    def process_choice(self, choice):
        self.log("", clear=True)

        if choice == "freq":
            self.log("=== ALL FREQUENCY TABLES ===\n")
            for col, table in frequency_tables.items():
                self.log(f"\nFREQUENCY TABLE: {col}")
                self.log(table.to_string(index=False))
                self.log("-" * 40)

            output_file = "SC22_Frequency_Distribution_Results.xlsx"
            with pd.ExcelWriter(output_file) as writer:
                for col, table in frequency_tables.items():
                    table.to_excel(
                        writer, sheet_name=self.clean_sheet_name(col), index=False
                    )
            self.log(f"\n[Success] Saved as {output_file}")

        elif choice == "choose_fdt":
            self.log("Select a column from the dropdown above and click 'Load Table'.")
            available_cols = list(frequency_tables.keys())

            tk.Label(
                self.dropdown_frame, text="Choose Variable/Column:"
            ).pack(side=tk.LEFT, padx=5)
            col_var = tk.StringVar(value=available_cols[0])
            dropdown = ttk.Combobox(
                self.dropdown_frame,
                textvariable=col_var,
                values=available_cols,
                state="readonly",
                width=45,
            )
            dropdown.pack(side=tk.LEFT, padx=5)

            def on_confirm_click():
                chosen_col = col_var.get()
                table = frequency_tables[chosen_col]
                self.log(
                    f"=== FREQUENCY TABLE FOR: {chosen_col} ===\n", clear=True
                )
                self.log(table.to_string(index=False))

                safe_name = "".join(
                    c if c.isalnum() or c in (" ", "_") else "_"
                    for c in chosen_col[:20]
                )
                output_file = f"FDT_{safe_name}.xlsx"
                with pd.ExcelWriter(output_file) as writer:
                    table.to_excel(
                        writer,
                        sheet_name=self.clean_sheet_name(chosen_col),
                        index=False,
                    )
                self.log(f"\n\n[Success] Saved as {output_file}")

            tk.Button(
                self.dropdown_frame,
                text="Load Table",
                bg="#ffc107",
                command=on_confirm_click,
            ).pack(side=tk.LEFT, padx=5)

        elif choice == "stats":
            self.log("=== DESCRIPTIVE STATISTICS (Mean, SD, Min, Max) ===\n")
            self.log(summary_df.to_string(index=False))

            output_file = "Descriptive_Statistics_Results.xlsx"
            with pd.ExcelWriter(output_file) as writer:
                summary_df.to_excel(
                    writer, sheet_name="Descriptive Statistics", index=False
                )
            self.log(f"\n[Success] Saved as {output_file}")

        elif choice == "both":
            self.log("=== DESCRIPTIVE STATISTICS ===\n")
            self.log(summary_df.to_string(index=False))
            self.log("\n" + "=" * 50 + "\n")
            self.log("=== ALL FDT TABLES ===\n")
            for col, table in frequency_tables.items():
                self.log(f"\nFREQUENCY TABLE: {col}")
                self.log(table.to_string(index=False))
                self.log("-" * 40)

            output_file = "Statistical_Results.xlsx"
            with pd.ExcelWriter(output_file) as writer:
                summary_df.to_excel(
                    writer, sheet_name="Descriptive Statistics", index=False
                )
                for col, table in frequency_tables.items():
                    table.to_excel(
                        writer, sheet_name=self.clean_sheet_name(col), index=False
                    )
            self.log(f"\n[Success] Saved as {output_file}")

    @staticmethod
    def clean_sheet_name(name):
        # Excel forbids characters like \ / ? * [ ] : in sheet names
        invalid = r"\/?*[] :"
        cleaned = "".join("_" if c in invalid else c for c in name)
        return cleaned[:31]


if __name__ == "__main__":
    root = tk.Tk()
    app = StatisticalApp(root)
    root.mainloop()
