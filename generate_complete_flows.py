import json
import os
import copy

OUTPUT_PATH = 'docs/diagrams/complete-user-flows.excalidraw'

def create_element(id, type, x, y, width, height, text=None, fontSize=16, backgroundColor="transparent", strokeColor="#000000", strokeStyle="solid", strokeWidth=1):
    element = {
        "id": id,
        "type": type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": strokeColor,
        "backgroundColor": backgroundColor,
        "fillStyle": "hachure",
        "strokeWidth": strokeWidth,
        "strokeStyle": strokeStyle,
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "strokeSharpness": "sharp",
        "seed": 12345,
        "version": 1,
        "versionNonce": 0,
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False
    }
    
    if type == "text":
        element.update({
            "text": text,
            "fontSize": fontSize,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "baseline": fontSize * 0.8
        })
    elif type == "arrow":
        element.update({
            "points": [[0, 0], [width, height]],
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow"
        })
        
    return element

def create_screen(screen_id, title, x, y, components):
    elements = []
    # Frame
    elements.append(create_element(f"{screen_id}-frame", "rectangle", x, y, 350, 500, backgroundColor="transparent"))
    # Title
    elements.append(create_element(f"{screen_id}-title", "text", x + 10, y + 10, 200, 30, text=f"{screen_id}: {title}", fontSize=20))
    # Reset text alignment for title
    elements[-1]["textAlign"] = "left"
    elements[-1]["verticalAlign"] = "top"
    
    current_y = y + 50
    for comp_name in components:
        # Box
        elements.append(create_element(f"{screen_id}-box-{comp_name}", "rectangle", x + 20, current_y, 310, 40, backgroundColor="#f0f0f0"))
        # Text
        elements.append(create_element(f"{screen_id}-text-{comp_name}", "text", x + 30, current_y + 10, 200, 24, text=comp_name))
        # Reset text alignment for components
        elements[-1]["textAlign"] = "left"
        elements[-1]["verticalAlign"] = "top"
        current_y += 50
        
    return elements

def create_arrow(x, y, width, label=None):
    elements = []
    arrow = create_element(f"arrow-{x}-{y}", "arrow", x, y, width, 0)
    elements.append(arrow)
    
    if label:
        text_x = x + (width / 2) - (len(label) * 4)
        text_y = y - 25
        elements.append(create_element(f"label-{x}-{y}", "text", text_x, text_y, 100, 20, text=label, fontSize=16))
        
    return elements

def create_action_box(id, text, x, y, color="#E6E6FA"):
    elements = []
    elements.append(create_element(f"box-{id}", "rectangle", x, y, 200, 80, backgroundColor=color, strokeStyle="dashed"))
    elements.append(create_element(f"text-{id}", "text", x + 10, y + 20, 180, 40, text=text, fontSize=14))
    return elements

def create_notification_box(id, text, x, y):
    elements = []
    # Phone shape
    elements.append(create_element(f"phone-{id}", "rectangle", x, y, 200, 100, backgroundColor="#FFFFFF", strokeWidth=2))
    # Screen
    elements.append(create_element(f"screen-{id}", "rectangle", x + 10, y + 10, 180, 80, backgroundColor="#F0F8FF"))
    # Text
    elements.append(create_element(f"text-{id}", "text", x + 20, y + 30, 160, 40, text=f"🔔 {text}", fontSize=14))
    return elements

def main():
    new_elements = []
    
    # --- Flow 1: Happy Flow ---
    y_row1 = 100
    x_start = 50
    gap = 100
    screen_w = 350
    action_w = 200
    
    # Title
    new_elements.append(create_element("title-happy", "text", x_start, y_row1 - 60, 500, 40, text="1. Happy Flow: Apply -> Approve -> WhatsApp -> Confirm", fontSize=24))
    new_elements[-1]["textAlign"] = "left"

    # 1. NA-06 (Available Shifts)
    na06_comps = ["Shift Cards List", "Filter/Sort", "Apply Button", "Conflict Warning"]
    new_elements.extend(create_screen("NA-06", "Available Shifts", x_start, y_row1, na06_comps))
    
    # Arrow
    arrow_x = x_start + screen_w
    arrow_y = y_row1 + 250
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Select"))
    
    # 2. NA-07 (Shift Details)
    x_pos = x_start + screen_w + gap
    na07_comps = ["Full Details", "Map", "Docs List", "Penalty Warning", "Apply Button"]
    new_elements.extend(create_screen("NA-07", "Shift Details", x_pos, y_row1, na07_comps))
    
    # Arrow
    arrow_x = x_pos + screen_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Apply"))
    
    # 3. ADM-05 (Job Details - Generated)
    x_pos += screen_w + gap
    adm05_components = [
        "Job Summary Header",
        "Applicant: Chan Tai Man",
        "Score: 95 | History: Good",
        "Approve Button (Green)",
        "Reject Button (Red)",
        "Assigned Staff List",
        "Unfilled Alert"
    ]
    new_elements.extend(create_screen("ADM-05", "Job Applications", x_pos, y_row1, adm05_components))
    
    # Arrow
    arrow_x = x_pos + screen_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Approve"))
    
    # 4. ADM Action: WhatsApp Template
    x_pos += screen_w + gap
    new_elements.extend(create_action_box("ADM-WhatsApp", "System Generates\nWhatsApp Template", x_pos, y_row1 + 210))
    
    # Arrow
    arrow_x = x_pos + action_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Send"))
    
    # 5. NA Notification
    x_pos += action_w + gap
    new_elements.extend(create_notification_box("NA-Notif-1", "WhatsApp/Push:\nAssignment Confirmed!", x_pos, y_row1 + 200))
    
    # Arrow
    arrow_x = x_pos + action_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "View"))

    # 6. NA-08 (My Shifts - Confirmed)
    x_pos += action_w + gap
    na08_comps = ["Tabs: Upcoming/Pending", "Shift Cards", "Cancel Button", "Cancel Modal"]
    new_elements.extend(create_screen("NA-08", "My Shifts", x_pos, y_row1, na08_comps))
    # Add a "Confirmed" badge overlay
    new_elements.append(create_element(f"badge-confirmed-{x_pos}", "rectangle", x_pos + 200, y_row1 + 120, 100, 30, backgroundColor="#90EE90"))
    new_elements.append(create_element(f"text-confirmed-{x_pos}", "text", x_pos + 210, y_row1 + 125, 80, 20, text="Confirmed", fontSize=14))
    new_elements[-1]["textAlign"] = "left"

    # --- Flow 2: Cancel Flow ---
    y_row2 = 800
    x_start = 50
    
    # Title
    new_elements.append(create_element("title-cancel", "text", x_start, y_row2 - 60, 500, 40, text="2. Cancel Flow: Confirmed -> Cancel -> Notify -> Penalty", fontSize=24))
    new_elements[-1]["textAlign"] = "left"
    
    # 1. NA-08 (Confirmed)
    new_elements.extend(create_screen("NA-08-Start", "My Shifts", x_start, y_row2, na08_comps))
    # Add Confirmed Badge
    new_elements.append(create_element(f"badge-confirmed-2-{x_start}", "rectangle", x_start + 200, y_row2 + 120, 100, 30, backgroundColor="#90EE90"))
    new_elements.append(create_element(f"text-confirmed-2-{x_start}", "text", x_start + 210, y_row2 + 125, 80, 20, text="Confirmed", fontSize=14))
    new_elements[-1]["textAlign"] = "left"

    # Arrow
    arrow_x = x_start + screen_w
    arrow_y = y_row2 + 250
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Cancel"))
    
    # 2. Cancel Modal
    x_pos = x_start + screen_w + gap
    modal_components = [
        "Warning: Late Cancellation!",
        "Penalty: -1 Score",
        "Deduction: $300 HKD",
        "[Keep Shift] Button",
        "[Confirm Cancel] Button (Red)"
    ]
    new_elements.extend(create_screen("MODAL", "Cancellation Warning", x_pos, y_row2 + 100, modal_components)) # Smaller/Centered
    
    # Arrow
    arrow_x = x_pos + screen_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Confirm"))
    
    # 3. Notification
    x_pos += screen_w + gap
    new_elements.extend(create_notification_box("NA-Notif-2", "Push:\nCancellation Confirmed\nPenalty Applied", x_pos, y_row2 + 200))
    
    # Arrow
    arrow_x = x_pos + action_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "View"))
    
    # 4. NA-08 (Cancelled)
    x_pos += action_w + gap
    new_elements.extend(create_screen("NA-08-End", "My Shifts", x_pos, y_row2, na08_comps))
    # Add Cancelled Badge
    new_elements.append(create_element(f"badge-cancelled-{x_pos}", "rectangle", x_pos + 200, y_row2 + 120, 100, 30, backgroundColor="#FFB6C1"))
    new_elements.append(create_element(f"text-cancelled-{x_pos}", "text", x_pos + 210, y_row2 + 125, 80, 20, text="Cancelled", fontSize=14))
    new_elements[-1]["textAlign"] = "left"

    # --- Flow 3: Reject Flow ---
    y_row3 = 1500
    x_start = 50
    
    # Title
    new_elements.append(create_element("title-reject", "text", x_start, y_row3 - 60, 500, 40, text="3. Reject Flow: Apply -> Admin Reject -> Notify", fontSize=24))
    new_elements[-1]["textAlign"] = "left"
    
    # 1. NA-07 (Shift Details - Apply)
    new_elements.extend(create_screen("NA-07-Apply", "Shift Details", x_start, y_row3, na07_comps))
    
    # Arrow
    arrow_x = x_start + screen_w
    arrow_y = y_row3 + 250
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Apply"))
    
    # 2. ADM-05 (Job Details - Reject)
    x_pos = x_start + screen_w + gap
    new_elements.extend(create_screen("ADM-05-Reject", "Job Applications", x_pos, y_row3, adm05_components))
    
    # Arrow
    arrow_x = x_pos + screen_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "Reject"))
    
    # 3. Notification
    x_pos += screen_w + gap
    new_elements.extend(create_notification_box("NA-Notif-3", "WhatsApp/Push:\nApplication Declined", x_pos, y_row3 + 200))
    
    # Arrow
    arrow_x = x_pos + action_w
    new_elements.extend(create_arrow(arrow_x + 10, arrow_y, gap - 20, "View"))
    
    # 4. NA-06 (Available Shifts - Back to pool)
    x_pos += action_w + gap
    new_elements.extend(create_screen("NA-06-Back", "Available Shifts", x_pos, y_row3, na06_comps))
    # Label
    new_elements.append(create_element(f"note-reject-{x_pos}", "text", x_pos, y_row3 + 520, 300, 30, text="*Shift remains in Available list", fontSize=16))
    new_elements[-1]["textAlign"] = "left"

    # Save
    output_data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": new_elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": 20
        }
    }
    
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Created {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
