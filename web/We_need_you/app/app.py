#!/usr/bin/env python3

from flask import Flask, request, render_template, make_response, url_for
import pdfkit
import os


app = Flask(__name__)

templates = {
    "home": "home.html",
    "form": "form.html",
    "resume": "resume.html",
    "error": "error.html"
}

@app.route('/')
def home():
    return render_template(templates["home"])

# Parse experiences args
def extract_experiences(parsed_data):
    experiences = []
    index = 1
    while f'job{index}_title' in parsed_data:
        experience = {
            "title": parsed_data.get(f'job{index}_title', ''),
            "company": parsed_data.get(f'job{index}_company', ''),
            "start_date": parsed_data.get(f'job{index}_start', ''),
            "end_date": parsed_data.get(f'job{index}_end', ''),
            "description": parsed_data.get(f'job{index}_description', '')
        }
        experiences.append(experience)
        index += 1
    return experiences

# Parse formations args
def extract_formations(parsed_data):
    formations = []
    index = 1
    while f'edu{index}_title' in parsed_data:
        formation = {
            "title": parsed_data.get(f'edu{index}_title', ''),
            "school": parsed_data.get(f'edu{index}_school', ''),
            "start_date": parsed_data.get(f'edu{index}_start', ''),
            "end_date": parsed_data.get(f'edu{index}_end', '')
        }
        formations.append(formation)
        index += 1
    return formations


@app.route('/resume', methods=["GET", "POST"])
def resume():
    # Return form
    if request.method == "GET":
        return render_template(templates["form"])

    # POST request
    try:
        # Else, export resume to HTML or PDF
        parsed_data = request.form

        # Create a structured Python dict from form args
        resume_data = {
            "name": parsed_data.get('name', ''),
            "email": parsed_data.get('email', ''),
            "phone": parsed_data.get('phone', ''),
            "address": parsed_data.get('address', ''),
            "experiences": extract_experiences(parsed_data),
            "formations": extract_formations(parsed_data),
            "skills": parsed_data.get('skills', ''),
            "languages": parsed_data.get('languages', '')
        }
        
        # Render HTML
        resume_html = render_template(templates["resume"], **resume_data)
        # Preview resume
        if parsed_data.get("action") == "preview":
            return resume_html
        # Export resume (HTML to PDF using wkhtmltopdf)
        elif parsed_data.get("action") == "export":
            pdf = pdfkit.from_string(resume_html, options = {
                "enable-local-file-access": ""
            })
            resp = make_response(pdf)
            resp.headers.add_header("Access-Control-Allow-Origin", "*")
            resp.headers.add_header("Content-Type", "application/pdf")
            resp.headers.add_header("Content-Disposition", f"inline;filename=CV.pdf")
            return resp
    # Error
    except Error:
        return render_template(templates["error"])



if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8000, debug=True)
    app.run(host="0.0.0.0", port=8000)
