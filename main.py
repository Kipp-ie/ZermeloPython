import flet as ft
import requests
from zermelo import Client

cl = Client("citadelcollege")
def main(page: ft.Page):
    page.title = "ZermeloPython"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    key = ft.TextField(label="Zermelo API Key", icon="key")
    school_url="https://citadelcollege.zportal.nl/api"

    def on_login(e):
        url = "{}/v3/oauth/token".format(school_url)
        data = {
            "grant_type": "authorization_code",
            "code": key.value
        }
        res = requests.post(url=url, data=data)
        print(res.json())

        access_token = res.json()["access_token"]

        print(access_token)

        url = "{}/v3/users/~me".format(school_url)
        params = {"access_token": access_token}
        urlresponse = requests.get(url=url, params=params)
        userjson = urlresponse.json()["response"]["data"]
        print(userjson["firstName"])




    page.add(
        ft.Row(
            [
                key,
                ft.FilledButton("Log-In", icon="login", on_click=on_login)

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)