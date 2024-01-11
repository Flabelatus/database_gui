import time

import flet
from flet import Text
from flet import Page
from flet_core import TextButton, Banner, colors, Icon, icons


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
