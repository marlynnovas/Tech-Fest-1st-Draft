import flet as ft
import json
import os
from datetime import datetime

expenses = []
DATA_FILE = "expenses.json"

CATEGORY_COLORS = {
    "Food": ft.colors.GREEN,
    "Transport": ft.colors.BLUE,
    "Shopping": ft.colors.PURPLE,
    "Utilities": ft.colors.ORANGE,
    "Health": ft.colors.RED,
    "Entertainment": ft.colors.PINK,
    "Other": ft.colors.GREY
}

INCOME = 20000  
EXPENSE_LIMIT_PERCENTAGE = 0.5  

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f)

def load_expenses():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                expenses.extend(data)
        except Exception as e:
            print("Error loading data:", e)

def main(page: ft.Page):
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

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

    # Campo de texto para categoría personalizada, por defecto oculto
    other_category_input = ft.TextField(label="Other Category", width=140, visible=False)

    date_input = ft.TextField(label="Date (YYYY-MM-DD)", width=140)

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)
    expense_list = ft.Column()
    charts_column = ft.Column()
    warning_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.RED)

    def refresh_ui():
        total = sum(exp["amount"] for exp in expenses)
        total_text.value = f"Total: RD${total:.2f}"

        # Comparar gasto total con el límite del ingreso
        if total > INCOME * EXPENSE_LIMIT_PERCENTAGE:
            warning_text.value = "⚠️ You're spending too much! Consider cutting back!"
            warning_text.color = ft.colors.RED
        else:
            warning_text.value = ""

        expense_list.controls.clear()
        charts_column.controls.clear()

        sorted_exp = sorted(expenses, key=lambda x: x["date"], reverse=True)

        for idx, exp in enumerate(sorted_exp):
            badge_color = CATEGORY_COLORS.get(exp["category"], ft.colors.GREY)

            badge = ft.Container(
                content=ft.Text(exp["category"], color="white", size=10, weight=ft.FontWeight.BOLD),
                bgcolor=badge_color,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
                border_radius=ft.border_radius.all(10)
            )

            card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(f"US${exp['amount']} | {exp['date']}", color=ft.colors.GREY_400)
                        ], spacing=5),
                        ft.Row([
                            badge,
                            ft.IconButton(ft.icons.DELETE, on_click=lambda e, i=idx: delete_expense(i), icon_color=ft.colors.RED_ACCENT)
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=15
                ),
                elevation=3,
                color=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                shape=ft.RoundedRectangleBorder(radius=10)
            )
            expense_list.controls.append(card)

        if expenses:
            category_totals = {}
            for exp in expenses:
                category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + exp["amount"]

            total_amount = sum(category_totals.values()) or 1  # evitar división por cero

            charts_column.controls.append(ft.Text("📊 Expenses by Category", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN))
            for category, amount in category_totals.items():
                percent = (amount / total_amount) * 100
                bar = ft.ProgressBar(value=percent / 100, bgcolor=ft.colors.with_opacity(0.1, "white"), color=CATEGORY_COLORS.get(category, ft.colors.GREY), width=300)
                charts_column.controls.append(
                    ft.Column([
                        ft.Text(f"{category}: US${amount:.2f} ({percent:.1f}%)", size=12),
                        bar
                    ], spacing=4)
                )

        page.update()

    def add_expense(e):
        if not amount_input.value or not title_input.value or not category_input.value or not date_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Fill all required fields!", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        try:
            amount = float(amount_input.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("💵 Invalid amount!", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        expense_date = date_input.value  # Usamos la fecha del campo de texto

        category = category_input.value
        if category == "Other" and other_category_input.value:
            category = other_category_input.value

        expenses.append({
            "title": title_input.value,
            "amount": amount,
            "category": category,
            "date": expense_date
        })
        save_expenses()
        amount_input.value = title_input.value = ""
        category_input.value = None
        other_category_input.value = ""
        date_input.value = ""

        page.snack_bar = ft.SnackBar(ft.Text("✅ Expense added!", color="white"), bgcolor="green")
        page.snack_bar.open = True
        refresh_ui()

    def delete_expense(index):
        expenses.pop(index)
        save_expenses()
        refresh_ui()

    def clear_all_expenses(e):
        expenses.clear()
        save_expenses()
        refresh_ui()
        page.snack_bar = ft.SnackBar(ft.Text("🧹 All expenses cleared!", color="white"), bgcolor="orange")
        page.snack_bar.open = True

    # Mostrar campo de texto solo si la categoría es "Other"
    def on_category_change(e):
        other_category_input.visible = category_input.value == "Other"
        page.update()

    category_input.on_change = on_category_change

    add_button = ft.ElevatedButton("➕ Add", on_click=add_expense, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
    clear_button = ft.TextButton("🗑️ Clear All", on_click=clear_all_expenses, style=ft.ButtonStyle(color=ft.colors.RED_300))

    input_row = ft.Row([
        title_input,
        amount_input,
        category_input,
        other_category_input,
        date_input,
        add_button
    ], spacing=10)

    page.add(
        ft.Column([
            title,
            input_row,
            ft.Row([total_text, clear_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            warning_text, 
            ft.Divider(),
            ft.Container(content=expense_list, padding=10),
            ft.Divider(),
            charts_column
        ])
    )

    refresh_ui()

ft.app(target=main)
