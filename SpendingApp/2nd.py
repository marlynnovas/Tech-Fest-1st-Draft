import flet as ft
import datetime
import json
import os

# Data
expenses = []
selected_month = "All"
months = ["All", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
DATA_FILE = "expenses.json"


# Functions
def save_expenses():
    with open(DATA_FILE, "w") as f:
        json.dump([
            {
                "title": e["title"],
                "amount": e["amount",]
                "category": e["category"],
                "date":e["date"].strftime('%Y-%m-%d')
            } for e in expenses
        ], f)
        
        
        (expenses, f, default=str)


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data:
                expenses.append({
                    "title": item["title"],
                    "amount": item["amount"],
                    "category": item["category"],
                    "date": datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
                })


def main(page: ft.Page):
    page.title = "Expense Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    load_expenses()

    title = ft.Text("Expense Tracker", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)

    dropdown = ft.Dropdown(
        label="Filter by Month",
        options=[ft.dropdown.Option(month) for month in months],
        value="All",
        on_change=lambda e: [refresh_ui(), update_pie_chart()]
    )

    amount_input = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER)
    title_input = ft.TextField(label="Title", width=160)
    category_input = ft.TextField(label="Category", width=140)
    date_picker = ft.DatePicker(
        first_date=datetime.date(2023, 1, 1),
        last_date=datetime.date.today()
    )
    page.overlay.append(date_picker)

    pie_chart = ft.PieChart(
        sections=[],
        sections_space=2,
        center_space_radius=40,
        expand=True
    )

    total_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER)
    expense_list = ft.Column()
    category_bars = ft.Column()

    def refresh_ui():
        total = 0
        expense_list.controls.clear()
        category_totals = {}

        for idx, exp in enumerate(expenses):
            exp_date = exp["date"]
            if selected_month != "All" and exp_date.strftime("%B") != selected_month:
                continue
            total += float(exp["amount"])
            category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + float(exp["amount"])

            expense_list.controls.append(
                ft.Row([
                    ft.Text(f"{exp['title']} - ${exp['amount']} - {exp['category']} - {exp['date']}"),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=idx: delete_expense(i))
                ])
            )
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def update_pie_chart():
        pie_chart.sections.clear()
        category_totals = {}

        for exp in expenses:
            exp_date = exp["date"]
            if selected_month != "All" and exp_date.strftime("%B") != selected_month:
                continue
            category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + float(exp["amount"])

        total = sum(category_totals.values())
        if total > 0:
            for category, amount in category_totals.items():
                pie_chart.sections.append(
                    ft.PieChartSection(
                        value=amount,
                        title=category,
                        title_style=ft.TextStyle(size=12),
                        color=None
                    )
                )
        page.update()

    def add_expense(e):
        if not amount_input.value or not title_input.value or not category_input.value or not date_picker.value:
            return

        expenses.append({
            "title": title_input.value,
            "amount": float(amount_input.value),
            "category": category_input.value,
            "date": date_picker.value
        })

        save_expenses()
        amount_input.value= title_input.value= category_input.value= ""
        refresh_ui()
        update_pie_chart()

        title_input.value = ""
        amount_input.value = ""
        category_input.value = ""
        page.update()

    def delete_expense(index):
        if 0 <= index < len(expenses):
            del expenses[index]
            save_expenses()
            refresh_ui()
            update_pie_chart()

    add_button = ft.ElevatedButton("+ Add", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)) on_click=add_expense)

    input_row = ft.ResponsiveRow([
        title_input,
        amount_input,
        category_input,
        ft.ElevatedButton("Pick Date", on_click=lambda _: date_picker.pick_date()),
        add_button
    ], spacing=10, run_spacing=10)

    Total_text= ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=ft.color.AMBER)
    expense_list=ft.Column()
    category_bars=Column()

    def refresh_ui():
        month=dropdown.valuefiltered=[]
        total= 0
        chart_data= defau;tdict(float)
        for odx, exp in enumarate (expenses):
                exp_month= ecp[ date ]. strftime('%B')
                of month=="All or exp_month==month:"
                filtered.append((idx, exp))
                total+=exp["amount"]
                chart_data[exp["Category"]]+= exp["aAmount"]
        Category_bars.controls.clear()
        for cat, amount in chart_data.items():
                percent= (amount/total) if total else 0
                category_bars.controls.append()
                    ft.Column([
                        ft.Text(f"{cat}-{amount:.2f}" ({percent*100:.1f}%)"),"
                        "ft.ProgressBar(value=percent, color=ft.colors.LIGHT_BLUE)")
                    ])
                
            )
        
        expense_list.controls.clear()
        for idx, exp in filtered:
                card=ft.Card(
                     ft.Container(
                          ft.Row([
                                ft.Column([
                                        ft.Text["title"], weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                        ft.Text(f"{exp['amount']}\ {exp['category']} | {exp['date'].strftime('%d %b %Y')}", color=ft.colors.GREY).
                                        }, spacing=5),
                                        ft.IconButton(ft.icons>DELETE, on click=lamdba e, i=idx: delete_expense(i), icon_color=ft.colors.RED_ACCENT)
                                        aligment=ft.Mainaxisaligment.SPACE_Between),
                                        padding=15
                                                      )
                                ])
                          ])
                     ),
                eelecvation3
                color=ft.colors.with_opacity(0,1 ft.colors.WHITE),
                Shape=ft.RoundedRectangularBorder(radius=10)

                )
                expense_list. controls.appnd(card)


                total_text.value= f"Total for {month}: {total:.2f}"
                page.update




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
#refresh_ui()
#update_pie_chart()
ft.app(target=main)

