import os
import re

def deploy_page(src_filename, dest_filename):
    src_path = os.path.join("national", src_filename)
    dest_path = os.path.join("uae-only-deploy", dest_filename)
    
    if not os.path.exists(src_path):
        print(f"Source file {src_path} does not exist!")
        return False
        
    print(f"Deploying {src_path} to {dest_path}...")
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace relative link paths
    content = content.replace("../", "/ads/")
    
    # Write to destination
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully deployed {dest_filename}")
    return True

if __name__ == "__main__":
    deploy_page("air-ambulance-portblair.html", "air-ambulance-portblair.html")
    deploy_page("air-ambulance-jammu-kashmir.html", "air-ambulance-jammu-kashmir.html")
    # Also deploy delhi if it exists
    # deploy_page("air-ambulance-delhi.html", "air-ambulance-delhi.html")
