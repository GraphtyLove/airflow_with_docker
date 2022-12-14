from common import download_file
import os

def clean() -> str:
    print("Cleaning...")
    
    # Check pipeline ID
    pipeline_id  = os.getenv("CUSTOM_PIPELINE_ID")
    if not pipeline_id:
        raise ValueError("Pipeline ID not found")
    
    houses = download_file("houses.html", f"houses_{pipeline_id}.html")
    
    print(f"html downloaded with: {len(houses)} lines")
    print("Cleaning Done")