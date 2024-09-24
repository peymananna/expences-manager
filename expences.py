import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
from datetime import datetime

# نام فایل
file_name = "expenses.csv"

# بررسی وجود فایل CSV
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
    df.to_csv(file_name, index=False)

# افزودن هزینه
def add_expense():
    try:
        date = entry_date.get()
        category = entry_category.get()
        amount = float(entry_amount.get())
        description = entry_description.get()

        # اعتبارسنجی فرمت تاریخ
        datetime.strptime(date, "%Y-%m-%d")

        df = pd.read_csv(file_name)

        # استفاده از pd.concat برای افزودن داده‌ها
        new_row = pd.DataFrame([{'Date': date, 'Category': category, 'Amount': amount, 'Description': description}])
        df = pd.concat([df, new_row], ignore_index=True)

        df.to_csv(file_name, index=False)

        messagebox.showinfo("Success", "Expense added successfully!")
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Check amount and date format (YYYY-MM-DD).")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add expense: {e}")

# حذف هزینه
def delete_expense():
    try:
        description = entry_description.get()
        df = pd.read_csv(file_name)
        initial_length = len(df)
        df = df[df['Description'] != description]
        if len(df) < initial_length:
            df.to_csv(file_name, index=False)
            messagebox.showinfo("Success", "Expense deleted successfully!")
        else:
            messagebox.showinfo("Info", "No expense found with that description.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete expense: {e}")

# محاسبه کل هزینه
def total_expense():
    category = entry_category.get()
    try:
        df = pd.read_csv(file_name)
        total = df[df['Category'] == category]['Amount'].sum()
        messagebox.showinfo("Total Expense", f"Total expense for category '{category}' is: {total}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate total: {e}")

# لیست هزینه‌ها بر اساس تاریخ
def list_expenses_by_date():
    date = entry_date.get()
    try:
        df = pd.read_csv(file_name)
        expenses = df[df['Date'] == date]
        if not expenses.empty:
            result = expenses.to_string(index=False)
            messagebox.showinfo("Expenses", result)
        else:
            messagebox.showinfo("Info", "No expenses found for the specified date.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list expenses: {e}")

# تولید گزارش
def generate_report():
    period = combo_report_period.get()
    try:
        df = pd.read_csv(file_name)
        if period == 'Monthly':
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[df['Date'].dt.month == datetime.now().month]
        elif period == 'Yearly':
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[df['Date'].dt.year == datetime.now().year]

        report = df.groupby('Category')['Amount'].sum().to_string()
        messagebox.showinfo("Report", report)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {e}")

# پاک کردن ورودی‌ها
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_description.delete(0, tk.END)

# رابط کاربری
root = tk.Tk()
root.title("Expense Manager")

# بخش ورودی‌ها
frame_inputs = ttk.Frame(root)
frame_inputs.pack(pady=10)

ttk.Label(frame_inputs, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
entry_date = ttk.Entry(frame_inputs)
entry_date.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Category:").grid(row=1, column=0, padx=5, pady=5)
entry_category = ttk.Entry(frame_inputs)
entry_category.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame_inputs)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Description:").grid(row=3, column=0, padx=5, pady=5)
entry_description = ttk.Entry(frame_inputs)
entry_description.grid(row=3, column=1, padx=5, pady=5)

# دکمه‌ها
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="Add Expense", command=add_expense).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(frame_buttons, text="Delete Expense", command=delete_expense).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(frame_buttons, text="Total Expense", command=total_expense).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(frame_buttons, text="List by Date", command=list_expenses_by_date).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame_buttons, text="Generate Report", command=generate_report).grid(row=1, column=1, padx=5, pady=5)

# گزارش‌ها
combo_report_period = ttk.Combobox(frame_buttons, values=['Monthly', 'Yearly'], state="readonly")
combo_report_period.grid(row=1, column=2, padx=5, pady=5)
combo_report_period.current(0)

root.mainloop()