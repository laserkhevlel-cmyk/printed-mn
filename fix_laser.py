filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find key line indices in the laser panel
img_grid_line = None      # line with 1fr 1fr grid for images
img_grid_end = None       # closing </div> of images grid
panel_right_start = None  # <div class="svc-panel-right">
panel_right_end = None    # closing </div> of svc-panel-right
outer_closes = None       # the </div></div> after panel-right

for i, line in enumerate(lines):
    if 'display:grid;grid-template-columns:1fr 1fr;gap:1rem' in line and img_grid_line is None:
        img_grid_line = i
    if img_grid_line and i > img_grid_line and line.strip() == '</div>' and img_grid_end is None and i > img_grid_line + 3:
        img_grid_end = i
    if 'class="svc-panel-right"' in line and panel_right_start is None and img_grid_line:
        panel_right_start = i
    if panel_right_start and i > panel_right_start and line.strip() == '</div>' and panel_right_end is None and i > panel_right_start + 3:
        panel_right_end = i

print(f"img_grid_line: {img_grid_line+1 if img_grid_line else None}")
print(f"img_grid_end:  {img_grid_end+1 if img_grid_end else None}")
print(f"panel_right_start: {panel_right_start+1 if panel_right_start else None}")
print(f"panel_right_end:   {panel_right_end+1 if panel_right_end else None}")

if not all([img_grid_line, img_grid_end, panel_right_start, panel_right_end]):
    print("ERROR: could not find all markers")
    exit(1)

# Print context
print("\n--- Images grid line ---")
print(repr(lines[img_grid_line][:80]))
print("--- Images grid end ---")
print(repr(lines[img_grid_end]))
print("--- Panel right start ---")
print(repr(lines[panel_right_start][:80]))
print("--- Panel right end ---")
print(repr(lines[panel_right_end]))
print("--- Line after panel_right_end ---")
print(repr(lines[panel_right_end+1]))
print(repr(lines[panel_right_end+2]))
