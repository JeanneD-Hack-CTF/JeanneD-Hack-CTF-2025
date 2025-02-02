import os
import re
import uuid
import markdown2
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

# Notes folder
NOTES_DIR = os.path.join(os.getcwd(), 'notes')
PUBLIC_NOTES = os.path.join(NOTES_DIR, 'public')
UUID_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


@app.before_request
def assign_cookie():
    if 'user_id' not in request.cookies:
        # Generate random ID
        user_id = str(uuid.uuid4())
        resp = make_response(redirect(request.path))
        resp.set_cookie('user_id', user_id)
        return resp


def get_user_id():
    user_id = request.cookies.get('user_id')
    return user_id if re.match(UUID_PATTERN, user_id) else None



@app.route('/')
def index():
    categories = [d for d in os.listdir(PUBLIC_NOTES) if os.path.isdir(os.path.join(PUBLIC_NOTES, d))]
    if (user_id := get_user_id()) and os.path.exists(os.path.join(NOTES_DIR, user_id)):
        categories.extend([d for d in os.listdir(os.path.join(NOTES_DIR, user_id))])
        categories = list(set(categories))
    return render_template('index.html', categories=categories)


@app.route('/category/<category_name>')
def view_category(category_name):
    notes = list()
    category_path = os.path.join(PUBLIC_NOTES, category_name)
    # Add notes from public category
    if os.path.exists(category_path) and os.path.isdir(category_path):
        notes.extend([f for f in os.listdir(category_path) if f.endswith('.md')])
    # Add notes from user category
    if (user_id := get_user_id()):
        category_path = os.path.join(NOTES_DIR, user_id, category_name)
        if os.path.exists(category_path) and os.path.isdir(category_path):
            notes.extend([f for f in os.listdir(category_path) if f.endswith('.md')])

    if notes:    
        return render_template('category.html', notes=notes, category=category_name)
    else:
        flash('Catégorie introuvable')
        return redirect(url_for('index'))


@app.route('/category/<category_name>/note/<filename>')
def view_note(category_name, filename):
    content = None
    note_path = os.path.join(PUBLIC_NOTES, category_name, filename)
    # Public note
    if os.path.exists(note_path):
        with open(note_path, 'r') as file:
            content = file.read()
    # Personal note
    elif (user_id := get_user_id()):
        personal_note = os.path.join(NOTES_DIR, user_id, category_name, filename)
        if os.path.exists(personal_note):
            with open(personal_note, 'r') as file:
                content = file.read()

    if content:
        html_content = markdown2.markdown(content, extras=["fenced-code-blocks"])
        return render_template('view_note.html', content=html_content, title=filename, category=category_name)
    else:
        flash('Note introuvable')
        return redirect(url_for('view_category', category_name=category_name))


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    categories = [d for d in os.listdir(PUBLIC_NOTES) if os.path.isdir(os.path.join(PUBLIC_NOTES, d))]

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        custom_category = request.form.get('custom_category', '').strip()
        
        # Set category path
        if (user_id := get_user_id()):
            if category == 'Autre...' and custom_category:
                category = custom_category
            category_path = os.path.join(NOTES_DIR, user_id, category)
        else:
            flash('Jeton utilisateur invalide !')
            return redirect(url_for('add_note'))
        
        if not os.path.exists(category_path):
            os.makedirs(category_path)
        
        # Create markdown file and write it
        note_path = os.path.join(category_path, f'{title}.md')
        with open(note_path, 'w') as file:
            file.write(content)
        
        flash('Note ajoutée avec succès !')
        return redirect(url_for('view_category', category_name=category))

    categories = [d for d in os.listdir(PUBLIC_NOTES) if os.path.isdir(os.path.join(PUBLIC_NOTES, d))]
    categories.append("Autre...")
    if (user_id := get_user_id()) and os.path.exists(user_dir := os.path.join(NOTES_DIR, user_id)):
        categories.extend([d for d in os.listdir(user_dir) if os.path.isdir(os.path.join(user_dir, d))])
    
    return render_template('add_note.html', categories=categories)


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']

    # Use find to search for files containing query pattern
    command = f"find {PUBLIC_NOTES} -type f -name '*.md' -exec grep -iHl '{query}' {{}} +"
    # Add research in personal dir if it exists
    if (user_id := get_user_id()):
        user_dir = os.path.join(NOTES_DIR, user_id)
        if os.path.exists(user_dir):
            command = f"find {PUBLIC_NOTES} {user_dir} -type f -name '*.md' -exec grep -iHl '{query}' {{}} +"
    
    results = subprocess.getoutput(command).split('\n')
    # Remove empty lines
    results = [result for result in results if result]

    search_results = []
    for result in results:
        preview = "Pas de résultats dans le fichier"
        try:
            with open(result, 'r') as file:
                content = file.read()

            # Search first occurence of pattern in file
            match = re.search(query, content, re.IGNORECASE)
            if match:
                # Keep 100 characters before and after
                start = max(match.start() - 100, 0)
                end = min(match.end() + 100, len(content))
                extract = content[start:end]

                # Highlight items found
                preview = re.sub(f"({query})", r"<mark>\1</mark>", extract, flags=re.IGNORECASE)
        except:
            preview = "Impossible de prévisualiser le fichier"

        search_results.append({
            'filepath': result.replace(NOTES_DIR, ''),
            'preview': preview
        })

    return render_template('search_results.html', query=query, results=search_results)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8000)
