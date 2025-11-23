import re

file_path = 'docs/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find images since we might not have bs4 installed in the environment, 
# but previous logs said bs4 was missing. I will try to use simple string manipulation or regex 
# to be safe and avoid dependency issues if bs4 is not available. 
# Wait, the previous session summary said "Missing BeautifulSoup: The bs4 library was unavailable".
# So I should NOT use bs4. I will use regex.

# Pattern to find img tags with src starting with ./photos/
# We need to capture the full tag to replace it.
# We also need to extract the src to calculate the set and photo number.

def replace_img(match):
    full_tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', full_tag)
    if not src_match:
        return full_tag
    
    src = src_match.group(1)
    
    # Extract set number
    set_match = re.search(r'/photos/set(\d+)/', src)
    if not set_match:
        return full_tag
    
    set_number = set_match.group(1)
    
    # Extract filename (without extension)
    filename_match = re.search(r'/([^/]+)\.[^.]+$', src)
    if not filename_match:
        return full_tag
    
    filename = filename_match.group(1)
    # Sanitize filename for URL (replace spaces with hyphens)
    filename = filename.replace(' ', '-')
    
    # Construct the new data attribute
    new_attr = f'data-slide-url="portfolio-set-{set_number}-photograph-{filename}"'
    
    # Check if data-slide-url already exists
    if 'data-slide-url=' in full_tag:
        # Replace existing
        new_tag = re.sub(r'data-slide-url="[^"]*"', new_attr, full_tag)
    else:
        # Add new
        new_tag = full_tag.replace('<img ', f'<img {new_attr} ')
        
    return new_tag

set_counts = {}

# Regex to match the specific images we are interested in.
pattern = r'<img[^>]+src="\./photos/[^"]+"[^>]*>'

new_content = re.sub(pattern, replace_img, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully updated data-slide-url attributes to use filenames.")
