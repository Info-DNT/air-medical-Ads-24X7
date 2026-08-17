import os
import re

def process_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # If Saudi Arabia is already present in this global helpline block, skip
    # We check for +9668001010817 or tel:+9668001010817 to be sure
    if '+9668001010817' in content or '+966 800 101 0817' in content:
        print(f" -> Already has Saudi Arabia helpline. Skipping.")
        return False

    # Find the Kenya section in the footer global helplines.
    # The structure:
    # <a href="tel:+254800230119" ...>
    #     ...Kenya...
    # </a>
    
    # We find '<span class="w-24 inline-block text-white font-normal text-left">Kenya</span>'
    kenya_span = '<span class="w-24 inline-block text-white font-normal text-left">Kenya</span>'
    idx = content.find(kenya_span)
    if idx == -1:
        print(f" -> Could not find Kenya span in {filepath}. Skipping.")
        return False

    # Find the closing </a> after the Kenya span
    close_a_idx = content.find('</a>', idx)
    if close_a_idx == -1:
        print(f" -> Could not find closing </a> after Kenya span in {filepath}. Skipping.")
        return False

    insert_pos = close_a_idx + len('</a>')
    
    # Let's detect the line ending style and indentation of the Kenya block
    # We search backwards from the start of Kenya's '<a>' block
    # Let's find the '<a href="tel:+254800230119"' tag before the span
    a_start_idx = content.rfind('<a href="tel:+254800230119"', 0, idx)
    if a_start_idx == -1:
        # try without tel prefix just in case
        a_start_idx = content.rfind('<a', 0, idx)
        
    if a_start_idx == -1:
        print(f" -> Could not determine start of Kenya link tag in {filepath}. Skipping.")
        return False

    # Get the line leading up to the <a> tag to determine indentation
    line_start_idx = content.rfind('\n', 0, a_start_idx)
    if line_start_idx == -1:
        line_start_idx = 0
    else:
        line_start_idx += 1
        
    indentation = content[line_start_idx:a_start_idx]
    # Check if there is a newline after the </a> tag
    newline_match = re.match(r'^(\r?\n)', content[insert_pos:])
    newline = newline_match.group(1) if newline_match else '\n'

    # Build the Saudi block
    saudi_block = (
        f"{newline}{indentation}<a href=\"tel:+9668001010817\" onclick=\"return gtag_report_phone_conversion(this.href);\""
        f"{newline}{indentation}    class=\"text-white hover:text-secondary transition-colors flex items-center gap-4\">"
        f"{newline}{indentation}    <span class=\"w-24 inline-block text-white font-normal text-left\">Saudi Arabia</span>"
        f"{newline}{indentation}    <span class=\"font-mono text-[13px] tracking-wide\">+966 800 101 0817</span>"
        f"{newline}{indentation}</a>"
    )

    new_content = content[:insert_pos] + saudi_block + content[insert_pos:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f" -> Successfully added Saudi Arabia helpline to {filepath}!")
    return True

def main():
    target_files = []
    # Traverse directories to find HTML files
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                # We skip thank-you.html and index.html as they do not have the helpline footer
                if f in ['thank-you.html', 'index.html']:
                    continue
                path = os.path.join(root, f)
                target_files.append(path)
                
    modified_count = 0
    for path in target_files:
        if process_file(path):
            modified_count += 1
            
    print(f"\nDone! Modified {modified_count} files.")

if __name__ == '__main__':
    main()
