import flet as ft
import json
import os
from datetime import datetime

#hola emireth

# Global Variables
expenses = []
DATA_FILE = "expenses.json"

# Save expenses to JSON
def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f)

# Load expenses from JSON
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            expenses.extend(data)

def main(page: ft.Page):
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

    # UI Components
    title = ft.Text("💰 My Transactions", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)

    amount_input = ft.TextField(label="Amount", keyboard_type="number", width=100)
    title_input = ft.TextField(label="Title", width=140)
    category_input = ft.Dropdown(
        label="Category",
        width=140,
        options=[
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("Shopping"),
            ft.dropdown.Option("Utilities"),
            ft.dropdown.Option("Health"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Other")
        ]
    )
    date_input = ft.TextField(
        label="Date (YYYY-MM-DD)",
        width=130,
        hint_text=datetime.now().strftime("%Y-%m-%d")  # Show today's date as hint
    )

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)
    expense_list = ft.Column()

    # Add expense
    def add_expense(e):
        if not amount_input.value or not title_input.value or not category_input.value:
            return
        
        expense_date = date_input.value.strip()
        if not expense_date:
            expense_date = datetime.now().strftime("%Y-%m-%d")  # Default to today

        expenses.append({
            "title": title_input.value,
            "amount": float(amount_input.value),
            "category": category_input.value,
            "date": expense_date
        })
        save_expenses()
        amount_input.value = title_input.value = ""
        category_input.value = None
        date_input.value = ""
        refresh_ui()

    # Delete expense
    def delete_expense(index):
        expenses.pop(index)
        save_expenses()
        refresh_ui()

    add_button = ft.ElevatedButton(
        "➕ Add",
        on_click=add_expense,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
    )

    input_row = ft.Row([
        title_input,
        amount_input,
        category_input,
        date_input,
        add_button
    ], spacing=10)

    # Refresh UI
    def refresh_ui():
        total = sum(exp["amount"] for exp in expenses)
        expense_list.controls.clear()
        for idx, exp in enumerate(expenses):
            card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(f"US${exp['amount']} | {exp['category']} | {exp['date']}", color=ft.colors.GREY_400)
                        ], spacing=5),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=idx: delete_expense(i), icon_color=ft.colors.RED_ACCENT)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=15
                ),
                elevation=3,
                color=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=10)
            )
            expense_list.controls.append(card)

        total_text.value = f"Total: US${total:.2f}"
        page.update()

    page.add(
        ft.Column([
            title,
            input_row,
            total_text,
            ft.Divider(),
            expense_list
        ])
    )

    refresh_ui()

ft.app(target=main)
