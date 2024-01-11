from banners import BannerMsg
from datetime import datetime
import json

import flet
from flet import TextField, Text, Column, Row, Checkbox
from flet import Page, Container, Divider, ElevatedButton
from flet_core import Card, ScrollMode
import webbrowser
import requests

index_to_print = 0
dictionary = {}

URL = "https://robotlab-residualwood.onrender.com/"
URL_DEV = "http://localhost:5000/"
KEYS = ["length", "width", "height", "weight", "name", "source", "color", "storage_location", "paint", "type",
        "is_fire_treated", "is_straight", "is_planed", "image", "intake_location", "info"]

values = []
param = []


def print_label(): ...


def handle_post_request(p, e):
    global index_to_print
    global dictionary
    inserted_data = list(zip(KEYS, values))
    payload = {}
    endpoint = "/wood"
    headers = {"Content-Type": "application/json"}

    try:
        for item in inserted_data:
            if item[0] in ["length", "width", "height", "weight", "density"]:
                payload[item[0]] = float(item[1])
            else:
                payload[item[0]] = item[1]
    except ValueError:
        BannerMsg(p, "Please make sure the value types are correct", 'warning', e)

    payload["timestamp"] = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
    json_body = json.dumps(payload)

    response = requests.post(URL + endpoint, data=json_body, timeout=10, headers=headers)
    dictionary = response.json()
    index_to_print = response.json()['id']
    print(">>>>>>", json_body)
    return response.json(), response.status_code


def handle_delete_request():
    # TODO: Implement login

    payload = {}
    if param:
        for p in param:
            payload["id"] = p

    json_body = json.dumps(payload)
    # response = requests.delete(URL + "wood", data=json_body, headers={"Content-Type": "application/json"})
    # print(response.status_code)
    # return response.status_code


def main(page: Page):
    page.theme_mode = 'light'
    page.scroll = flet.ScrollMode.ALWAYS
    page.title = "Robot Lab Wood DB"
    page.description = "A simple tool to add data of waste wood into the database"
    page.window_width = 520
    page.window_height = 1200
    page.theme = flet.Theme(visual_density=flet.ThemeVisualDensity.COMPACT, use_material3=True,
                            color_scheme_seed="#4336f5")

    tab_status = "Insert Row"

    def __print_label__(e):
        global index_to_print
        if index_to_print == 0:
            BannerMsg(page, "The index to print is not specified. First insert the data to generate the Index.",
                      'error', e)
        else:
            BannerMsg(page, "Printing label...",
                      'message', e)
        index_to_print = 0

    def tab_changed(e):
        update_tab()

    def submit(e):
        error_status = False
        if len(values) > 0:
            values.clear()
        for f in widgets:
            if type(f) == flet.Card:
                continue
            if (
                    f.label == "Length *" and f.value == "" or
                    f.label == "Width *" and f.value == "" or
                    f.label == "Height *" and f.value == "" or
                    f.label == "Weight *" and f.value == "" or
                    f.label == "Density *" and f.value == "" or
                    f.label == "Color *" and f.value == "" or
                    f.label == "Source *" and f.value == ""
            ):
                error_msg(e)
                error_status = True
                break
            values.append(f.value)

        if error_status is False:
            handle_post_request(page, e)
            response = handle_post_request(page, e)
            if response[1] != 201:
                if response[1] == 400:
                    BannerMsg(page, f"Message: {response[0]['message']}", 'error', e)
                elif response[1] != 400:
                    BannerMsg(page, "Something went wrong - status code: {}".format(response[1]), 'error', e)
            else:
                BannerMsg(page, "Successfully saved to DB", 'message', e)

    def delete_row(e):
        ...

    # err = False
    # if len(param) > 0:
    #     param.clear()
    # for f in widgets:
    #     if f.label == "Wood ID *" and f.value == "":
    #         error_msg(e)
    #         err = True
    #         break
    #     elif f == wood_id_text_field:
    #         param.append(f.value)
    #         break
    # if err is False:
    #     resp = handle_delete_request()
    #     if resp != 200:
    #         if resp == 404:
    #             BannerMsg(page, "The entered ID does not exist - status code: {}".format(resp), 'error', e)
    #         elif resp != 404:
    #             BannerMsg(page, "Something went wrong - status code: {}".format(resp), 'error', e)
    #     else:
    #         BannerMsg(page, f"Successfully deleted the row with Wood ID: {param[-1]}", 'message', e)

    def go_to_api_docs(e):
        webbrowser.open("https://robotlab-residualwood.onrender.com/api-docs")

    def go_to_github_page(e):
        webbrowser.open("https://uva-hva.gitlab.host/robotlab/wood/cw4.0")

    # Widgets
    tabs = flet.Tabs(
        selected_index=0,
        tabs=[flet.Tab(text="Insert Row"),
              # flet.Tab(text="Delete Row"),
              # flet.Tab(text="Modify Row")
              ],
        on_change=tab_changed
    )
    length_text_field = TextField(
        label="Length *",
        tooltip="Length of the wood in mm",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5",
        keyboard_type=flet.KeyboardType.NUMBER
    )
    width_text_field = TextField(
        label="Width *",
        tooltip="Width of the wood in mm",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    height_text_field = TextField(
        label="Height *",
        tooltip="Height of the wood in mm",
        width=200
        , height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    weight_text_field = TextField(
        label="Weight *",
        tooltip="Weight of the wood in kg",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    wood_species_field = TextField(
        label="Species",
        tooltip="Species and process of the wood e.g. Red Oak FSC ",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    label_field = TextField(
        label="Source location",
        tooltip="Label of the material from specific project", width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    color_text_field = TextField(
        label="Color *",
        tooltip="Color of the wood in (RGB) e.g. '120, 130, 90'",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    storage_location_text_field = TextField(
        label="Storage Location",
        tooltip="A reference to where the wood is stored in the physical storage",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    wood_id_text_field = TextField(
        label="Wood ID *",
        tooltip="ID of the wood e.g. in the 7 digits format of '00000001'",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )

    type_text_field = TextField(
        label="Wood type",
        width=200,
        height=40,
        tooltip="Wood type e.g. hardwood or softwood",
        border_color="#4336f5",
        color="#4336f5"
    )

    is_fire_treated_checkbox = Checkbox(label="Fire treated")
    is_straight_checkbox = Checkbox(label="Straight", value=True)
    is_planned_checkbox = Checkbox(label="Planed", value=True)

    image_path_field = TextField(
        label="Image path",
        tooltip="Path to where image is stored",
        width=412,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )
    source_path_field = TextField(
        label="Intake location *",
        tooltip="Location where the wood was in-taken",
        width=200,
        height=40,
        border_color="#4336f5",
        color="#4336f5"
    )

    info_path_field = TextField(width=410, label="Info", multiline=True, border_color="#4336f5", color="#4336f5")
    insert_btn = ElevatedButton(text="Insert", on_click=submit, bgcolor="#4336f5", color="white")
    delete_btn = ElevatedButton(text="Delete", on_click=delete_row, bgcolor="#4336f5", color="white")
    print_label_btn = ElevatedButton(text="Print Label", on_click=__print_label__, bgcolor="#9891F6", color="white")

    action_buttons = [insert_btn, delete_btn, print_label_btn]

    widgets = [
        length_text_field,
        width_text_field,
        height_text_field,
        weight_text_field,
        wood_species_field,
        label_field,
        color_text_field,
        storage_location_text_field,
        wood_id_text_field,
        type_text_field,
        is_fire_treated_checkbox,
        is_straight_checkbox,
        is_planned_checkbox,
        image_path_field,
        source_path_field,
        info_path_field,
    ]

    def error_msg(e):
        gui.content.page.add(
            Text("Error")
        )
        BannerMsg(page, "Please fill in the required fields or make sure the entered data is the correct value type",
                  "warning", e)

    def update_tab():
        nonlocal tab_status
        tab_status = tabs.tabs[tabs.selected_index].text
        for f in widgets:
            if f != wood_id_text_field:
                f.visible = (
                        tab_status == "Insert Row"
                )
            page.update()

        for b in action_buttons:
            if b == insert_btn or b == print_label_btn:
                b.visible = tab_status == "Insert Row"
            else:
                b.visible = tab_status == "Delete Row"
            page.update()

        for f in widgets:
            if f == wood_id_text_field:
                f.visible = tab_status == "Delete Row"
                page.update()

    def cancel(e):
        for f in widgets:
            f.value = None
        page.update()

    gui = Container(
        bgcolor="white",
        content=
        Column(
            scroll=ScrollMode.ALWAYS,
            height=1000,
            controls=[
                Card(color="#4336f5", content=Container(padding=10, content=Row(width=800, controls=[

                    Text("DATA ENTRY GUI", size=22, weight=flet.FontWeight.W_900, color="white"),

                    ElevatedButton(text="API Documentation", on_click=go_to_api_docs, bgcolor="white",
                                   color="#4336f5"),
                    ElevatedButton(text="Repository", on_click=go_to_github_page, bgcolor="white",
                                   color="#4336f5")

                ], alignment=flet.MainAxisAlignment.CENTER, wrap=True))),
                tabs,

                Divider(height=10, color="white"),

                Row(controls=[
                    Column(controls=[length_text_field, width_text_field, height_text_field, weight_text_field,
                                     wood_id_text_field, source_path_field]),
                    Column(controls=[wood_species_field, label_field, color_text_field,
                                     storage_location_text_field, type_text_field])],
                    alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[image_path_field], alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[is_planned_checkbox, is_straight_checkbox, is_fire_treated_checkbox],
                    alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[info_path_field], alignment=flet.MainAxisAlignment.CENTER),

                Divider(height=10, visible=True, color="white"),
                Row(controls=[
                    Column(
                        controls=action_buttons[:-1]),
                    Column(
                        controls=[action_buttons[-1]]),
                    Column(controls=[ElevatedButton(text="Clear", on_click=cancel, bgcolor="grey", color="white")]),

                ], alignment=flet.MainAxisAlignment.CENTER),
            ], alignment=flet.MainAxisAlignment.CENTER, horizontal_alignment=flet.CrossAxisAlignment.CENTER)
    )

    page.views.append(
        gui
    )
    update_tab()


flet.app(target=main, view=flet.WEB_BROWSER)
