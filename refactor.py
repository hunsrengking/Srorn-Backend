import os
import shutil
import re

# We will create app/api/ and move files into it.
TARGET_DIR = "app/api"
base_dir = "app"

# Mapping of file names to their respective feature folders
file_to_feature = {
    # Auth
    "auth_controller.py": "auth",
    "auth_routes.py": "auth",
    "auth_service.py": "auth",
    
    # Dashboard
    "dashboard_controller.py": "dashboard",
    "dashboard_route.py": "dashboard",
    "dashboard_service.py": "dashboard",
    
    # Department
    "department_controller.py": "department",
    "department_model.py": "department",
    "department_route.py": "department",
    "departments_schema.py": "department",
    "department_service.py": "department",
    
    # Notification
    "notification_controller.py": "notification",
    "notification_model.py": "notification",
    "notifications_route.py": "notification",
    "notification_schema.py": "notification",
    "notification_service.py": "notification",
    
    # Organization
    "organization_controller.py": "organization",
    "organization_model.py": "organization",
    "organization_route.py": "organization",
    "organization_service.py": "organization",
    
    # Position
    "positions_controller.py": "position",
    "positions_model.py": "position",
    "positions_route.py": "position",
    "position_schema.py": "position",
    "positions_service.py": "position",
    
    # Report
    "report_controller.py": "report",
    "report_route.py": "report",
    "report_service.py": "report",
    
    # Role
    "role_controller.py": "role",
    "role_model.py": "role",
    "role_route.py": "role",
    "role_schema.py": "role",
    "role_service.py": "role",
    "permission_schema.py": "role",
    
    # Staff
    "staff_controller.py": "staff",
    "staff_model.py": "staff",
    "staff_route.py": "staff",
    "staff_schema.py": "staff",
    "staff_service.py": "staff",
    
    # Status
    "status_controller.py": "status",
    "status_route.py": "status",
    "status_schema.py": "status",
    "status_service.py": "status",
    
    # Student
    "student_controller.py": "student",
    "student_model.py": "student",
    "student_route.py": "student",
    "student_schema.py": "student",
    "student_service.py": "student",
    "print_card_schema.py": "student",
    
    # Telegram
    "telegram_controller.py": "telegram",
    "telegram_model.py": "telegram",
    "telegram_route.py": "telegram",
    "telegram_schema.py": "telegram",
    "telegram_service.py": "telegram",
    
    # Ticket
    "ticket_controller.py": "ticket",
    "ticket_model.py": "ticket",
    "ticket_route.py": "ticket",
    "ticket_schema.py": "ticket",
    "ticket_service.py": "ticket",
    "ticket_mail_service.py": "ticket",
    "category_schema.py": "ticket",
    "item_schema.py": "ticket",
    "priority_schema.py": "ticket",
    
    # User
    "user_controller.py": "user",
    "user_model.py": "user",
    "user_routes.py": "user",
    "user_schema.py": "user",
    "user_service.py": "user",
}

layers = ["controllers", "models", "routes", "schema", "services"]

# Create API directory
os.makedirs(TARGET_DIR, exist_ok=True)

# 1. Move files and build a dictionary of old module path to new module path
module_replacements = {}  # e.g., "app.controllers.user_controller": "app.api.user.user_controller"
module_dir_replacements = {} # e.g. "app.controllers": { "user_controller": "app.api.user" }

for layer in layers:
    layer_dir = os.path.join(base_dir, layer)
    if not os.path.exists(layer_dir):
        continue
    for filename in os.listdir(layer_dir):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue
        
        feature = file_to_feature.get(filename)
        if not feature:
            print(f"Warning: No mapping for {filename} in {layer}, placing in 'shared'")
            feature = "shared"
            
        feature_dir = os.path.join(TARGET_DIR, feature)
        os.makedirs(feature_dir, exist_ok=True)
        
        # Move file
        src = os.path.join(layer_dir, filename)
        dst = os.path.join(feature_dir, filename)
        shutil.move(src, dst)
        
        # Register module replacement
        mod_name = filename[:-3] # remove .py
        old_mod_path = f"app.{layer}.{mod_name}"
        new_mod_path = f"app.api.{feature}.{mod_name}"
        module_replacements[old_mod_path] = new_mod_path
        
        # Register dir replacement
        old_dir_path = f"app.{layer}"
        if old_dir_path not in module_dir_replacements:
            module_dir_replacements[old_dir_path] = {}
        module_dir_replacements[old_dir_path][mod_name] = f"app.api.{feature}"

        # Touch __init__.py inside feature dir
        open(os.path.join(feature_dir, "__init__.py"), "a").close()

# 2. Update all imports in new files and main.py
def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # We need to replace imports like:
    # 1. from app.controllers import user_controller -> from app.api.user import user_controller
    # 2. from app.models.user_model import * -> from app.api.user.user_model import *
    # 3. import app.schema.user_schema -> import app.api.user.user_schema
    # 4. app.schema.user_schema (in code) -> app.api.user.user_schema
    
    for old_dir_path, mods in module_dir_replacements.items():
        # Handle `from app.layer import mod1, mod2`
        # It's tricky because multiple modules might go to different features.
        # So we better replace `from app.layer import mod1` with `from app.api.feature import mod1`
        # If there are multi-imports like `from app.routes import org_route, user_routes`,
        # they might need to be split. But let's first see if we can just string replace the simplest case.
        pass

    # Actually, a simpler approach for code text replaces:
    # `app.controllers.user_controller` -> `app.api.user.user_controller`
    # `from app.controllers import user_controller` -> `from app.api.user import user_controller`
    # Wait, what if they did:
    # from app.routes import (
    #     organization_route,
    #     student_route,
    # )
    # This is in main.py, so we must handle main.py specifically or cautiously.

    # Let's do a naive string replace first for the exact module path
    for old_path, new_path in module_replacements.items():
        content = content.replace(old_path, new_path)

    # For `from app.layer import mod`
    for old_dir_path, mods in module_dir_replacements.items():
        for mod, new_dir_path in mods.items():
            # pattern: from app.controllers import mod
            pattern1 = rf"from\s+{old_dir_path}\s+import\s+((?:[\w_]+,\s*)*){mod}((?:,\s*[\w_]+)*)"
            
            # This is complex with regex. Let's do a safer substitution logic.
            # Instead of a complex regex, we'll find lines starting with `from app.layer import`
            pass
            
    # Simpler textual fix for `from app.layer import mod` that's not grouped
    # We'll just read line by line, if it matches, replace it.
    lines = content.split('\n')
    new_lines = []
    
    # A tiny parser for `from app.routes import (...)` block
    in_import_block = False
    current_block_layer = None
    
    for line in lines:
        if in_import_block:
            if ')' in line:
                in_import_block = False
            # process individual lines in block
            stripped = line.strip().strip(',')
            if current_block_layer in module_dir_replacements and stripped in module_dir_replacements[current_block_layer]:
                new_dir = module_dir_replacements[current_block_layer][stripped]
                new_lines.append(f"from {new_dir} import {stripped}")
            else:
                if stripped:
                     # fallback
                     new_lines.append(line)
            continue
            
        match = re.search(r'^from\s+(app\.\w+)\s+import\s+\((.*)', line)
        if match:
            in_import_block = True
            current_block_layer = match.group(1)
            # handle the rest of the line if there's any
            continue
            
        match_simple = re.search(r'^from\s+(app\.\w+)\s+import\s+([\w_]+)(.*)', line)
        if match_simple:
            layer = match_simple.group(1)
            mod = match_simple.group(2)
            rest = match_simple.group(3)
            # if multiple modules on one line like `from app.routes import a, b`, we split them.
            if ',' in rest or layer not in module_dir_replacements:
                # If there are multiple like from app.routes import org_route, user_routes
                mods_on_line = [m.strip() for m in line.replace(f"from {layer} import", "").split(',')]
                for m in mods_on_line:
                    if m in module_dir_replacements.get(layer, {}):
                        new_dir = module_dir_replacements[layer][m]
                        new_lines.append(f"from {new_dir} import {m}")
                    elif m:
                        new_lines.append(f"from {layer} import {m}")
            else:
                if mod in module_dir_replacements.get(layer, {}):
                    new_dir = module_dir_replacements[layer][mod]
                    new_lines.append(f"from {new_dir} import {mod}{rest}")
                else:
                    new_lines.append(line)
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)

    # Finally, replace exact module strings
    for old_path, new_path in module_replacements.items():
        content = content.replace(old_path, new_path)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# Process all newly moved files
for root, dirs, files in os.walk(TARGET_DIR):
    for f in files:
        if f.endswith(".py"):
            process_file(os.path.join(root, f))

# Process main.py
if os.path.exists("app/main.py"):
    process_file("app/main.py")

# Optionally remove old dirs
for layer in layers:
    layer_dir = os.path.join(base_dir, layer)
    if os.path.exists(layer_dir):
        # Check if dir is empty except __init__.py and __pycache__
        for root, dirs, files in os.walk(layer_dir, topdown=False):
            for name in files:
                if name not in ("__init__.py") and not name.endswith(".pyc"):
                    print(f"File left behind: {os.path.join(root, name)}")
        # We can safely delete it or leave it to the user.
        # Let's try to remove if it's mostly empty.
        shutil.rmtree(layer_dir, ignore_errors=True)

print("Refactoring complete.")
