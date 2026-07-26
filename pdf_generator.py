from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
import os

def generate_pdf(resume: dict, template: str = "classic", output_path: str = "output/resume.pdf"):
    env = Environment(loader=FileSystemLoader("templates"))
    tmpl = env.get_template(f"{template}.html")
    html_content = tmpl.render(resume=resume)
    
    with open(output_path, "wb") as f:
        pisa.CreatePDF(html_content, dest=f)
    
    print(f"PDF saved to {output_path}")