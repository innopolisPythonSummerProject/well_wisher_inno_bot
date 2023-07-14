from browser import document, html, window

# main doby
main = html.DIV(id="main")

# Picture part
# header
picture_title_container = html.DIV(Class="headers", id="firstHeader")
picture_title_container <= html.H3("Generate your picture:")
main <= picture_title_container

# Kittens checkbox
first_checkbox_div = html.DIV(
    style={"display": "flex", "flex-direction": "column"},
    Class="checkboxes",
    id="checkbox_first_div",
)
label = html.LABEL()
checkbox1 = html.INPUT(type="checkbox")
label_text = "Kittens"
label <= checkbox1
label <= label_text
first_checkbox_div <= label

# Sparkles checkbox
checkbox2 = html.INPUT(type="checkbox", name="myCheckbox")
label2 = html.LABEL()
label2 <= checkbox2
label2 <= "Sparkles"
first_checkbox_div <= label2

# User profile checkbox
second_checkbox_div = html.DIV(
    style={"display": "flex", "flex-direction": "column"},
    id="checkbox2",
    Class="checkboxes",
)
checkbox3 = html.INPUT(type="checkbox", name="myCheckbox")
label3 = html.LABEL()
label3 <= checkbox3
label3 <= "User picture"
second_checkbox_div <= label3

# div for all checkboxes
all_checkboxes_div = html.DIV(
    style={
        "padding-top": "0px",
        "padding-bottom": "20px",
        "width": "280px",
        "display": "flex",
        "flex-direction": "row",
        "gap": "12px",
        "justify-content": "space-between",
    }
)  # rewrite in %
all_checkboxes_div <= first_checkbox_div
all_checkboxes_div <= second_checkbox_div
main <= all_checkboxes_div

# Image container witha a picture
container = html.DIV(id="picture_container")
loading_text = html.SPAN(
    "Loading...", id="loadingText", style={"position": "relative", "bottom": "-48%"}
)
container <= loading_text


# Image loading
def handle_image_load(event):
    # Remove the loading text when the image is successfully loaded
    loading_text.remove()


def handle_image_error(event):
    # Handle the case when the image fails to load
    failed_div = html.DIV(id="failed_div")
    loading_text.text = "Failed to load image"


image = html.IMG(src="../example.png", style={"width": "100%", "height": "100%"})

# Add event listeners for image load and error
image.bind("load", handle_image_load)  # need to make multiple calls for generation
image.bind("error", handle_image_error)

container <= image
main <= container

# New picture bottum
# Variable to track button click state
button_clicked = False


# Function to handle the button click event
# need to make two separate functions for text and picture generation
def handle_picture_button_click(event):
    global button_clicked  # лиза сказала что она ожидает каждый раз видеть предупреждение

    # Show the picture only when the button is clicked for the first time
    if not button_clicked:
        # Set button click state to True
        button_clicked = True

        overlay = html.DIV(id="overlay")
        document <= overlay

        # Create custom pop-up window
        popup_window = html.DIV(Class="popup-window", id="popup_window_id")
        popup_content = html.DIV(Class="popup-content")
        popup_text_1 = html.SPAN(
            "Are you sure?",
            style={"font-weight": "bolder", "border": "0px solid #000000"},
        )
        popup_text_2 = html.SPAN(
            "Your latest generation will be deleted",
            style={"font-size": "14px", "border": "0px solid #000000"},
        )

        popup_close_button = html.DIV(id="close_button_div")
        popup_no = html.BUTTON(Class="newButon", id="popup-no")
        svg_code = """<svg xmlns="http://www.w3.org/2000/svg" class="close-svg" viewBox="0 -960 960 960"><path d="m249-207-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>"""
        div = html.DIV()
        div.innerHTML = svg_code
        popup_no <= div
        popup_close_button <= popup_no
        popup_content <= popup_close_button

        popup_content <= popup_text_1
        popup_content <= popup_text_2
        popup_yes_button = html.BUTTON(
            "Generate new", Class="newButtom", id="popup-yes"
        )
        yes_button_div = html.DIV(id="yes_button_div")
        yes_button_div <= popup_yes_button
        popup_content <= yes_button_div
        popup_window <= popup_content
        document <= popup_window
        overlay <= popup_window

        # Bind events to the buttons in the pop-up window
        popup_no_button = document["popup-no"]
        popup_yes_button.bind("click", handle_popup_yes_click)
        popup_no_button.bind("click", handle_popup_no_click)


# Function to handle the "Yes" button click event
def handle_popup_yes_click(event):
    document["overlay"].remove()
    # new generation code here


# Function to handle the "No" button click event
def handle_popup_no_click(event):
    document["overlay"].remove()


picture_button = html.BUTTON(Class="regeneraring_button", id="newPictureButton")
picture_button.bind("click", handle_picture_button_click)
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" class="regenerate-svg" viewBox="0 -960 960 960" >
<path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h60v254H546v-60h168q-38-60-97-97t-137-37q-109 0-184.5 75.5T220-480q0 109 75.5 184.5T480-220q83 0 152-47.5T728-393h62q-29 105-115 169t-195 64Z"/>
</svg>"""
div = html.DIV()
div.innerHTML = svg_code
picture_button <= div
main <= picture_button

# Text part

text_title_container = html.DIV(Class="headers", id="secondHeader")
text_title_container <= html.H3(
    "Generate your text:", style={"position": "relative", "bottom": "-24px"}
)
main <= text_title_container
text_container = html.DIV(id="textContainer")
text_container <= "Ты лучшая тарелочка в этом чатике!"
main <= text_container

# New text button
text_button = html.BUTTON(Class="regeneraring_button", id="newTextButton")
text_button.bind("click", handle_picture_button_click)
svg_code = """<svg xmlns="http://www.w3.org/2000/svg" class="regenerate-svg" viewBox="0 -960 960 960" width="48">
<path d="M480-160q-133 0-226.5-93.5T160-480q0-133 93.5-226.5T480-800q85 0 149 34.5T740-671v-129h60v254H546v-60h168q-38-60-97-97t-137-37q-109 0-184.5 75.5T220-480q0 109 75.5 184.5T480-220q83 0 152-47.5T728-393h62q-29 105-115 169t-195 64Z"/>
</svg>"""
div = html.DIV()
div.innerHTML = svg_code
text_button <= div
main <= text_button


# Wish button


def handle_last_button_click(event):
    overlay = html.DIV(id="overlay")
    document <= overlay

    # Create custom pop-up window
    popup_window = html.DIV(Class="popup-window", id="popup_window_id")
    popup_content = html.DIV(Class="popup-content")
    popup_text_1 = html.SPAN(
        "Are you sure?", style={"font-weight": "bolder", "border": "0px solid #000000"}
    )
    popup_text_2 = html.SPAN(
        "You only have one try this year",
        style={"font-size": "14px", "border": "0px solid #000000"},
    )

    popup_close_button = html.DIV(id="close_button_div")
    popup_no = html.BUTTON(id="popup-no")  # svg not inside the button
    svg_code = """<svg xmlns="http://www.w3.org/2000/svg" class="close-svg" viewBox="0 -960 960 960"><path d="m249-207-42-42 231-231-231-231 42-42 231 231 231-231 42 42-231 231 231 231-42 42-231-231-231 231Z"/></svg>"""
    div = html.DIV()
    div.innerHTML = svg_code
    popup_no <= div
    popup_close_button <= popup_no
    popup_content <= popup_close_button

    popup_content <= popup_text_1
    popup_content <= popup_text_2
    send_button_div = html.DIV(id="send_button_div")
    popup_yes_button = html.BUTTON("Send!", id="popup-send-button")
    send_button_div <= popup_yes_button
    popup_content <= send_button_div
    popup_window <= popup_content
    document <= popup_window
    overlay <= popup_window

    # Bind events to the buttons in the pop-up window
    popup_no_button = document["popup-no"]
    popup_yes_button.bind("click", handle_popup_yes_click)
    popup_no_button.bind("click", handle_popup_no_click)


# Function to handle the "Yes" button click event
def handle_last_yes_click(event):
    # more actions
    window.close()


# Function to handle the "No" button click event
def handle_last_no_click(event):
    document["overlay"].remove()


div = html.DIV(id="send_my_wishes_button_div")
submit_button = html.BUTTON("Send my wishes!", id="send_my_wishes_button")
submit_button.bind("click", handle_last_button_click)
div <= submit_button
main <= div
document <= main
