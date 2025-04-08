import flet as ft
class ExpenseApp(ft.container):
        def __init__(self,page: ft.Page):
            self.page= page
            self.bg_color="#88ddfb"
            self.page.bgcolor=self.bg_color
            self.blue_color= "88ddfb"
            self.container_color= "823243d"
            self.cotainer2_color = "484a66"

            self.header=ft.Container(
                height=50,
                content=ft.Row(
                    aligment=ft.MainAxisAligment.SPACE_AROUND,
                    controls=[
                            ft.IconButton(icon=ft.icons.ARROW_BACK_IOS,icon_color= "white"),
                            ft.Dropdown(
                                width=150,
                                hint_test="Este mes",
                                border_color=self.container2_color,
                                suffix_icon= ft.icons.KEYBOARD_ARROW_DOWN,
                                BGCOLOR= self.bg_color,
                                border_radius=10,
                                icon_enabled_color="transparent"
                                ),
                                Ft.Image(src="assets") 
                            ]
                    )
            )

            self.page.add(ft.Column(
                        expand = True,scroll="auto",
                        controls=[self.header]        
            ))

ft.app(target=ExpenseApp)
