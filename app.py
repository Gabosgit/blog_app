from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)

# Opening JSON file

def load_json_file():
    with open('data/blog_posts.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return blog_posts

def write_json(blog_posts):
    with open("data/blog_posts.json", "w") as my_file:
        dict = json.dumps(blog_posts, indent=4)
        my_file.write(dict + '\n')


def fetch_post_by_id(post_id):
    blog_posts = load_json_file()
    for post in blog_posts:
        if post['id'] == post_id:
            return post

def free_id_key(list_of_dictionaries):
    list_id= []
    for dict in list_of_dictionaries:
        list_id.append(dict['id'])
    for free_id in range(1, max(list_id)+2): # +2 to generate a new id if no one is free
        if free_id not in list_id:
            return free_id


@app.route('/')
def index():
    blog_posts = load_json_file()
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_json_file()
        id_new_post = free_id_key(blog_posts)
        new_dict = {'id': id_new_post, 'author': author, 'title': title, 'content': content}
        blog_posts += [new_dict]
        write_json(blog_posts)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_json_file()
    post = fetch_post_by_id(post_id)
    blog_posts.remove(post)
    write_json(blog_posts)
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    print(post)
    if post is None:
        # Post not found
        return "Post not found", 404
    # Update the post in the JSON file
    # Redirect back to index
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        updated_dict = {'id': post_id, 'author': author, 'title': title, 'content': content}
        blog_posts = load_json_file()
        post_index_in_list = blog_posts.index(post)
        blog_posts[post_index_in_list] = updated_dict
        write_json(blog_posts)
        return redirect('/')
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)