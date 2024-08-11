"""A script to move OBS sources to where they are on the screen."""
import obspython as obs
import pygetwindow as gw
import itertools
import threading
import time
import pyautogui
import win32gui
import win32api
import win32con


# Note: to see your changes when editing this code, restart OBS.

# The time after no windows have been moved until when the loop slows down
INACTIVITY_WAIT = 1.5
# The time the loop sleeps per iteration when it slows down
SLEEP_TIME = 0.2

screen_width, screen_height = pyautogui.size()
program_names = []
is_shutting_down = False
keep_in_bounds = False


def loop():
    """Run the follow windows program."""
    last_movement_time = 0
    while not is_shutting_down:
        current_scene = obs.obs_frontend_get_current_scene()
        named_sources = get_named_sources_from_program_names()
        # Stores the movement states of each program (moving/not moving)
        is_moving = []
        for window_name, source in named_sources:
            is_moving.append(
                update_pos_get_movement(window_name, source, current_scene)
            )
        obs.obs_source_release(current_scene)
        if True in is_moving:
            last_movement_time = time.time()
        elif (time.time() - last_movement_time) > INACTIVITY_WAIT:
            time.sleep(SLEEP_TIME)


def get_named_sources_from_program_names():
    """Get the sources to follow from the names the user enters."""
    named_sources = []
    sources = obs.obs_enum_sources()
    for source in sources:
        source_type = obs.obs_source_get_unversioned_id(source)
        # Skips this source if it is not a window or game capture
        if source_type not in ["window_capture", "game_capture"]:
            continue
        obs_window_name = get_obs_window_name(source)
        # Program names are the names specified by the user
        for name in program_names:
            window_name = None
            occurrences_of_name = 0
            for title in gw.getAllTitles():
                # If the name the user entered is part of a window title
                if name.lower() in title.lower():
                    window_name = title
                    occurrences_of_name += 1
            # If the name the user entered could refer to multiple windows
            if occurrences_of_name > 1:
                window_name = None
            # If the name the user entered is in the properties for this source
            if (name.lower() in obs_window_name.lower()) and window_name:
                named_sources.append([window_name, source])
    obs.source_list_release(sources)
    return named_sources


def update_pos_get_movement(window_name, source, current_scene):
    """Update the position of a window and get if it was moved or not."""
    pos = obs.vec2()
    window = win32gui.FindWindow(None, window_name)
    if not window:
        return
    left, top, right, bottom = win32gui.GetWindowRect(window)

    # The total area of the window
    total_rect = win32gui.GetWindowRect(window)
    total_height = total_rect[3] - total_rect[1]

    # The total size of the "usable" portion of the window
    client_rect = win32gui.GetClientRect(window)
    client_height = client_rect[3] - client_rect[1]
    client_width = client_rect[2] - client_rect[0]

    # The padding around the sides of the windows
    y_frame = win32api.GetSystemMetrics(win32con.SM_CYFRAME)
    x_frame = win32api.GetSystemMetrics(win32con.SM_CXFRAME)
    # The height of the title bar at the top of windows
    title_bar_height = total_height - client_height

    # The window dimensions (including borders + titles bars)
    if has_border(window):
        top = top + title_bar_height - (2 * y_frame)
        left = left + (2 * x_frame)
        bottom = bottom - (2 * y_frame)
        right = right - (2 * x_frame)

    pos.x = left
    pos.y = top
    # Keeps the window within the boundaries
    if keep_in_bounds:
        if left < 0:
            pos.x = 0
        if right > screen_width:
            pos.x = (screen_width - client_width)
        if top < 0:
            pos.y = 0
        if bottom > screen_height:
            pos.y = (screen_height - client_height)

    # Gets the scene that is being used
    scene = obs.obs_scene_from_source(current_scene)
    # Gets the scene item from the source and scene
    scene_item = obs.obs_scene_sceneitem_from_source(scene, source)
    # Changes the position of the scene item if it has moved
    old_pos = obs.vec2()
    obs.obs_sceneitem_get_pos(scene_item, old_pos)
    if (pos.x, pos.y) != (old_pos.x, old_pos.y):
        is_moving = True
        obs.obs_sceneitem_set_pos(scene_item, pos)
    else:
        is_moving = False
    return is_moving


def has_border(window):
    """Get if a window has a border around it."""
    style = win32gui.GetWindowLong(window, win32con.GWL_STYLE)
    border_styles = win32con.WS_BORDER | win32con.WS_THICKFRAME
    return (style & border_styles) != 0


def get_obs_window_name(source):
    """Get a source's window name from its properties in obs."""
    settings = obs.obs_source_get_settings(source)
    window_name = obs.obs_data_get_string(settings, "window")
    obs.obs_data_release(settings)
    # Removes other information about the window that is not its title
    if ":" in window_name:
        window_name = window_name.split(":")[0]
    return window_name


def script_properties():
    """The dropdown menu to select windows to follow."""
    properties = obs.obs_properties_create()
    # Add a dropdown list for choosing sources
    dropdown = obs.obs_properties_add_list(
        properties, "source_names", "Sources to follow:",
        obs.OBS_COMBO_TYPE_EDITABLE,
        obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_properties_add_bool(
        properties, "in_bounds", "Keep sources within the view window"
    )
    # Fill the dropdown list with available sources
    fill_dropdown(dropdown)
    return properties


def fill_dropdown(dropdown):
    """Fill the dropdown menu with sources/source combinations."""
    # Gets all available sources
    sources = obs.obs_enum_sources()
    items_to_add = []
    # If the source type is "window capture", add its name to items_to_add
    for source in sources:
        window_name = get_obs_window_name(source)
        source_type = obs.obs_source_get_unversioned_id(source)
        if source_type in ["window_capture", "game_capture"]:
            items_to_add.append(window_name)
    obs.source_list_release(sources)
    subsets = []
    # Gets all possible combinations of window names to select from
    for length in range(len(items_to_add) + 1):
        for subset in itertools.combinations(items_to_add, length):
            subsets.append(subset)
    # Updates the dropdown to show the combinations
    for subset in subsets:
        if len(subset) > 0:
            joined_subset = ", ".join(subset)
            obs.obs_property_list_add_string(
                dropdown, joined_subset, joined_subset
            )


def script_update(settings):
    """Get inputs when the settings for the script are interacted with."""
    global program_names, keep_in_bounds
    # Get the program names that have been selected
    source_names = obs.obs_data_get_string(settings, "source_names")
    # Splits them for when multiple programs have been selected
    program_names = source_names.split(",")
    # Strips whitespaces around each program name
    for i, name in enumerate(program_names):
        program_names[i] = name.strip()
    keep_in_bounds = obs.obs_data_get_bool(settings, "in_bounds")


def script_load(settings):
    """Start the program."""
    thread_active = False
    for thread in threading.enumerate():
        if thread != threading.main_thread():
            thread_active = True
    if not thread_active:
        # Starts the loop only if it is not running already
        script_update(settings)
        thread = threading.Thread(target=loop)
        thread.start()


def script_unload():
    """End the program by terminating the loop."""
    global is_shutting_down
    is_shutting_down = True


def script_description():
    """The description for the follow windows program."""
    return ("𝔽𝕠𝕝𝕝𝕠𝕨 𝕎𝕚𝕟𝕕𝕠𝕨𝕤\n"
            "Follow windows on your screen.\n\n"
            "Enter the names of the windows that you want to follow.\n\n"
            "You can enter incomplete window names so that the program "
            "continues to follow the window if its name changes, eg. "
            "'Google Chrome' for 'New Tab - Google Chrome'. \n"
            "Just make sure that each window name can only correspond to 1 "
            "window.\n\n"
            "To update the dropdown menu's options after adding sources "
            "through obs, press the refresh arrow.")
