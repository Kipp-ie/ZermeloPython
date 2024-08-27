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
        end_unix = ""
        start_unix = ""
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
        def onDateChange(e):
            year = e.control.value.strftime('%Y')
            month = e.control.value.strftime('%m')
            day = e.control.value.strftime('%d')
            start_unix = time.mktime(datetime.datetime(int(year), int(month), int(day), 0, 0).timetuple())
            end_unix = time.mktime(datetime.datetime(int(year), int(month), int(day), 23, 59).timetuple())
            page.clean()
            scheduleurl = "{}/v3/appointments/".format(school_url)
            scheduleparams = {"access_token": open("token.txt", 'r'), "start": int(start_unix), "end": int(end_unix),
                              "user": "~me"}
            schedule = requests.get(url=scheduleurl, params=scheduleparams)
            scheduleresponse = schedule.json()["response"]
            print(scheduleresponse)
            scheduledata = scheduleresponse["data"]
            userName = ft.Container(
                content=ft.Text("Logged in as " + userjson[0]["firstName"]),
                alignment=ft.alignment.center,
                width=300,
                height=50,
                bgcolor=ft.colors.RED,
                border_radius=ft.border_radius.all(5),
            )

            page.add(
                ft.Row(
                    [
                        userName
                    ],
                    alignment=MainAxisAlignment.CENTER

                )


            )

            for i in range(1, scheduleresponse["totalRows"] + 1):
                containerName = ft.Container(
                    content=ft.Text(str(scheduledata[-i]["teachers"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["subjects"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["locations"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["startTimeSlotName"]).replace('[','').replace(']','').replace('\'','').replace('\"','')),
                    alignment=ft.alignment.center,
                    width=200,
                    height=50,
                    bgcolor=ft.colors.RED_ACCENT,
                    border_radius=ft.border_radius.all(5),
                )
                page.add(
                    ft.Row(
                        [
                            containerName
                        ],
                        alignment=MainAxisAlignment.CENTER
                    )

                )
            planningDateButton2 = ft.ElevatedButton(
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
            page.add(
                ft.Row(
                    [
                        planningDateButton2
                    ],
                    alignment=MainAxisAlignment.CENTER
                )
            )





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


                ],
                alignment=MainAxisAlignment.CENTER

            )
        )



    else:

        def on_login2(e):

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

            def onDateChange(e):
                year = e.control.value.strftime('%Y')
                month = e.control.value.strftime('%m')
                day = e.control.value.strftime('%d')
                start_unix = time.mktime(datetime.datetime(int(year), int(month), int(day), 0, 0).timetuple())
                end_unix = time.mktime(datetime.datetime(int(year), int(month), int(day), 23, 59).timetuple())
                page.clean()
                scheduleurl = "{}/v3/appointments/".format(school_url)
                scheduleparams = {"access_token": open("token.txt", 'r'), "start": int(start_unix),
                                  "end": int(end_unix),
                                  "user": "~me"}
                schedule = requests.get(url=scheduleurl, params=scheduleparams)
                scheduleresponse = schedule.json()["response"]
                print(scheduleresponse)
                scheduledata = scheduleresponse["data"]
                userName = ft.Container(
                    content=ft.Text("Logged in as " + userjson[0]["firstName"]),
                    alignment=ft.alignment.center,
                    width=300,
                    height=50,
                    bgcolor=ft.colors.RED,
                    border_radius=ft.border_radius.all(5),
                )

                page.add(
                    ft.Row(
                        [
                            userName
                        ],
                        alignment=MainAxisAlignment.CENTER

                    )

                )

                for i in range(0, scheduleresponse["totalRows"]):
                    containerName = ft.Container(
                        content=ft.Text(str(scheduledata[-i]["teachers"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["subjects"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["locations"]).replace('[','').replace(']','').replace('\'','').replace('\"','') + " - " + str(scheduledata[-i]["startTimeSlotName"]).replace('[','').replace(']','').replace('\'','').replace('\"','')),
                        alignment=ft.alignment.center,
                        width=200,
                        height=50,
                        bgcolor=ft.colors.RED_ACCENT,
                        border_radius=ft.border_radius.all(5),
                    )
                    page.add(
                        ft.Row(
                            [
                                containerName
                            ],
                            alignment=MainAxisAlignment.CENTER
                        )

                    )
                planningDateButton2 = ft.ElevatedButton(
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
                page.add(
                    ft.Row(
                        [
                            planningDateButton2
                        ],
                        alignment=MainAxisAlignment.CENTER
                    )
                )

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

                    ],
                    alignment=MainAxisAlignment.CENTER

                )
            )


        loginbutton = ft.FilledButton("Log-In", icon="login", on_click=on_login2, style=ft.ButtonStyle(
        bgcolor=ft.colors.RED
        ))
        page.add(
            ft.Row(
            [
                    key,
                    loginbutton

                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )



ft.app(main)