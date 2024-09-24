from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import pandas as pd
import os
from datetime import datetime

# نام فایل CSV
file_name = "expenses.csv"

# ایجاد فایل CSV در صورت عدم وجود
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
    df.to_csv(file_name, index=False)

class ExpenseApp(App):
    def build(self):
        layout = GridLayout(cols=2, padding=10, spacing=10)

        # ورودی‌ها
        self.date_input = TextInput(hint_text='Date (YYYY-MM-DD)', size_hint=(0.8, None), height=50)
        layout.add_widget(Label(text="Date:"))
        layout.add_widget(self.date_input)

        self.category_input = TextInput(hint_text='Category', size_hint=(0.8, None), height=50)
        layout.add_widget(Label(text="Category:"))
        layout.add_widget(self.category_input)

        self.amount_input = TextInput(hint_text='Amount', size_hint=(0.8, None), height=50)
        layout.add_widget(Label(text="Amount:"))
        layout.add_widget(self.amount_input)

        self.description_input = TextInput(hint_text='Description', size_hint=(0.8, None), height=50)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.description_input)

        # دکمه‌ها
        add_button = Button(text="Add Expense", size_hint=(1, None), height=50)
        add_button.bind(on_press=self.add_expense)
        layout.add_widget(add_button)

        delete_button = Button(text="Delete Expense", size_hint=(1, None), height=50)
        delete_button.bind(on_press=self.delete_expense)
        layout.add_widget(delete_button)

        total_button = Button(text="Total Expense", size_hint=(1, None), height=50)
        total_button.bind(on_press=self.total_expense)
        layout.add_widget(total_button)

        list_button = Button(text="List by Date", size_hint=(1, None), height=50)
        list_button.bind(on_press=self.list_expenses_by_date)
        layout.add_widget(list_button)

        # گزارش‌ها
        self.report_spinner = Spinner(
            text='Monthly',
            values=('Monthly', 'Yearly'),
            size_hint=(1, None),
            height=50
        )
        layout.add_widget(self.report_spinner)

        report_button = Button(text="Generate Report", size_hint=(1, None), height=50)
        report_button.bind(on_press=self.generate_report)
        layout.add_widget(report_button)

        return layout

    def add_expense(self, instance):
        date = self.date_input.text
        category = self.category_input.text
        amount = self.amount_input.text
        description = self.description_input.text

        if not date or not category or not amount or not description:
            print("All fields are required!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            amount = float(amount)
        except ValueError:
            print("Invalid date or amount")
            return

        df = pd.read_csv(file_name)
        new_row = pd.DataFrame([{'Date': date, 'Category': category, 'Amount': amount, 'Description': description}])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_name, index=False)
        print("Expense added")

    def delete_expense(self, instance):
        description = self.description_input.text
        df = pd.read_csv(file_name)
        df = df[df['Description'] != description]
        df.to_csv(file_name, index=False)
        print("Expense deleted")

    def total_expense(self, instance):
        category = self.category_input.text
        try:
            df = pd.read_csv(file_name)
            total = df[df['Category'] == category]['Amount'].sum()
            print(f"Total expense for category '{category}' is: {total}")
        except Exception as e:
            print(f"Error calculating total: {e}")

    def list_expenses_by_date(self, instance):
        date = self.date_input.text
        try:
            df = pd.read_csv(file_name)
            expenses = df[df['Date'] == date]
            if not expenses.empty:
                print(expenses.to_string(index=False))
            else:
                print("No expenses found for the specified date.")
        except Exception as e:
            print(f"Error listing expenses: {e}")

    def generate_report(self, instance):
        period = self.report_spinner.text
        try:
            df = pd.read_csv(file_name)
            df['Date'] = pd.to_datetime(df['Date'])
            if period == 'Monthly':
                df = df[df['Date'].dt.month == datetime.now().month]
            elif period == 'Yearly':
                df = df[df['Date'].dt.year == datetime.now().year]
            report = df.groupby('Category')['Amount'].sum().to_string()
            print(report)
        except Exception as e:
            print(f"Error generating report: {e}")

if __name__ == '__main__':
    ExpenseApp().run()