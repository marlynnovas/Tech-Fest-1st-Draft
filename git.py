import flet as ft

def main(page: ft.Page):
    page.title = "Expense Tracker"
    page.window_width = 400
    page.window_height = 600
    page.padding = 20
    
    expenses = []
    total_expense = ft.Text(value="Total: $0", size=18, weight="bold")
    expense_list = ft.Column()
    
    def update_expenses():
        total = sum(float(exp["amount"]) for exp in expenses)
        total_expense.value = f"Total: ${total:.2f}"
        expense_list.controls.clear()
        for exp in expenses:
            expense_list.controls.append(
                ft.Row([
                    ft.Text(exp["name"], expand=1),
                    ft.Text(f"${exp["amount"]}", expand=1),
                    ft.IconButton(ft.icons.DELETE, on_click=lambda e, x=exp: delete_expense(x))
                ])
            )
        page.update()
    