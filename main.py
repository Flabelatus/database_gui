import time
from datetime import datetime

import flet
from flet import TextField, Text, Column, Row, Checkbox
from flet import Page, Container, Divider, FilledTonalButton
from flet_core import Card, FilledButton, TextButton, Banner, colors, Icon, icons
import webbrowser
import requests


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


values = []
keys = ["length", "width", "height", "weight", "density", "wood_species", "label", "color", "paint", "type",
        "project_type", "is_fire_treated", "is_straight", "is_planed", "image", "source", "info"]


def handle_request():
    inserted_data = list(zip(keys, values))
    payload = {}

    for item in inserted_data:
        if item[0] in ["length", "width", "height", "weight", "density"]:
            payload[item[0]] = float(item[1])
        else:
            payload[item[0]] = item[1]

    payload["timestamp"] = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
    print(payload)


def main(page: Page):
    page.theme_mode = 'light'
    page.title = "Robot Lab Wood DB"
    page.description = "A simple tool to add data of waste wood into the database"
    page.window_width = 520
    page.window_height = 850
    page.scroll = "always"

    btn_style_1 = flet.ButtonStyle(bgcolor=flet.colors.BLUE)
    btn_style_2 = flet.ButtonStyle(bgcolor=flet.colors.GREY)
    btn_style_3 = flet.ButtonStyle(bgcolor=flet.colors.GREEN)

    def go_to_api_docs(e):
        webbrowser.open("https://robotlab-residualwood.onrender.com/swagger-ui")

    def go_to_github_page(e):
        webbrowser.open("https://github.com/Flabelatus/CircularWood_4.0_WP1")

    length_text_field = TextField(label="Length *", tooltip="Length of the wood in mm", width=200, height=40)
    width_text_field = TextField(label="Width *", tooltip="Width of the wood in mm", width=200, height=40)
    height_text_field = TextField(label="Height *", tooltip="Height of the wood in mm", width=200, height=40)

    weight_text_field = TextField(label="Weight *", tooltip="Weight of the wood in kg", width=200, height=40)
    density_text_field = TextField(label="Density *", tooltip="Density of the wood mm3/kg", width=200, height=40)
    wood_species_field = TextField(label="Species", tooltip="Species and process of the wood e.g. Red Oak FSC ",
                                   width=200, height=40)
    label_field = TextField(label="Label", tooltip="Label of the material from specific project", width=200, height=40)
    color_text_field = TextField(label="Color *", tooltip="Color of the wood in (RGB) e.g. '120, 130, 90'", width=200,
                                 height=40)
    paint_text_field = TextField(label="RAL number", width=120, height=40, tooltip="The RAL number of the"
                                                                                   " wood if it is painted")
    type_text_field = TextField(label="Wood type", width=120, height=40, tooltip="Wood type e.g. hardwood or softwood")

    project_type = TextField(label="Project type", width=120, height=40,
                             tooltip="Project type that determines if the material contains holes or not and if yes,"
                                     " where are they positioned. This is clarified in the spreadsheet of"
                                     " the projects usually")

    is_fire_treated_checkbox = Checkbox(label="Fire treated")
    is_straight_checkbox = Checkbox(label="Straight", value=True)
    is_planned_checkbox = Checkbox(label="Planed", value=True)

    image_path_field = TextField(label="Image path", tooltip="Path to where image is stored", width=200, height=40)
    source_path_field = TextField(label="Source *", tooltip="Source location where the wood was collected", width=200,
                                  height=40)
    info_path_field = TextField(width=410, label="Info", multiline=True)

    fields = [length_text_field, width_text_field, height_text_field, weight_text_field, density_text_field,
              wood_species_field, label_field,
              color_text_field, paint_text_field, type_text_field, project_type, is_fire_treated_checkbox,
              is_straight_checkbox, is_planned_checkbox, image_path_field, source_path_field, info_path_field
              ]

    def error_msg(e):
        gui.content.page.add(
            Text("Error")
        )
        BannerMsg(page, "Please fill in the required fields", "warning", e)

    def cancel(e):
        for f in fields:
            f.value = None
        page.update()

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
            handle_request()
            BannerMsg(page, "Successfully saved to DB", 'message', e)

    gui = Container(
        content=Column(controls=[
            Divider(height=25, color="#FFFFFF"),
            Card(content=Container(padding=10, content=Column(controls=[
                Text("ROBOT LAB WOOD DATABASE", size=20, weight=flet.FontWeight.W_500),
                Text("URL: https://https://robotlab-residualwood.onrender.com/residual_wood", size=14,
                     weight=flet.FontWeight.W_100, selectable=True),
                Row(controls=[FilledTonalButton(text="API Documentation", on_click=go_to_api_docs, style=btn_style_1),
                              FilledTonalButton(text="Repository", on_click=go_to_github_page, style=btn_style_2)]),
            ], horizontal_alignment=flet.CrossAxisAlignment.CENTER, wrap=True))),

            Divider(height=25, color="#FFFFFF"),

            Row(controls=[
                Column(controls=[length_text_field, width_text_field, height_text_field, weight_text_field]),
                Column(controls=[density_text_field, wood_species_field, label_field, color_text_field])],
                alignment=flet.MainAxisAlignment.CENTER),
            Row(controls=[image_path_field, source_path_field], alignment=flet.MainAxisAlignment.CENTER),
            Divider(height=25, visible=True),
            Row(controls=[is_planned_checkbox, is_straight_checkbox, is_fire_treated_checkbox],
                alignment=flet.MainAxisAlignment.CENTER),
            Row(controls=[project_type, paint_text_field, type_text_field],
                alignment=flet.MainAxisAlignment.CENTER),

            Divider(height=25, visible=True),

            Row(controls=[info_path_field], alignment=flet.MainAxisAlignment.CENTER),

            Divider(height=30, visible=True),
            Row(controls=[
                Column(controls=[FilledButton(text="Save", on_click=submit, style=btn_style_3)]),
                Column(controls=[FilledTonalButton(text="Clear", on_click=cancel, style=btn_style_2)]),
                Column(controls=[
                    FilledTonalButton(text="Close", on_click=lambda x: page.window_destroy(), style=btn_style_2)])
            ], alignment=flet.MainAxisAlignment.CENTER),

        ], alignment=flet.MainAxisAlignment.CENTER, horizontal_alignment=flet.CrossAxisAlignment.CENTER)

    )

    page.views.append(
        gui
    )
    page.update()


flet.app(target=main)
