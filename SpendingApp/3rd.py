import flet as ft
import datetime
import json
import os
from collections import defaultdict

#Pechurina con papa

expenses = []
selected_month = "All"
months = ["All", "January", "February", "March","April","May","June","July","August","September","October","November","December"]
DATA_FILE = "expenses.json"

def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump([
            {
                "title": e["title"],
                "amount": e["amount"],
                "category": e["category"],
                "date": e["date"].strftime('%Y-%m-%d')
            } for e in expenses
        ], f)

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                expenses.append({
                    "title": item["title"],
                    "amount": item["amount"],
                    "category": item["category"],
                    "date": datetime.datetime.strptime(item["date"], '%Y-%m-%d').date()
                })

def main(page: ft.Page):
    page.title = "💸 Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

    title = ft.Text("💰 Expense Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN)

    selected_date = ft.TextField(label="Selected Date", read_only=True, width=140)

    dropdown = ft.Dropdown(
        label="Filter by Month",
        options=[ft.dropdown.Option(month) for month in months],
        value="All",
        on_change=lambda e: [refresh_ui(), update_pie_chart()]
    )

    amount_input = ft.TextField(label="Amount", keyboard_type="number", width=120)
    title_input = ft.TextField(label="Title", width=160)
    category_input = ft.TextField(label="Category", width=140)
    
    date_picker = ft.DatePicker(
        first_date=datetime.date(2023, 1, 1),
        last_date=datetime.date.today(),
        on_change=lambda e: selected_date_update()
    )
    page.overlay.append(date_picker)

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True
    )

    def selected_date_update():
        if date_picker.value:
            selected_date.value = date_picker.value
            page.update()

    def update_pie_chart():
        month = dropdown.value
        category_totals = defaultdict(float)

        for exp in expenses:
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                cat = exp["category"]
                amt = exp["amount"]
                category_totals[cat] += amt

        pie_chart.sections = [
            ft.PieChartSection(
                value=amt,
                title=f"{cat}\n₹{amt}",
                color=ft.colors.CYAN if i % 2 == 0 else ft.colors.TEAL
            )
            for i, (cat, amt) in enumerate(category_totals.items())
        ]

        pie_chart.update()

    def add_expense(e):
        if not amount_input.value or not title_input.value or not category_input.value or not selected_date.value:
            return

        expenses.append({
            "title": title_input.value,
            "amount": float(amount_input.value),
            "category": category_input.value,
            "date": datetime.datetime.strptime(selected_date.value, "%Y-%m-%d").date()
        })
        save_expenses()
        amount_input.value = ""
        title_input.value = ""
        category_input.value = ""
        selected_date.value = ""
        page.update()
        refresh_ui()
        update_pie_chart()

    def delete_expense(index):
        expenses.pop(index)
        save_expenses()
        refresh_ui()
        update_pie_chart()

    add_button = ft.ElevatedButton("➕ Add", on_click=add_expense, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)))
    
    input_row = ft.ResponsiveRow([
        title_input,
        amount_input,
        category_input,
        selected_date,
        ft.ElevatedButton("📅 Pick Date", on_click=lambda _: date_picker.pick_date()),
        add_button
    ], spacing=10, run_spacing=10)

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)
    expense_list = ft.Column()
    category_bars = ft.Column()

    def refresh_ui():
        month = dropdown.value
        filtered = []
        total = 0
        chart_data = defaultdict(float)
        for idx, exp in enumerate(expenses):
            exp_month = exp["date"].strftime('%B')
            if month == "All" or exp_month == month:
                filtered.append((idx, exp))
                total += exp["amount"]
                chart_data[exp["category"]] += exp["amount"]

        category_bars.controls.clear()
        for cat, amount in chart_data.items():
            percent = (amount / total) if total else 0
            category_bars.controls.append(
                ft.Column([
                    ft.Text(f"{cat} - ₹{amount:.2f} ({percent*100:.1f}%)"),
                    ft.ProgressBar(value=percent, color=ft.colors.LIGHT_BLUE_ACCENT)
                ])
            )

        expense_list.controls.clear()
        for idx, exp in filtered:
            card = ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(exp["title"], weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(f"₹{exp['amount']} | {exp['category']} | {exp['date'].strftime('%d %b %Y')}", color=ft.colors.GREY_400)
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

        total_text.value = f"Total for {month}: ₹{total:.2f}"
        page.update()

    # Final layout
    page.add(
        ft.Column([
            title,
            dropdown,
            input_row,
            total_text,
            ft.Container(content=pie_chart, width=400, height=400),
            ft.Divider(),
            category_bars,
            ft.Divider(),
            expense_list
        ])
    )

    refresh_ui()
    update_pie_chart()

ft.app(target=main)
