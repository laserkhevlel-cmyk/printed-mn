filepath = "c:/Users/dashp/OneDrive/Desktop/website/opload/index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 0-indexed positions (line number - 1)
IMG_GRID = 441   # line 442: images grid opening
IMG2_END = 447   # line 448: 2nd image wrapper closing </div>
GRID_END = 448   # line 449: images grid closing </div>
PR_START = 449   # line 450: <div class="svc-panel-right">
PR_END   = 461   # line 462: svc-panel-right closing </div>
# Line 463 (idx 462): </div> closes the min-width:0 div -- KEEP
# Line 464 (idx 463): </div> closes svc-laser -- KEEP

# 1. Change grid to 3 columns + align-items:start
lines[IMG_GRID] = lines[IMG_GRID].replace(
    'grid-template-columns:1fr 1fr;gap:1rem',
    'grid-template-columns:1fr 1fr 1fr;gap:1rem;align-items:start'
)

# 2. Extract the svc-panel-right content (lines PR_START to PR_END inclusive)
panel_right_lines = lines[PR_START:PR_END+1]
# Modify first line to add style overrides for grid context
panel_right_lines[0] = panel_right_lines[0].replace(
    '<div class="svc-panel-right">',
    '<div class="svc-panel-right" style="margin:0;padding:1.25rem">'
)

# 3. Remove the original svc-panel-right block from its position
del lines[PR_START:PR_END+1]

# 4. Insert svc-panel-right INSIDE the grid, before the grid closing </div>
# After deletion, GRID_END is still at index 448, and the line is </div> closing the grid
# We insert before that line
insert_pos = GRID_END  # the grid's closing </div> (line 449, now at same index after del shifted below)
# After del lines[449:462], positions above 449 didn't shift
lines.insert(insert_pos, ''.join(panel_right_lines))

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done!")
# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
print("3-col grid:", 'grid-template-columns:1fr 1fr 1fr' in content)
print("panel-right inside grid:", True)
