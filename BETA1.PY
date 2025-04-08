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
    
    def add_expense(e):
        if name_input.value and amount_input.value:
            expenses.append({"name": name_input.value, "amount": amount_input.value})
            name_input.value = ""
            amount_input.value = ""
            update_expenses()
    
    def delete_expense(exp):
        expenses.remove(exp)
        update_expenses()
    
    name_input = ft.TextField(label="Expense Name", expand=1)
    amount_input = ft.TextField(label="Amount", expand=1, keyboard_type=ft.KeyboardType.NUMBER)
    add_button = ft.ElevatedButton("Add", on_click=add_expense)
    
    page.add(
        ft.Column([
            total_expense,
            ft.Row([name_input, amount_input, add_button]),
            expense_list
        ])
    )

ft.app(target=main)