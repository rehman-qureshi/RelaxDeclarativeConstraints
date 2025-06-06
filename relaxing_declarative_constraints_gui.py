import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from find_constraints import find_constraints_function
from find_transitivity import find_transitivity_by_removal
from generate_declare_and_regex import generate_declare_and_regex_function 

# --- Utility Functions ---
check_vars = []
findTransitivityByRemovalSet = set()
directlyFollowSet,eventuallyFollowSet = set(),set()

def create_scrollable_frame(parent):
    outer = ttk.Frame(parent)

    canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Use tk.Frame with matching background
    inner = tk.Frame(canvas, bg="#f0f0f0")
    window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_frame_configure(event):
        # Dynamically update scrollregion to match inner frame size
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        # Ensure inner frame width matches canvas width
        canvas.itemconfig(window_id, width=canvas.winfo_width())

    inner.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return outer, inner


def populate_constraints_frame(frame, dataset, label):
    for widget in frame.winfo_children():
        widget.destroy()

    outer, inner = create_scrollable_frame(frame)
    outer.pack(fill="both", expand=True)
    ttk.Label(inner, text=label, font=('Segoe UI', 10, 'bold')).pack(anchor="w", padx=10, pady=(10, 5))

    for src, tgt in dataset:
        ttk.Label(inner, text=f"{src} → {tgt}").pack(anchor="w", padx=10)
    
def show_tuple_selection(df,last_activities,container, directlyFollowSet, eventuallyFollowSet):
    removedDirectlyFollowSet = set()
    affectedEventuallyFollowSet = set()
    findTransitivityByRemovalSet = set()
    tuple_list = list(directlyFollowSet)
    check_vars.clear()

    frames = {name: ttk.Frame(container, width=300) for name in ("left", "right1", "right2")}
    for frame in frames.values():
        frame.pack(side="left", fill="both", expand=True)

    outer_left, inner_left = create_scrollable_frame(frames["left"])
    ttk.Label(inner_left, text="Directly Follows Constraints", font=('Segoe UI', 10, 'bold')).pack(anchor="w", padx=10, pady=(10, 5))
    outer_left.pack(fill="both", expand=True)

    VISIBLE_COUNT = 100
    current_index = [0]  # Use list to allow mutation in nested functions
    def populate_left_frame():
        for widget in inner_left.winfo_children():
            widget.destroy()
        ttk.Label(inner_left, text="Directly Follows Constraints", font=('Segoe UI', 10, 'bold')).pack(anchor="w", padx=10, pady=(10, 5))
        
        visible_items = tuple_list[current_index[0]:current_index[0] + VISIBLE_COUNT]
        check_vars.clear()

        for src, tgt in visible_items:
            var = tk.BooleanVar()
            ttk.Checkbutton(inner_left, text=f"{src} → {tgt}", variable=var).pack(anchor="w", padx=10)
            check_vars.append(var)

        # Paging buttons
        nav_frame = ttk.Frame(inner_left)
        nav_frame.pack(fill="x", pady=(10, 5))

        def prev_page():
            if current_index[0] - VISIBLE_COUNT >= 0:
                current_index[0] -= VISIBLE_COUNT
                populate_left_frame()

        def next_page():
            if current_index[0] + VISIBLE_COUNT < len(tuple_list):
                current_index[0] += VISIBLE_COUNT
                populate_left_frame()

        ttk.Button(nav_frame, text="Next", command=next_page).pack(side="right", padx=5)
        ttk.Button(nav_frame, text="Previous", command=prev_page).pack(side="right", padx=5)
    
    def populate_right_frames():
        populate_constraints_frame(frames["right1"], eventuallyFollowSet, "Transitive Closed Constraints")
        populate_constraints_frame(frames["right2"], affectedEventuallyFollowSet, "Affected Transitive Closed Constraints")

    populate_left_frame()
    populate_right_frames()

    btn_frame = ttk.Frame(frames["left"])
    btn_frame.pack(fill="x", pady=(1, 1))

    def confirm_action():
        
        selected_indices = [i for i, var in enumerate(check_vars) if var.get()]
        global_indices = [current_index[0] + i for i in selected_indices]

        removed_tuple_list = [tuple_list[i] for i in global_indices]
        remaining = [t for i, t in enumerate(tuple_list) if i not in global_indices]
        tuple_list.clear()
        tuple_list.extend(remaining)

        directlyFollowSet.clear()
        directlyFollowSet.update(tuple_list)
        removedDirectlyFollowSet.update(removed_tuple_list)

        print("Removed Constraints:", removed_tuple_list)

        for value in removedDirectlyFollowSet:
            transitivity = find_transitivity_by_removal(df, value[0], value[1], last_activities)
            findTransitivityByRemovalSet.update(transitivity)

        for val in findTransitivityByRemovalSet:
            if val in eventuallyFollowSet:
                affectedEventuallyFollowSet.add(val)
                eventuallyFollowSet.remove(val)

        check_vars.clear()
        populate_left_frame()
        populate_right_frames()

    def confirm_declare_and_regex():
        generate_declare_and_regex_function(directlyFollowSet)

    ttk.Button(btn_frame, text="Generate Declare and Regex", command=confirm_declare_and_regex).pack(side="left", expand=True, padx=0)
    ttk.Button(btn_frame, text="Cancel", command=lambda: [var.set(False) for var in check_vars]).pack(side="left", expand=True, padx=0)
    ttk.Button(btn_frame, text="Remove", command=confirm_action).pack(side="left", expand=True, padx=0)


# --- Main GUI Setup ---
def main_gui_function(df,last_activities,image_path):

    directlyFollowSet,eventuallyFollowSet=find_constraints_function(df,last_activities)

    root = tk.Tk()
    root.title("Relaxed Declarative Constraints")
    root.state("zoomed")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    petri_frame = ttk.LabelFrame(main_frame, text="Business Process Model")
    petri_frame.pack(fill="both", padx=10, pady=10, expand=True)

    fixed_canvas_width = 600  # Set your desired canvas width
    fixed_canvas_height = 250  # Optional: also control vertical scrolling

    canvas = tk.Canvas(petri_frame, background="white",width=fixed_canvas_width, height=fixed_canvas_height)
    h_scroll = ttk.Scrollbar(petri_frame, orient="horizontal", command=canvas.xview)
    v_scroll = ttk.Scrollbar(petri_frame, orient="vertical", command=canvas.yview)
    canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")
    petri_frame.grid_rowconfigure(0, weight=1)
    petri_frame.grid_columnconfigure(0, weight=1)

    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk

     # Set scroll region to full image dimensions
    canvas.config(scrollregion=(0, 0, img.width, img.height))

    # Enable horizontal scrollbar only if image is wider than canvas
    if img.width > fixed_canvas_width:
        h_scroll.grid(row=1, column=0, sticky="ew")
    else:
        h_scroll.grid_remove()

    tuple_frame = ttk.LabelFrame(main_frame)
    tuple_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    show_tuple_selection(df,last_activities,tuple_frame, directlyFollowSet, eventuallyFollowSet)

    root.mainloop()
