import os
import sys
import time
from datetime import datetime
import json

import zpl
from zebra import Zebra
from PIL import Image as Img
import flet
from flet import TextField, Text, Column, Row, Checkbox
from flet import Page, Container, Divider, Image, ElevatedButton
from flet_core import Card, TextButton, Banner, colors, Icon, icons, ScrollMode
import webbrowser
import requests

# index is used to print the label
index_to_print = 0

# Get data from the server and append the ID of the wood to the URL
data = requests.get('https://robotlab-residualwood.onrender.com/residual_wood/' + str(index_to_print))

# turns received data into a dictionary
library = data.json()

# the printername you gave to the printer during installation
cups_printername = 'Zebra_ZD410'

dictionary = {}

URL = "https://robotlab-residualwood.onrender.com/"
URL_DEV = "http://localhost:5000/"
KEYS = ["length", "width", "height", "weight", "wood_species", "label", "color", "storage_location",
        "wood_id", "paint", "type",
        "project_type", "is_fire_treated", "is_straight", "is_planed", "image", "source", "info"]
values = []
param = []


def resource_path(relative_path):
    """ Get absolute path to resource"""

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def print_label(d):
    # create label
    label_to_print = zpl.Label(17, 38)  # vertical, horizontal

    # write an image (change 'if False' to 'if True' when you want to actually add it
    image_width = 2
    label_to_print.origin(30, 2)
    # logo = Img.open('C:\\Users\\jjooshe\\Desktop\\from remote\\python\\wood_db_manual_gui\\assets\\logo.png')
    # label_to_print.write_graphic(logo, image_width)
    label_to_print.endorigin()

    label_to_print.origin(3, 8)  # horizontal, vertical
    label_to_print.write_text("Density: {}g/cm3".format(int(d["density"])), char_height=2, char_width=1.5,
                              line_width=25,
                              justification='L', orientation='N')
    label_to_print.endorigin()

    label_to_print.origin(3, 12)  # horizontal, vertical
    label_to_print.write_text("{}".format(index_to_print), char_height=5, char_width=3, line_width=25,
                              justification='L',
                              orientation='N')
    label_to_print.endorigin()

    label_to_print.origin(3, 4)  # horizontal, vertical
    label_to_print.write_text("LxWxH: {}".format((str(d["length"]) + "X" + str(d["width"]) + "X" + str(d["height"]))),
                              char_height=2, char_width=1.5, line_width=25, justification='L', orientation='N')
    label_to_print.endorigin()

    label_to_print.origin(3, 6)  # horizontal, vertical
    label_to_print.write_text("Weight (grams): {}".format(d["weight"]), char_height=2, char_width=1.5, line_width=25,
                              justification='L',
                              orientation='N')
    label_to_print.endorigin()

    label_to_print.origin(3, 2)  # horizontal, vertical
    label_to_print.write_text("Location: {}".format(d["storage_location"]), char_height=2, char_width=1.5,
                              line_width=25,
                              justification='L',
                              orientation='N')
    label_to_print.endorigin()

    # now add a 2D barcode
    # starting point
    barcode2d_x = 10
    barcode2d_y = 4

    label_to_print.origin(barcode2d_x + 10, barcode2d_y + 3)  # horizontal, vertical
    # the first argument determines the type of code, 'Q' for QR code and 'X' for datamatrix code.
    label_to_print.barcode('X', index_to_print, height=10)
    label_to_print.endorigin()

    z = Zebra()

    queue = z.getqueues()
    z.setqueue(queue[0])
    z.setup()
    z.output(label_to_print.dumpZPL())


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
        time.sleep(3.5)
        self.close_banner(self.event)

    def show_banner(self, event):
        self.page.banner.open = True
        self.page.update()

    def close_banner(self, event):
        self.page.banner.open = False
        self.page.update()


def handle_post_request(p, e):
    global index_to_print
    global dictionary
    inserted_data = list(zip(KEYS, values))
    payload = {}
    endpoint = "/residual_wood"
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

    # response = requests.post(URL + endpoint, data=json_body, timeout=10, headers=headers)
    # dictionary = response.json()
    # index_to_print = response.json()['id']
    print(">>>>>>", json_body)
    # return response.json(), response.status_code


def handle_delete_request():
    payload = {}
    if param:
        for p in param:
            payload["wood_id"] = p

    json_body = json.dumps(payload)
    response = requests.delete(URL + "residual_wood", data=json_body, headers={"Content-Type": "application/json"})
    print(response.status_code)
    return response.status_code


def main(page: Page):
    page.theme_mode = 'light'
    page.title = "Robot Lab Wood DB"
    page.description = "A simple tool to add data of waste wood into the database"
    page.window_width = 520
    page.window_height = 850
    page.theme = flet.Theme(visual_density=flet.ThemeVisualDensity.COMFORTABLE, use_material3=True,
                            color_scheme_seed="#4336f5")

    tab_status = "Insert Row"

    def __print_label__(e):
        global index_to_print
        if index_to_print == 0:
            BannerMsg(page, "The index to print is not specified. First insert the data to generate the Index.",
                      'error', e)
        else:
            print_label(dictionary)
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
            # response = handle_post_request(page, e)
            # if response[1] != 201:
            #     if response[1] == 400:
            #         BannerMsg(page, f"Message: {response[0]['message']}", 'error', e)
            #     elif response[1] != 400:
            #         BannerMsg(page, "Something went wrong - status code: {}".format(response[1]), 'error', e)
            # else:
            #     BannerMsg(page, "Successfully saved to DB", 'message', e)

    def delete_row(e):
        err = False
        if len(param) > 0:
            param.clear()
        for f in widgets:
            if f.label == "Wood ID *" and f.value == "":
                error_msg(e)
                err = True
                break
            elif f == wood_id_text_field:
                param.append(f.value)
                break
        if err is False:
            resp = handle_delete_request()
            if resp != 200:
                if resp == 404:
                    BannerMsg(page, "The entered ID does not exist - status code: {}".format(resp), 'error', e)
                elif resp != 404:
                    BannerMsg(page, "Something went wrong - status code: {}".format(resp), 'error', e)
            else:
                BannerMsg(page, f"Successfully deleted the row with Wood ID: {param[-1]}", 'message', e)

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
                                  border_color="#4336f5", color="#4336f5", keyboard_type=flet.KeyboardType.NUMBER)
    width_text_field = TextField(label="Width *", tooltip="Width of the wood in mm", width=200, height=40,
                                 border_color="#4336f5", color="#4336f5")
    height_text_field = TextField(label="Height *", tooltip="Height of the wood in mm", width=200, height=40,
                                  border_color="#4336f5", color="#4336f5")

    weight_text_field = TextField(label="Weight *", tooltip="Weight of the wood in kg", width=200, height=40,
                                  border_color="#4336f5", color="#4336f5")

    wood_species_field = TextField(label="Species", tooltip="Species and process of the wood e.g. Red Oak FSC ",
                                   width=200, height=40, border_color="#4336f5", color="#4336f5")
    label_field = TextField(label="Source location", tooltip="Label of the material from specific project", width=200,
                            height=40,
                            border_color="#4336f5", color="#4336f5")
    color_text_field = TextField(label="Color *", tooltip="Color of the wood in (RGB) e.g. '120, 130, 90'", width=200,
                                 height=40, border_color="#4336f5", color="#4336f5")
    storage_location_text_field = TextField(label="Storage Location",
                                            tooltip="A reference to where the wood is stored in the physical storage",
                                            width=200, height=40, border_color="#4336f5", color="#4336f5")
    wood_id_text_field = TextField(label="Wood ID *",
                                   tooltip="ID of the wood e.g. in the 7 digits format of '00000001'",
                                   width=200, height=40, border_color="#4336f5", color="#4336f5")
    paint_text_field = TextField(label="Paint color", width=120, height=40, tooltip="The RAL number of the"
                                                                                    " wood if it is painted",
                                 border_color="#83613F", color="#83613F", bgcolor="FFE5CC")
    type_text_field = TextField(label="Wood type", width=200, height=40, tooltip="Wood type e.g. hardwood or softwood",
                                border_color="#4336f5", color="#4336f5")

    project_type = TextField(label="Project type", width=120, height=40, border_color="#83613F", color="#83613F",
                             bgcolor='FFE5CC',
                             tooltip="Project specific information considered for Derako BV."
                                     " This is clarified in the spreadsheet of"
                                     " the projects usually. If you do not know what it is, leave it blank")

    is_fire_treated_checkbox = Checkbox(label="Fire treated")
    is_straight_checkbox = Checkbox(label="Straight", value=True)
    is_planned_checkbox = Checkbox(label="Planed", value=True)

    image_path_field = TextField(label="Image path", tooltip="Path to where image is stored", width=412, height=40,
                                 border_color="#4336f5", color="#4336f5")
    source_path_field = TextField(label="Intake location *", tooltip="Location where the wood was in-taken", width=200,
                                  height=40, border_color="#4336f5", color="#4336f5")
    info_path_field = TextField(width=410, label="Info", multiline=True, border_color="#4336f5", color="#4336f5")

    insert_btn = ElevatedButton(text="Insert", on_click=submit, bgcolor="#4336f5", color="white")
    delete_btn = ElevatedButton(text="Delete", on_click=delete_row, bgcolor="#4336f5", color="white")
    print_label_btn = ElevatedButton(text="Print Label", on_click=__print_label__, bgcolor="#9891F6", color="white")

    action_buttons = [insert_btn, delete_btn, print_label_btn]

    card_widget = Card(
        width=400,
        color="#C6905A",
        content=Container(
            padding=20,
            content=Column(
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                alignment=flet.MainAxisAlignment.CENTER,
                controls=[
                    Text("Data Related to Wood from Derako BV", size=18,
                         weight=flet.FontWeight.W_500,
                         color=colors.WHITE,
                         text_align=flet.TextAlign.CENTER),
                    Text("This fields are used only for the wood that is delivered by Derako BV", size=14,
                         weight=flet.FontWeight.W_200,
                         color=colors.WHITE,
                         text_align=flet.TextAlign.CENTER),
                    Divider(height=10, visible=True, color="#C6905A"),
                    Row(controls=[project_type, paint_text_field],
                        alignment=flet.MainAxisAlignment.CENTER),
                ]
            )
        )
    )

    widgets = [
        length_text_field,
        width_text_field,
        height_text_field,
        weight_text_field,
        # density_text_field,
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
        info_path_field,
        card_widget
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
            scroll=ScrollMode.HIDDEN,
            height=760,
            controls=[
                Divider(height=25, color="white"),
                Card(color="#4336f5", content=Container(padding=10, content=Column(controls=[
                    Image(
                        src="C:\\Users\\jjooshe\\Desktop\\from remote\\python\\wood_db_manual_gui\\"
                            "assets\\RL LOGO WHITE .png",
                        fit=flet.ImageFit.CONTAIN, width=200),
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
                    Column(controls=[wood_species_field, label_field, color_text_field,
                                     storage_location_text_field, type_text_field])],
                    alignment=flet.MainAxisAlignment.CENTER),
                Row(controls=[image_path_field], alignment=flet.MainAxisAlignment.CENTER),
                Divider(height=10, visible=True, color="white"),
                Row(controls=[is_planned_checkbox, is_straight_checkbox, is_fire_treated_checkbox],
                    alignment=flet.MainAxisAlignment.CENTER),
                Divider(height=10, visible=True, color="white"),
                Row(controls=[info_path_field], alignment=flet.MainAxisAlignment.CENTER),
                Divider(height=10, visible=True, color="white"),

                card_widget,

                # Row(controls=[project_type, paint_text_field],
                #     alignment=flet.MainAxisAlignment.CENTER),

                # Divider(height=25, visible=True, color="white"),

                # Row(controls=[info_path_field], alignment=flet.MainAxisAlignment.CENTER),

                Divider(height=30, visible=True, color="white"),
                Row(controls=[
                    Column(
                        controls=action_buttons[:-1]),
                    Column(
                        controls=[action_buttons[-1]]),
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


flet.app(target=main, view=flet.WEB_BROWSER)

