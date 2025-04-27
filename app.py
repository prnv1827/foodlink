from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__, template_folder='.')

# In-memory store for food posts
food_posts = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post_food():
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        quantity = request.form.get('quantity')
        location = request.form.get('location')

        post = {
            'id': str(uuid.uuid4()),  # unique id for each post
            'food_name': food_name,
            'quantity': quantity,
            'location': location,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        food_posts.append(post)
        return redirect(url_for('find_food'))
    return render_template('post.html')

@app.route('/find')
def find_food():
    return render_template('find.html', food_posts=food_posts)

@app.route('/pickup/<post_id>', methods=['POST'])
def pickup_food(post_id):
    global food_posts
    food_posts = [post for post in food_posts if post['id'] != post_id]
    return redirect(url_for('find_food'))

if __name__ == '__main__':
    app.run(debug=True)
