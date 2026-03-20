import os

dataset_path = "data/plantvillage_dataset/color"

# Get all class folders sorted
all_classes = sorted([
    d for d in os.listdir(dataset_path)
    if os.path.isdir(os.path.join(dataset_path, d))
])

# Group by plant
plant_groups = {}
for cls in all_classes:
    plant = cls.split("___")[0]
    if plant not in plant_groups:
        plant_groups[plant] = []
    plant_groups[plant].append(cls)

# Print ready-to-paste model_config.py code
print("# Auto-generated class lists\n")

var_names = {}
for plant, classes in plant_groups.items():
    # Make a clean variable name e.g. "Corn_(maize)" → "corn_class"
    var_name = plant.split("_(")[0].lower() + "_class"
    var_names[plant] = var_name
    print(f"{var_name} = [")
    for cls in classes:
        print(f"    '{cls}',")
    print("]\n")

print("ALL_CLASSES = [")
for plant, var_name in var_names.items():
    print(f"    *{var_name},")
print("]")
