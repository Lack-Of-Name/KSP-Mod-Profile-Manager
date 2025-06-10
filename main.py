import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
from datetime import datetime
import re
import ctypes
import platform
import sys

DEBUG_MODE = "-d" in sys.argv

# --- UI Settings ---
UI_FONT = ("Helvetica", 10)
UI_WIDTH = 25

BASE_DIR = Path(__file__).resolve().parent
MODS_DIR = BASE_DIR / "mods"
INSTANCES_FILE = BASE_DIR / "instances.json"
PROFILES_DIR = BASE_DIR / "profiles"
BACKUPS_DIR = BASE_DIR / "backups"

for folder in [MODS_DIR, PROFILES_DIR, BACKUPS_DIR]:
    folder.mkdir(exist_ok=True)

class ModSelectionDialog:
    def __init__(self, parent, available_mods, title="Select Mods"):
        self.result = None
        self.selected_mods = []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.setup_ui(available_mods)
        
    def setup_ui(self, available_mods):
        # Instructions
        instruction_label = tk.Label(
            self.dialog, 
            text="Select mods to include in the profile:",
            font=("Helvetica", 10, "bold")
        )
        instruction_label.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.dialog)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_mods)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=5)
        
        # Selection buttons frame
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        select_all_btn = tk.Button(button_frame, text="Select All", command=self.select_all)
        select_all_btn.pack(side="left", padx=5)
        
        select_none_btn = tk.Button(button_frame, text="Select None", command=self.select_none)
        select_none_btn.pack(side="left", padx=5)
        
        # Listbox with checkboxes (using Listbox for simplicity)
        list_frame = tk.Frame(self.dialog)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.mods_listbox = tk.Listbox(
            list_frame, 
            selectmode=tk.MULTIPLE,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 9)
        )
        self.mods_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.mods_listbox.yview)
        
        # Store original mod list for filtering
        self.all_mods = sorted(available_mods, key=lambda x: x.lower())
        self.populate_mods(self.all_mods)
        
        # Bottom buttons
        bottom_frame = tk.Frame(self.dialog)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        cancel_btn = tk.Button(bottom_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side="right", padx=5)
        
        ok_btn = tk.Button(bottom_frame, text="Create Profile", command=self.ok, bg="lightgreen")
        ok_btn.pack(side="right", padx=5)
        
        # Selected count label
        self.count_label = tk.Label(bottom_frame, text="0 mods selected", fg="blue")
        self.count_label.pack(side="left")
        
        # Bind selection event to update count
        self.mods_listbox.bind("<<ListboxSelect>>", self.update_selection_count)
        
    def populate_mods(self, mods):
        self.mods_listbox.delete(0, tk.END)
        for mod in mods:
            self.mods_listbox.insert(tk.END, mod)
            
    def filter_mods(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            filtered_mods = self.all_mods
        else:
            filtered_mods = [mod for mod in self.all_mods if search_term in mod.lower()]
        self.populate_mods(filtered_mods)
        
    def select_all(self):
        self.mods_listbox.selection_set(0, tk.END)
        self.update_selection_count()
        
    def select_none(self):
        self.mods_listbox.selection_clear(0, tk.END)
        self.update_selection_count()
        
    def update_selection_count(self, event=None):
        count = len(self.mods_listbox.curselection())
        self.count_label.config(text=f"{count} mods selected")
        
    def ok(self):
        # Get selected mods
        selected_indices = self.mods_listbox.curselection()
        self.selected_mods = [self.mods_listbox.get(i) for i in selected_indices]
        self.result = "ok"
        self.dialog.destroy()
        
    def cancel(self):
        self.result = "cancel"
        self.dialog.destroy()
        
    def show(self):
        self.dialog.wait_window()
        return self.result, self.selected_mods

# Updated new_profile method for the App class
def new_profile_enhanced(self):
    instance = self.instance_var.get()
    if not instance:
        return messagebox.showerror("Error", "Select instance")
    
    # Create a menu to choose profile creation method
    choice_dialog = tk.Toplevel(self.root)
    choice_dialog.title("Create New Profile")
    choice_dialog.geometry("300x200")
    choice_dialog.transient(self.root)
    choice_dialog.grab_set()
    
    # Center the dialog
    choice_dialog.update_idletasks()
    x = (choice_dialog.winfo_screenwidth() // 2) - (300 // 2)
    y = (choice_dialog.winfo_screenheight() // 2) - (150 // 2)
    choice_dialog.geometry(f"300x200+{x}+{y}")
    
    result = {"choice": None}
    
    def choice_made(choice):
        result["choice"] = choice
        choice_dialog.destroy()
    
    # Instructions
    tk.Label(
        choice_dialog, 
        text="How would you like to create the profile?",
        font=("Helvetica", 10, "bold")
    ).pack(pady=10)
    
    # Buttons
    button_frame = tk.Frame(choice_dialog)
    button_frame.pack(expand=True)
    
    blank_btn = tk.Button(
        button_frame, 
        text="Create Blank Profile", 
        command=lambda: choice_made("blank"),
        width=20,
        bg="lightblue"
    )
    blank_btn.pack(pady=5)
    
    select_btn = tk.Button(
        button_frame, 
        text="Choose from Cached Mods", 
        command=lambda: choice_made("select"),
        width=20,
        bg="lightgreen"
    )
    select_btn.pack(pady=5)
    
    cancel_btn = tk.Button(
        button_frame, 
        text="Cancel", 
        command=lambda: choice_made("cancel"),
        width=20
    )
    cancel_btn.pack(pady=5)
    
    choice_dialog.wait_window()
    
    if result["choice"] == "cancel" or not result["choice"]:
        return
    
    # Get profile name
    profile_name = simpledialog.askstring("Profile Name", "Enter profile name:")
    if not profile_name:
        return
        
    # Check if profile already exists
    profile_file = PROFILES_DIR / instance / f"{profile_name}.json"
    if profile_file.exists():
        if not messagebox.askyesno("Profile Exists", f"Profile '{profile_name}' already exists. Overwrite?"):
            return
    
    if result["choice"] == "blank":
        # Create empty profile
        save_profile(instance, profile_name, [])
        self.update_profiles(instance)
        self.set_profile(profile_name)
        messagebox.showinfo("Profile Created", f"Empty profile '{profile_name}' created.")
        
    elif result["choice"] == "select":
        # Get available mods from mods folder
        available_mods = []
        if MODS_DIR.exists():
            available_mods = [item.name for item in MODS_DIR.iterdir() 
                            if item.is_dir() or item.is_file()]
        
        if not available_mods:
            messagebox.showinfo("No Mods", "No mods found in the mods folder. Add some mods first.")
            return
            
        # Show mod selection dialog
        dialog = ModSelectionDialog(self.root, available_mods, f"Select Mods for '{profile_name}'")
        result_action, selected_mods = dialog.show()
        
        if result_action == "ok":
            # Create profile with selected mods
            save_profile(instance, profile_name, selected_mods)
            self.update_profiles(instance)  
            self.set_profile(profile_name)
            messagebox.showinfo(
                "Profile Created", 
                f"Profile '{profile_name}' created with {len(selected_mods)} mod(s)."
            )

if not INSTANCES_FILE.exists():
    with open(INSTANCES_FILE, 'w') as f:
        json.dump({}, f)

def load_instances():
    with open(INSTANCES_FILE) as f:
        return json.load(f)

def save_instances(data):
    with open(INSTANCES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def list_instances():
    return list(load_instances().keys())

def list_profiles(instance):
    profile_path = PROFILES_DIR / instance
    profile_path.mkdir(exist_ok=True)
    # Only return profiles that actually exist as JSON files
    profiles = sorted([p.stem for p in profile_path.glob("*.json")])
    
    # Get the active profile and put it first if it exists
    instances = load_instances()
    active_profile = instances.get(instance, {}).get("active_profile")
    if active_profile and active_profile in profiles:
        profiles.remove(active_profile)
        profiles.insert(0, active_profile)
    
    return profiles

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def confirm_and_remove_instance(instance):
    if not instance:
        return
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove instance '{instance}'?"):
        data = load_instances()
        data.pop(instance, None)
        save_instances(data)
        shutil.rmtree(PROFILES_DIR / instance, ignore_errors=True)
        shutil.rmtree(Path(data.get(instance, {}).get("path", "")), ignore_errors=True)

def confirm_and_remove_profile(instance, profile):
    if not instance or not profile:
        return
    path = PROFILES_DIR / instance / f"{profile}.json"
    if not path.exists():
        return
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete profile '{profile}'?"):
        path.unlink()

def safe_remove_item(item_path):
    """Safely remove a file or directory, handling various edge cases"""
    try:
        if item_path.is_symlink():
            item_path.unlink()
        elif item_path.is_dir():
            # For directories, use shutil.rmtree with error handling
            def handle_remove_readonly(func, path, exc):
                if os.path.exists(path):
                    os.chmod(path, 0o777)
                    func(path)
            shutil.rmtree(item_path, onerror=handle_remove_readonly)
        elif item_path.is_file():
            # Handle read-only files
            if not os.access(item_path, os.W_OK):
                os.chmod(item_path, 0o777)
            item_path.unlink()
    except Exception as e:
        raise Exception(f"Failed to remove {item_path}: {e}")

def safe_copy_item(src, dst):
    """Safely copy a file or directory with comprehensive error handling"""
    try:
        # Ensure destination parent directory exists
        dst.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove destination if it exists
        if dst.exists():
            safe_remove_item(dst)
        
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
            
    except Exception as e:
        raise Exception(f"Failed to copy {src} to {dst}: {e}")

def apply_profile(instance, profile_name, status_callback):
    instances = load_instances()
    instance_path = Path(instances[instance]['path'])
    instance_gamedata = instance_path / "GameData"
    profile_file = PROFILES_DIR / instance / f"{profile_name}.json"

    if not profile_file.exists():
        messagebox.showerror("Error", f"Profile file not found: {profile_file}")
        return

    # Ensure GameData directory exists
    if not instance_gamedata.exists():
        messagebox.showerror("Error", f"GameData folder not found: {instance_gamedata}")
        return

    with open(profile_file) as f:
        mods_to_apply = json.load(f)

    status_callback("Cleaning existing GameData...")
    
    # Clean GameData (keep Squad folder and any other stock folders)
    items_to_remove = []
    for item in instance_gamedata.iterdir():
        if item.name not in ["Squad", "SquadExpansion"]:  # Keep stock KSP folders
            items_to_remove.append(item)
    
    # Remove existing mod folders/files
    for item in items_to_remove:
        try:
            safe_remove_item(item)
            status_callback(f"Removed {item.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove {item.name}: {e}")
            return

    status_callback("Applying mods to GameData...")
    
    # Copy mods from mods directory to GameData
    applied_count = 0
    for mod_name in mods_to_apply:
        mod_path = MODS_DIR / mod_name
        target_path = instance_gamedata / mod_name

        if not mod_path.exists():
            messagebox.showwarning("Missing Mod", f"Mod not found in 'mods' folder: {mod_name}")
            continue

        try:
            status_callback(f"Applying {mod_name}...")
            safe_copy_item(mod_path, target_path)
            applied_count += 1
            status_callback(f"Applied {mod_name}")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to apply {mod_name}: {e}")
            # Continue with other mods instead of stopping completely
            continue

    # Update the active profile
    instances[instance]['active_profile'] = profile_name
    save_instances(instances)
    
    if applied_count == len(mods_to_apply):
        status_callback(f"Profile '{profile_name}' applied successfully with {applied_count} mod(s).")
    else:
        status_callback(f"Profile '{profile_name}' partially applied: {applied_count}/{len(mods_to_apply)} mod(s).")
    
    messagebox.showinfo("Apply Complete", f"Applied {applied_count} out of {len(mods_to_apply)} mods from profile '{profile_name}'.")

def backup_gamedata(instance, profile_name=None):
    instances = load_instances()
    instance_path = Path(instances[instance]['path'])
    instance_gamedata = instance_path / "GameData"
    
    if not instance_gamedata.exists():
        messagebox.showerror("Error", f"GameData folder not found: {instance_gamedata}")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    profile_part = f"-{profile_name}" if profile_name else ""
    backup_path = BACKUPS_DIR / f"{instance}{profile_part}-{timestamp}.zip"
    
    try:
        shutil.make_archive(str(backup_path).replace(".zip", ""), 'zip', instance_gamedata)
        messagebox.showinfo("Backup Complete", f"GameData backed up to: {backup_path}")
    except Exception as e:
        messagebox.showerror("Backup Error", f"Failed to create backup: {e}")

def save_profile(instance, profile_name, mods):
    profile_path = PROFILES_DIR / instance
    profile_path.mkdir(exist_ok=True)
    mods_sorted = sorted(mods, key=natural_sort_key)
    with open(profile_path / f"{profile_name}.json", 'w') as f:
        json.dump(mods_sorted, f, indent=2)

def cleanup_unused_mods(status_callback=None):
    """Remove mods from the mods folder that aren't referenced in any profile"""
    if status_callback:
        status_callback("Scanning profiles for used mods...")
    
    # Get all mods referenced in all profiles
    used_mods = set()
    instances = load_instances()
    
    for instance_name in instances.keys():
        profile_path = PROFILES_DIR / instance_name
        if profile_path.exists():
            for profile_file in profile_path.glob("*.json"):
                try:
                    with open(profile_file) as f:
                        mods = json.load(f)
                        used_mods.update(mods)
                except Exception as e:
                    if status_callback:
                        status_callback(f"Warning: Could not read {profile_file}: {e}")
    
    # Get all mods in the mods folder
    if not MODS_DIR.exists():
        return
    
    existing_mods = set(item.name for item in MODS_DIR.iterdir() if item.is_dir() or item.is_file())
    
    # Find unused mods
    unused_mods = existing_mods - used_mods
    
    if not unused_mods:
        if status_callback:
            status_callback("No unused mods found.")
        return
    
    # Ask user for confirmation
    unused_list = sorted(list(unused_mods), key=natural_sort_key)
    message = f"Found {len(unused_mods)} unused mod(s) in the mods folder:\n\n"
    message += "\n".join(unused_list[:10])  # Show first 10
    if len(unused_list) > 10:
        message += f"\n... and {len(unused_list) - 10} more"
    message += "\n\nDelete these unused mods?"
    
    result = messagebox.askyesno("Clean Up Unused Mods", message, icon='question')
    
    if result:
        deleted_count = 0
        for mod_name in unused_mods:
            mod_path = MODS_DIR / mod_name
            try:
                if status_callback:
                    status_callback(f"Removing unused mod: {mod_name}")
                safe_remove_item(mod_path)
                deleted_count += 1
            except Exception as e:
                if status_callback:
                    status_callback(f"Failed to remove {mod_name}: {e}")
                messagebox.showwarning("Removal Failed", f"Failed to remove {mod_name}: {e}")
        
        if status_callback:
            status_callback(f"Cleanup complete. Removed {deleted_count} unused mod(s).")
        messagebox.showinfo("Cleanup Complete", f"Successfully removed {deleted_count} unused mod(s).")
    else:
        if status_callback:
            status_callback("Cleanup cancelled.")

def update_profile(instance, profile_name, status_callback):
    status_callback("Updating profile from GameData...")
    instances = load_instances()
    instance_path = Path(instances[instance]['path'])
    instance_gamedata = instance_path / "GameData"

    if not instance_gamedata.exists():
        messagebox.showerror("Error", f"GameData folder not found: {instance_gamedata}")
        return

    updated_mods = []
    
    # Process each item in GameData (except Squad)
    for item in instance_gamedata.iterdir():
        if item.name == "Squad":
            continue
            
        mod_dest = MODS_DIR / item.name
        
        # If mod doesn't exist in mods folder, copy it there
        if not mod_dest.exists():
            try:
                status_callback(f"Adding {item.name} to mods folder...")
                safe_copy_item(item, mod_dest)
            except Exception as e:
                messagebox.showwarning("Copy Warning", f"Failed to copy {item.name} to mods folder: {e}")
                continue
        
        updated_mods.append(item.name)

    updated_mods = sorted(updated_mods, key=natural_sort_key)

    # Check if profile exists and ask for confirmation
    profile_file = PROFILES_DIR / instance / f"{profile_name}.json"
    if profile_file.exists():
        result = messagebox.askquestion(
            "Overwrite Profile?",
            f"Profile '{profile_name}' already exists. Do you want to overwrite it?",
            icon='warning'
        )
        if result != 'yes':
            status_callback("Update cancelled.")
            return

    # Save the updated profile
    save_profile(instance, profile_name, updated_mods)
    instances = load_instances()
    instances[instance]['active_profile'] = profile_name
    save_instances(instances)
    
    status_callback(f"Profile '{profile_name}' updated with {len(updated_mods)} mod(s).")

def validate_ksp_installation(exe_path):
    """Validate that the selected executable is a valid KSP installation"""
    exe_path = Path(exe_path)
    
    # Check if it's an executable file
    if not exe_path.suffix.lower() == '.exe':
        return False, "Please select a .exe file"
    
    # Check if the file exists
    if not exe_path.exists():
        return False, "Selected file does not exist"
    
    # Check for common KSP executable names
    valid_names = ['ksp.exe', 'ksp_x64.exe', 'kerbal space program.exe']
    if exe_path.name.lower() not in valid_names:
        # Show warning but don't block - user might have renamed the exe
        result = messagebox.askquestion(
            "Unusual Executable Name",
            f"The selected file '{exe_path.name}' doesn't match common KSP executable names.\n"
            f"Expected names: {', '.join(valid_names)}\n\n"
            f"Continue anyway?",
            icon='warning'
        )
        if result != 'yes':
            return False, "Selection cancelled"
    
    # Check if GameData folder exists in the same directory
    gamedata_path = exe_path.parent / "GameData"
    if not gamedata_path.exists() or not gamedata_path.is_dir():
        return False, f"GameData folder not found in {exe_path.parent}"
    
    # Check if GameData contains Squad folder (indicates valid KSP installation)
    squad_path = gamedata_path / "Squad"
    if not squad_path.exists() or not squad_path.is_dir():
        result = messagebox.askquestion(
            "Missing Squad Folder",
            f"GameData folder found, but it doesn't contain a 'Squad' folder.\n"
            f"This might not be a valid KSP installation.\n\n"
            f"Continue anyway?",
            icon='warning'
        )
        if result != 'yes':
            return False, "Selection cancelled"
    
    return True, exe_path.parent

def elevate_privileges():
    if os.name == 'nt' and not ctypes.windll.shell32.IsUserAnAdmin():
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()

def handle_exception(exc):
    if DEBUG_MODE:
        import traceback
        print("An error occurred:")
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        input("Press Enter to exit...")
    else:
        raise exc  # re-raise for normal error handling

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 10
        y = self.widget.winfo_rooty()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left', background="#ffffe0", relief='solid', borderwidth=1, font=UI_FONT)
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class App:
    def __init__(self, root):
        self.root = root
        header_frame = tk.Frame(root)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.instance_var = tk.StringVar()
        self.instance_var.set("")

        self.instance_menu = tk.OptionMenu(header_frame, self.instance_var, "")
        self.instance_menu.config(width=UI_WIDTH, font=UI_FONT)
        self.instance_menu.grid(row=0, column=0, sticky="ew")

        btn_new_instance = tk.Button(header_frame, text="+", command=self.new_instance, bg="lightgreen", width=2)
        btn_new_instance.grid(row=0, column=1, sticky="w")
        Tooltip(btn_new_instance, "Add new KSP instance by selecting the KSP executable")

        btn_remove_instance = tk.Button(header_frame, text="−", fg="white", bg="red", font=("Helvetica", 10, "bold"),
                                        command=self.remove_instance, width=2)
        btn_remove_instance.grid(row=0, column=2, padx=2)

        # profiles: delay full setup until instance is selected
        self.profile_var = tk.StringVar()
        self.profile_var.set("")
        self.profile_menu = tk.OptionMenu(header_frame, self.profile_var, "")
        self.profile_menu.config(width=UI_WIDTH, font=UI_FONT)
        self.profile_menu.grid(row=0, column=3, sticky="ew")

        btn_new_profile = tk.Button(header_frame, text="+", command=self.new_profile, bg="lightgreen", width=2)
        btn_new_profile.grid(row=0, column=4, sticky="w")

        btn_remove_profile = tk.Button(header_frame, text="−", fg="white", bg="red", font=("Helvetica", 10, "bold"),
                                       command=self.remove_profile, width=2)
        btn_remove_profile.grid(row=0, column=5, padx=2)

        actions_frame = tk.Frame(root)
        actions_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        btn_apply = tk.Button(actions_frame, text="Apply Selected Profile", command=self.apply, width=UI_WIDTH, font=UI_FONT)
        btn_apply.grid(row=0, column=0, sticky="ew")
        Tooltip(btn_apply, "Apply the selected profile's mods to the GameData folder")

        btn_backup = tk.Button(actions_frame, text="Backup GameData", command=self.backup, width=UI_WIDTH, font=UI_FONT)
        btn_backup.grid(row=0, column=1, sticky="ew")
        Tooltip(btn_backup, "Create a zip backup of the current GameData folder")

        btn_update_profile = tk.Button(actions_frame, text="Update Profile from GameData", command=self.update_profile, width=UI_WIDTH, font=UI_FONT)
        btn_update_profile.grid(row=1, column=0, sticky="ew")
        Tooltip(btn_update_profile, "Update the selected profile with current GameData contents")

        btn_cleanup_mods = tk.Button(actions_frame, text="Clean Up Unused Mods", command=self.cleanup_unused_mods, width=UI_WIDTH, font=UI_FONT)
        btn_cleanup_mods.grid(row=1, column=1, sticky="ew")
        Tooltip(btn_cleanup_mods, "Remove mods from the mods folder that aren't used in any profile")

        self.status_label = tk.Label(root, text="Ready", fg="blue", font=UI_FONT)
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.mods_listbox = tk.Listbox(root, width=UI_WIDTH*3, height=10, font=UI_FONT)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=self.mods_listbox.yview)
        self.mods_listbox.configure(yscrollcommand=scrollbar.set)
        self.mods_listbox.grid(row=3, column=0, sticky="nsew")
        scrollbar.grid(row=3, column=1, sticky="ns")

        self.tip_label = tk.Label(root, text="", justify="left", wraplength=200, font=UI_FONT, fg="gray")
        self.tip_label.grid(row=3, column=2, sticky="nw", padx=10)

        # Clean up any invalid active_profile references in instances.json
        instances = load_instances()
        for instance_name, instance_data in instances.items():
            active_prof = instance_data.get("active_profile")
            if active_prof:
                profile_file = PROFILES_DIR / instance_name / f"{active_prof}.json"
                if not profile_file.exists():
                    # Clear invalid active_profile reference
                    instances[instance_name]["active_profile"] = None
        save_instances(instances)

        self.update_instances()

    def cleanup_unused_mods(self):
        cleanup_unused_mods(self.set_status)

    def remove_instance(self):
        instance = self.instance_var.get()
        if not instance:
            return
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to remove instance '{instance}'?"):
            data = load_instances()
            data.pop(instance, None)
            save_instances(data)
            shutil.rmtree(PROFILES_DIR / instance, ignore_errors=True)
            self.update_instances()
            # Reset to first available instance or empty
            instances = list_instances()
            if instances:
                self.set_instance(instances[0])
            else:
                self.instance_var.set("")
                self.profile_var.set("")
                self.mods_listbox.delete(0, tk.END)

    def remove_profile(self):
        instance = self.instance_var.get()
        profile = self.profile_var.get()
        if not instance or not profile:
            return
        path = PROFILES_DIR / instance / f"{profile}.json"
        if not path.exists():
            return
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete profile '{profile}'?"):
            path.unlink()
            self.update_profiles(instance)
            # Clear the mods listbox if no profiles remain
            profiles = list_profiles(instance)
            if not profiles:
                self.profile_var.set("")
                self.mods_listbox.delete(0, tk.END)

    def set_status(self, msg):
        self.status_label.config(text=msg)
        self.root.update_idletasks()

    def update_instances(self):
        menu = self.instance_menu["menu"]
        menu.delete(0, "end")
        instances = list_instances()
        for instance in instances:
            menu.add_command(label=instance, command=lambda value=instance: self.set_instance(value))
        if instances:
            self.set_instance(instances[0])

    def set_instance(self, value):
        self.instance_var.set(value)
        self.update_profiles(value)

    def update_profiles(self, instance):
        profiles = list_profiles(instance)
        menu = self.profile_menu["menu"]
        menu.delete(0, "end")
        for prof in profiles:
            menu.add_command(label=prof, command=lambda value=prof: self.set_profile(value))
        if profiles:
            self.set_profile(profiles[0])
        else:
            self.profile_var.set("")
            self.mods_listbox.delete(0, tk.END)

    def set_profile(self, value):
        self.profile_var.set(value)
        self.show_profile_mods(self.instance_var.get(), value)

    def show_profile_mods(self, instance, profile):
        if not profile:  # Don't try to show mods if no profile is selected
            self.mods_listbox.delete(0, tk.END)
            return
            
        profile_file = PROFILES_DIR / instance / f"{profile}.json"
        self.mods_listbox.delete(0, tk.END)
        if profile_file.exists():
            with open(profile_file) as f:
                mods = json.load(f)
                for mod in mods:
                    self.mods_listbox.insert(tk.END, mod)

    def apply(self):
        instance = self.instance_var.get()
        profile = self.profile_var.get()
        if not instance or not profile:
            return messagebox.showerror("Error", "Select instance and profile")
        apply_profile(instance, profile, self.set_status)

    def backup(self):
        instance = self.instance_var.get()
        profile = self.profile_var.get()
        if not instance:
            return messagebox.showerror("Error", "Select instance")
        backup_gamedata(instance, profile)

    def new_profile(self):
        return new_profile_enhanced(self)

    def new_instance(self):
        # Use file dialog to select KSP executable
        exe_path = filedialog.askopenfilename(
            title="Select KSP Executable (KSP.exe, KSP_x64.exe, etc.)",
            filetypes=[
                ("Executable files", "*.exe"),
                ("All files", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        
        if not exe_path:
            return  # User cancelled
        
        # Validate the selected executable and get the installation path
        is_valid, result = validate_ksp_installation(exe_path)
        
        if not is_valid:
            messagebox.showerror("Invalid KSP Installation", result)
            return
        
        installation_path = result
        
        # Ask for instance name
        name = simpledialog.askstring(
            "Instance Name", 
            f"Name this KSP instance:\n\nLocation: {installation_path}",
            initialvalue=installation_path.name
        )
        
        if name:
            # Check if instance name already exists
            instances = load_instances()
            if name in instances:
                messagebox.showerror("Instance Exists", f"An instance named '{name}' already exists.")
                return
            
            # Save the new instance
            instances[name] = {"path": str(installation_path), "active_profile": None}
            save_instances(instances)
            self.update_instances()
            self.set_instance(name)
            messagebox.showinfo(
                "Instance Added", 
                f"KSP instance '{name}' added successfully!\n\n"
                f"Location: {installation_path}\n"
                f"GameData: {installation_path / 'GameData'}"
            )

    def update_profile(self):
        instance = self.instance_var.get()
        profile = self.profile_var.get()
        if not instance or not profile:
            return messagebox.showerror("Error", "Select instance and profile")
        update_profile(instance, profile, self.set_status)
        # Refresh the mods display
        self.show_profile_mods(instance, profile)

if __name__ == "__main__":
    elevate_privileges()
    try:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    except Exception as e:
        handle_exception(e)