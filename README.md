# PySimpleGUI Events
A simple event system for PySimpleGUI applications.

### Simple Tutorial
The following tutorial is based on the CookBook entry [Recipe - Pattern 2B - Persistent window](https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-pattern-2b-persistent-window-multiple-reads-using-an-event-loop-updates-data-in-window).

#### Importing the Event Handler
    
    import PySimpleGUI as sg
    import PySimpleGUI_Events as sge

#### Instantiate the EventManager and ApplicationState

    layout = [...]

    window = sg.Window("Pattern 2B", layout)

    # application_data caries a reference to the window for use in event handlers
    # The message="" inclusion creates a data member in the application_data object
    # under the key "message".
    application_data = sge.SimpleApplicationState(window, message="")

    event_manager = sge.EventManager()

#### Create an Event Handler Function
Every event handler is a function that satisfies the following function signature:
event_handler_function(values, application_data)

Values are the values dictionary returned from window.read() while application_data
is a data record object based on the SimpleActionData object.
    
    def _show_handler(values, application_data):
        application_data[MESSAGE_KEY] = values[IN_KEY]
        application_data.window[OUTPUT_KEY].update(application_data[MESSAGE_KEY])
        application_data.window[CAPITALIZE_KEY].update(disabled=False)

#### Create Event Handler Object
Handler objects are SimpleHandler objects that marry the key of the firing UI Element
to a handler function.

    show_handler = sge.SimpleHandler(SHOW_KEY, _show_handler)

#### Add the Event Handler to the Event Manager
SimpleHandler objects are passed to the event manager object java-style through the += operator.

    event_manager += show_handler

#### Execute all EventHandlers in the Application Loop
Event handlers are tracked through a dictionary of function lists and fired in
the order they are added to the event handler.
**Event handler functions that raise an Abort exception will abort handler execution
and any un-executed handlers will not fire.**

The goal of the PySimpleGUI_Events library is to allow UI events to be broken up into
small, logical pieces and keep complexity to a minimum.

    event_manager.execute(event, values, application_data)


#### app.py (full code)

    import PySimpleGUI as sg
    import PySimpleGUI_Events as sge
    
    OUTPUT_KEY = "-OUTPUT-"
    IN_KEY = "-IN-"
    CAPITALIZE_KEY = "Capitalize"
    SHOW_KEY = "Show"
    EXIT_KEY = "Exit"
    MESSAGE_KEY = "message"
    
    
    def _exit_handler(values, application_data):
        application_data.window.close()
        exit()
    
    
    exit_handler = sge.SimpleHandler(EXIT_KEY, _exit_handler)
    
    
    def _show_handler(values, application_data):
        application_data[MESSAGE_KEY] = values[IN_KEY]
        application_data.window[OUTPUT_KEY].update(application_data[MESSAGE_KEY])
        application_data.window[CAPITALIZE_KEY].update(disabled=False)
    
    
    show_handler = sge.SimpleHandler(SHOW_KEY, _show_handler)
    
    
    def _capitalize_handler(values, application_data):
        application_data.window[OUTPUT_KEY].update(application_data[MESSAGE_KEY].upper())
    
    
    capitalize_handler = sge.SimpleHandler(CAPITALIZE_KEY, _capitalize_handler)
    
    layout = [
        [sg.Text("Your typed chars appear here:"), sg.Text(size=(15, 1), key=OUTPUT_KEY)],
        [sg.Input(key=IN_KEY)],
        [sg.Button("Capitalize", disabled=True), sg.Button("Show"), sg.Button("Exit")],
    ]
    
    event_manager = sge.EventManager()
    
    event_manager += exit_handler
    event_manager += show_handler
    event_manager += capitalize_handler
    
    window = sg.Window("Pattern 2B", layout)
    application_data = sge.SimpleApplicationState(window, message="")
    
    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        event_manager.execute(event, values, application_data)
    
    window.close()

### Project Structure Best Practices

* All key values used in the layout, and event handlers should be stored in constant values, or in a constants class. Do not hard-code raw strings if possible.
* Handler functions...
  * Handler functions and SimpleHandler object definitions should be stored in a handlers package with files named after the owning gui elements.
    * Example: If the Show button were to both set the string value *and* capitalize the string they should both be written in the same *show_handlers.py* file.
  * The handlers package shouldn't import any of the functions into __init__.py. Sorting handler objects by filename allows handler objects for different GUI elements to share names across files and enables a level of standardization.