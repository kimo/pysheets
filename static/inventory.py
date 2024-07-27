"""
Copyright (c) 2024 laffra - All Rights Reserved. 

Retrieves and displays a list of sheets in the application's main view.
"""

import constants
import ltk
import state
import storage
import menu


def list_sheets():
    """
    Retrieves and displays a list of sheets in the application's main view.
    """
    state.clear()
    ltk.find("#main").append(
        ltk.Button("New Sheet", ltk.proxy(lambda event: None)).addClass("new-button temporary"),
        ltk.Card(ltk.Div().css("width", 204).css("height", 188)).addClass("document-card temporary"),
        ltk.Card(ltk.Div().css("width", 204).css("height", 188)).addClass("document-card temporary"),
        ltk.Card(ltk.Div().css("width", 204).css("height", 188)).addClass("document-card temporary"),
        ltk.Card(ltk.Div().css("width", 204).css("height", 188)).addClass("document-card temporary"),
        ltk.Card(ltk.Div().css("width", 204).css("height", 188)).addClass("document-card temporary"),
    )
    ltk.find(".temporary").css("opacity", 0).animate(ltk.to_js({ "opacity": 1 }), 2000)
    storage.list_sheets(show_sheet_list)
    ltk.find("#main").animate(ltk.to_js({ "opacity": 1 }), constants.ANIMATION_DURATION)


def show_sheet_list(sheets):
    """
    Displays a list of sheets in the application's main view. This function is responsible for creating
    the UI elements that represent each sheet, including a screenshot, name, and a click/keyboard
    event handler to load the sheet.
    """
    state.clear()
    ltk.find("#main").empty()

    def create_card(uid, index, runtime, packages, *items):
        def select_doc(event):
            if event.keyCode == 13:
                load_doc_with_packages(uid, runtime, packages)

        return (
            ltk.Card(*items)
                .on("click", ltk.proxy(lambda event=None: load_doc_with_packages(uid, runtime, packages)))
                .on("keydown", ltk.proxy(select_doc))
                .attr("tabindex", 1000 + index)
                .addClass("document-card")
        )

    ltk.find("#main").append(
        ltk.Container(
            *[
                create_card(
                    sheet.uid,
                    index,
                    "mpy",
                    "",
                    ltk.VBox(
                        ltk.Image(sheet.screenshot),
                        ltk.Text(sheet.name),
                    ),
                )
                for index, sheet in enumerate(sheets)
            ]
        ).prepend(
            ltk.Button("New Sheet", ltk.proxy(lambda event: menu.new_sheet())).addClass(
                "new-button"
            )
        ).css("overflow", "auto").css("height", "100%")
    )
    ltk.find(".document-card").eq(0).focus()
    ltk.find("#menu").empty()
    state.show_message("Select a sheet below or create a new one...")


def load_doc_with_packages(uid, runtime, packages):
    """
    Loads a document with the specified packages.
    
    Args:
        uid (str): The unique identifier of the document to load.
        runtime (str): The runtime environment to use for the document.
        packages (str): A comma-separated list of Python packages to load with the document.
    
    Returns:
        None
    """
    url = f"/?{constants.SHEET_ID}={uid}&{constants.PYTHON_RUNTIME}={runtime}"
    if packages:
        url += f"&{constants.PYTHON_PACKAGES}={packages}"
    ltk.window.location = url