import time
from datetime import datetime
import json

import flet
from flet import TextField, Text, Column, Row, Checkbox
from flet import Page, Container, Divider, Image, ElevatedButton
from flet_core import Card, TextButton, Banner, colors, Icon, icons, ScrollMode
import webbrowser
import requests

URL = "https://robotlab-residualwood.onrender.com/"
URL_DEV = "http://localhost:5000/"
KEYS = ["length", "width", "height", "weight", "density", "wood_species", "label", "color", "storage_location",
        "wood_id", "paint", "type",
        "project_type", "is_fire_treated", "is_straight", "is_planed", "image", "source", "info"]
values = []
param = []


class BannerMsg:
    """
    A class to represent a Banner object.
    It is initiated either as 'warning' or 'message' to inform the user about the process actions

    Attributes:
        page (:Page): The Page control in which this banner as a flet control object is added to.
            Also, can be the main page.
        msg (str): The message which will be shown in the banner
        banner_type (str): Specifying the type of banner. Only can be from these options
            'warning' or 'message'.
        event (:Event): The event argument for of flet application

    Methods:
        show_banner: Set the `open` property of the `Banner` to True
        close_banner: Set the `open` property of the `Banner` to False

    """

    def __init__(self, page: Page, msg: str, banner_type: str, event):

        self.event = event
        self.page = page
        self.msg = msg
        self.banner_type = banner_type

        if self.banner_type == 'error':
            self.icon = flet.icons.ERROR_ROUNDED
            self.color = flet.colors.RED_ACCENT
            self.bg_color = flet.colors.RED_ACCENT_100

        if self.banner_type == 'warning':
            self.icon = flet.icons.WARNING_AMBER_ROUNDED
            self.color = flet.colors.ORANGE
            self.bg_color = flet.colors.ORANGE_100

        elif self.banner_type == 'message':
            self.icon = flet.icons.MESSAGE_ROUNDED
            self.color = flet.colors.INDIGO
            self.bg_color = flet.colors.INDIGO_50

        self.page.banner = Banner(bgcolor=self.bg_color,
                                  leading=Icon(self.icon, color=self.color, size=30),
                                  content=Text(self.msg, color=colors.BLACK87),
                                  actions=[
                                      TextButton(icon_color=colors.BLACK45, icon=icons.CHECK,
                                                 on_click=self.close_banner, scale=1.2)])
        self.show_banner(self.event)
        time.sleep(2.5)
        self.close_banner(self.event)

    def show_banner(self, event):
        self.page.banner.open = True
        self.page.update()

    def close_banner(self, event):
        self.page.banner.open = False
        self.page.update()


def handle_post_request():
    inserted_data = list(zip(KEYS, values))
    payload = {}
    endpoint = "/residual_wood"
    headers = {"Content-Type": "application/json"}

    for item in inserted_data:
        if item[0] in ["length", "width", "height", "weight", "density"]:
            payload[item[0]] = float(item[1])
        else:
            payload[item[0]] = item[1]

    payload["timestamp"] = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
    json_body = json.dumps(payload)

    response = requests.post(URL + endpoint, data=json_body, timeout=10, headers=headers)
    # print(">>>>>>", json_body)
    return response.json()


def handle_delete_request():
    payload = {}
    if param:
        for p in param:
            payload["wood_id"] = p

    json_body = json.dumps(payload)
    response = requests.delete(URL + "residual_wood", data=json_body, headers={"Content-Type": "application/json"})
    return response.json()


def main(page: Page):
    page.theme_mode = 'light'
    page.title = "Robot Lab Wood DB"
    page.description = "A simple tool to add data of waste wood into the database"
    page.window_width = 520
    page.window_height = 850
    page.theme = flet.Theme(visual_density=flet.ThemeVisualDensity.COMFORTABLE, use_material3=True,
                            color_scheme_seed="#4336f5")

    def tab_changed(e):
        update_tab()

    def submit(e):
        error_status = False
        if len(values) > 0:
            values.clear()
        for f in fields:
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
            handle_post_request()
            BannerMsg(page, "Successfully saved to DB", 'message', e)
            time.sleep(1)
            for f in fields:
                if f != wood_id_text_field:
                    f.value = ""
            page.update()

    def delete_row(e):
        err = False
        if len(param) > 0:
            param.clear()
        for f in fields:
            if f.label == "Wood ID *" and f.value == "":
                error_msg(e)
                err = True
                break
            elif f == wood_id_text_field:
                param.append(f.value)
                break
        if err is False:
            handle_delete_request()
            BannerMsg(page, f"Successfully deleted the row with Wood ID: {param[-1]}", 'message', e)
            time.sleep(1)
            for f in fields:
                if f == wood_id_text_field:
                    f.value = ""
                    page.update()
                    break

    def go_to_api_docs(e):
        webbrowser.open("https://robotlab-residualwood.onrender.com/api-docs")

    def go_to_github_page(e):
        webbrowser.open("https://github.com/Flabelatus/CircularWood_4.0_WP1")

    tabs = flet.Tabs(
        selected_index=0,
        tabs=[flet.Tab(text="Insert Row"), flet.Tab(text="Delete Row")],
        on_change=tab_changed
    )

    length_text_field = TextField(label="Length *", tooltip="Length of the wood in mm", width=200, height=40,
                                  border_color="#4336f5", color="#4336f5")
    width_text_field = TextField(label="Width *", tooltip="Width of the wood in mm", width=200, height=40,
                                 border_color="#4336f5", color="#4336f5")
    height_text_field = TextField(label="Height *", tooltip="Height of the wood in mm", width=200, height=40,
                                  border_color="#4336f5", color="#4336f5")

    weight_text_field = TextField(label="Weight *", tooltip="Weight of the wood in kg", width=200, height=40,
                                  border_color="#4336f5", color="#4336f5")
    density_text_field = TextField(label="Density *", tooltip="Density of the wood mm3/kg", width=200, height=40,
                                   border_color="#4336f5", color="#4336f5")
    wood_species_field = TextField(label="Species", tooltip="Species and process of the wood e.g. Red Oak FSC ",
                                   width=200, height=40, border_color="#4336f5", color="#4336f5")
    label_field = TextField(label="Label", tooltip="Label of the material from specific project", width=200, height=40,
                            border_color="#4336f5", color="#4336f5")
    color_text_field = TextField(label="Color *", tooltip="Color of the wood in (RGB) e.g. '120, 130, 90'", width=200,
                                 height=40, border_color="#4336f5", color="#4336f5")
    storage_location_text_field = TextField(label="Storage Location",
                                            tooltip="A reference to where the wood is stored in the physical storage",
                                            width=200, height=40, border_color="#4336f5", color="#4336f5")
    wood_id_text_field = TextField(label="Wood ID *", tooltip="ID of the wood e.g. in the 7 digits format of '00000001'",
                                   width=200, height=40, border_color="#4336f5", color="#4336f5")
    paint_text_field = TextField(label="RAL number", width=120, height=40, tooltip="The RAL number of the"
                                                                                   " wood if it is painted",
                                 border_color="#4336f5", color="#4336f5")
    type_text_field = TextField(label="Wood type", width=120, height=40, tooltip="Wood type e.g. hardwood or softwood",
                                border_color="#4336f5", color="#4336f5")

    project_type = TextField(label="Project type", width=120, height=40, border_color="#4336f5", color="#4336f5",
                             tooltip="Project type that determines if the material contains holes or not and if yes,"
                                     " where are they positioned. This is clarified in the spreadsheet of"
                                     " the projects usually")

    is_fire_treated_checkbox = Checkbox(label="Fire treated")
    is_straight_checkbox = Checkbox(label="Straight", value=True)
    is_planned_checkbox = Checkbox(label="Planed", value=True)

    image_path_field = TextField(label="Image path", tooltip="Path to where image is stored", width=412, height=40,
                                 border_color="#4336f5", color="#4336f5")
    source_path_field = TextField(label="Source *", tooltip="Source location where the wood was collected", width=200,
                                  height=40, border_color="#4336f5", color="#4336f5")
    info_path_field = TextField(width=410, label="Info", multiline=True, border_color="#4336f5", color="#4336f5")

    insert_btn = ElevatedButton(text="Insert", on_click=submit, bgcolor="#4336f5", color="white")
    delete_btn = ElevatedButton(text="Delete", on_click=delete_row, bgcolor="#4336f5", color="white")

    action_buttons = [insert_btn, delete_btn]

    fields = [
        length_text_field,
        width_text_field,
        height_text_field,
        weight_text_field,
        density_text_field,
        wood_species_field,
        label_field,
        color_text_field,
        storage_location_text_field,
        wood_id_text_field,
        paint_text_field,
        type_text_field,
        project_type,
        is_fire_treated_checkbox,
        is_straight_checkbox,
        is_planned_checkbox,
        image_path_field,
        source_path_field,
        info_path_field
    ]

    def error_msg(e):
        gui.content.page.add(
            Text("Error")
        )
        BannerMsg(page, "Please fill in the required fields", "warning", e)

    def update_tab():
        status = tabs.tabs[tabs.selected_index].text
        for f in fields:
            if f != wood_id_text_field:
                f.visible = (
                    status == "Insert Row"
                )
            page.update()

        for b in action_buttons:
            if b == insert_btn:
                b.visible = status == "Insert Row"
            else:
                b.visible = status == "Delete Row"
            page.update()

        for f in fields:
            if f == wood_id_text_field:
                f.visible = status == "Delete Row"
                page.update()

    def cancel(e):
        for f in fields:
            f.value = None
        page.update()

    gui = Container(
        bgcolor="white",
        content=
        Column(
            scroll=ScrollMode.HIDDEN,
            height=760,
            controls=[
                Divider(height=25, color="white"),
                Card(color="#4336f5", content=Container(padding=10, content=Column(controls=[
                    Image(src="assets/RL LOGO WHITE .png", fit=flet.ImageFit.CONTAIN, width=200),
                    Text("DATA ENTRY GUI", size=22, weight=flet.FontWeight.W_900, color="white"),
                    Text("contact: j.jooshesh@hva.nl", size=14,
                         weight=flet.FontWeight.W_200, selectable=True, color="white"),
                    Text("https://robotlab-residualwood.onrender.com/residual_wood", size=14,
                         weight=flet.FontWeight.W_200, selectable=True, color="white"),

                    Row(controls=[ElevatedButton(text="API Documentation", on_click=go_to_api_docs, bgcolor="white",
                                                 color="#4336f5"),
                                  ElevatedButton(text="Repository", on_click=go_to_github_page, bgcolor="white",
                                                 color="#4336f5")]),

                ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, wrap=True))),
                tabs,

                Divider(height=25, color="white"),

                Row(controls=[
                    Column(controls=[length_text_field, width_text_field, height_text_field, weight_text_field,
                                     wood_id_text_field, source_path_field]),
                    Column(controls=[density_text_field, wood_species_field, label_field, color_text_field,
                                     storage_location_text_field])],
                    alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[image_path_field], alignment=flet.MainAxisAlignment.CENTER),
                Divider(height=25, visible=True, color="white"),
                Row(controls=[is_planned_checkbox, is_straight_checkbox, is_fire_treated_checkbox],
                    alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[project_type, paint_text_field, type_text_field],
                    alignment=flet.MainAxisAlignment.CENTER),

                Divider(height=25, visible=True, color="white"),

                Row(controls=[info_path_field], alignment=flet.MainAxisAlignment.CENTER),

                Divider(height=30, visible=True, color="white"),
                Row(controls=[
                    Column(
                        controls=action_buttons),
                    Column(controls=[ElevatedButton(text="Clear", on_click=cancel, bgcolor="grey", color="white")]),
                    Column(controls=[
                        ElevatedButton(text="Close", on_click=lambda x: page.window_destroy(), bgcolor="grey",
                                       color="white")])
                ], alignment=flet.MainAxisAlignment.CENTER),
            ], alignment=flet.MainAxisAlignment.CENTER, horizontal_alignment=flet.CrossAxisAlignment.CENTER)
    )

    page.views.append(
        gui
    )
    update_tab()


flet.app(target=main)
