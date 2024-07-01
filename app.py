from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('recipes.db', check_same_thread=False)
c = conn.cursor()

# Create categories table
c.execute('''CREATE TABLE IF NOT EXISTS categories (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL
             )''')

# Create recipes table
c.execute('''CREATE TABLE IF NOT EXISTS recipes (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             category_id INTEGER NOT NULL,
             ingredients TEXT NOT NULL,
             procedure TEXT NOT NULL,
             FOREIGN KEY (category_id) REFERENCES categories(id)
             )''')

conn.commit()

@app.route('/')
def index():
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()
    return render_template('index.html', categories=categories)

@app.route('/view_recipes/<int:category_id>')
def view_recipes(category_id):
    c.execute("SELECT * FROM recipes WHERE category_id=?", (category_id,))
    recipes = c.fetchall()
    return render_template('view_recipes.html', recipes=recipes, category_id=category_id)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    title = request.form['title']
    category_id = request.form['category_id']
    ingredients = request.form['ingredients']
    procedure = request.form['procedure']

    c.execute("INSERT INTO recipes (title, category_id, ingredients, procedure) VALUES (?, ?, ?, ?)",
              (title, category_id, ingredients, procedure))
    conn.commit()

    return redirect(url_for('view_recipes', category_id=category_id))

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['category']
    c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    c.execute("DELETE FROM recipes WHERE category_id=?", (category_id,))
    c.execute("DELETE FROM categories WHERE id=?", (category_id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
