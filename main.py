import flet as ft
import requests
from flet_core import MainAxisAlignment
import datetime
import time



def main(page: ft.Page):
    page.title = "ZermeloPython"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    key = ft.TextField(label="Zermelo API Key", icon="key")
    school_url="https://citadelcollege.zportal.nl/api"


    if open("token.txt", 'r').read(1):
        url = "{}/v3/users/~me".format(school_url)
        params = {"access_token": open("token.txt", 'r')}
        urlresponse = requests.get(url=url, params=params)
        userjson = urlresponse.json()["response"]["data"]

        page.clean()

        userName = ft.Container(
            content=ft.Text("Welcome " + userjson[0]["firstName"]),
            alignment=ft.alignment.center,
            width=200,
            height=50,
            bgcolor=ft.colors.RED,
            border_radius=ft.border_radius.all(5),
        )
        agendaInfo = ft.Container(
            content=ft.Text("Use the date selectors to get the planning from that date."),
            alignment=ft.alignment.center,
            width=200,
            height=50,
            bgcolor=ft.colors.RED,
            border_radius=ft.border_radius.all(5),
        )
        planningDateButton = ft.ElevatedButton(
            "Pick date:",
            icon=ft.icons.CALENDAR_MONTH,
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=10, day=1),
                    last_date=datetime.datetime(year=2024, month=10, day=1),
                    on_change=onDateChange,
                )
            )
        )
        planningDate = ""
        def onDateChange(e):
            planningDate1 = e.control.value.strftime('%Y, %m, %d, %H, %M')
            planningDate = datetime.datetime(int(planningDate1))


        def onsubmit(e):
            page.clean()
            scheduleurl = "{}/v3/appointments/".format(school_url)
            scheduleparams = {"access_token": open("token.txt", 'r'), "start": time.mktime(planningDate.timetuple())}
            scheduleresponse = requests.get(url=scheduleurl, params=scheduleparams)
            print(scheduleresponse.json())



        page.add(
            ft.Row(
                [
                    userName,
                    agendaInfo,
                    planningDateButton
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    ft.FilledButton("Fetch Data", icon="login", on_click=onsubmit, style=ft.ButtonStyle(
                bgcolor=ft.colors.RED, color=ft.colors.WHITE,
            ))

                ],
                alignment=MainAxisAlignment.CENTER

            )
        )



    else:
        def on_login(e):
            url = "{}/v3/oauth/token".format(school_url)
            data = {
            "grant_type": "authorization_code",
            "code": key.value
            }
            res = requests.post(url=url, data=data)
            print(res.json())

            access_token = res.json()["access_token"]

            file2write = open("token.txt", 'w')
            file2write.write(access_token)
            file2write.close()

            print(access_token)

            url = "{}/v3/users/~me".format(school_url)
            params = {"access_token": access_token}
            urlresponse = requests.get(url=url, params=params)
            userjson = urlresponse.json()["response"]["data"]

            page.clean()

            userName = ft.Container(
                content=ft.Text("Welcome " + userjson[0]["firstName"]),
                alignment=ft.alignment.center,
                width=200,
                height=50,
                bgcolor=ft.colors.RED,
                border_radius=ft.border_radius.all(5),
            )
            agendaInfo = ft.Container(
                content=ft.Text("Use the date selectors to get the planning from that date."),
                alignment=ft.alignment.center,
                width=200,
                height=50,
                bgcolor=ft.colors.RED,
                border_radius=ft.border_radius.all(5),
            )


            page.add(
                ft.Row(
                [
                    userName,
                    agendaInfo
                ]
            ))

        logintext = ft.Container(
            content=ft.Text("You only need to log in once, this app will store your token."),
            alignment=ft.alignment.center,
            width=300,
            height=50,
            bgcolor=ft.colors.RED,
            border_radius=ft.border_radius.all(5),
        )


        page.add(
            ft.Row(
                [
                    logintext,
                    ft.Column(spacing=5, controls=(key, ft.FilledButton("Log-In", icon="login", on_click=on_login)))


                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

ft.app(main)