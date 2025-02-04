""" This app is a blog that allows the user to create, update, delete posts and like each post."""
from flask import Flask, request, render_template, redirect
import json

app = Flask(__name__)
JSON_FILE = 'data/blog_posts.json'


def load_json_file():
    """ Returns a list of dictionaries with posts information """
    try:
        with open(JSON_FILE, 'r') as json_file:
            blog_posts = json.load(json_file)
    except FileNotFoundError as e:
        print(e)
        error_function()
    else:
        return blog_posts


def write_json(blog_posts):
    """ Update/save the data in the json file. """
    with open(JSON_FILE, "w") as my_file:
        dict_post = json.dumps(blog_posts, indent=4)
        my_file.write(dict_post + '\n')


def fetch_post_by_id(post_id):
    """ Returns the dictionary of the post containing the given id (post_id) """
    blog_posts = load_json_file()

    for post in blog_posts:
        if post['id'] == post_id:
            return post
    print("ID doesn't exist")


def free_id_key(list_of_dictionaries):
    """ Puts all post id values in a list.
        Checks the greater id number.
        Returns the lower missing number in the list or the greater number + 1, as free id number.
    """
    list_id= []
    for post_dict in list_of_dictionaries:
        list_id.append(post_dict['id'])
    for free_id in range(1, max(list_id)+2): # +2 to generate a new id if no one is free
        if free_id not in list_id:
            return free_id


@app.route('/')
def index():
    """ Passes the data to the template and renders it. """
    try:
        blog_posts = load_json_file()
    except Exception as e:
        print(e)
        return render_template('error.html')
    else:
        # add code here to fetch the job posts from a file
        return render_template('index.html', posts=blog_posts)


def error_function():
    """ Shows the error.html template in @app.route('/')"""
    @app.route('/')
    def error_template():
        """ Renders general error.html"""
        return render_template('error.html')


@app.errorhandler(404)
def page_not_found(error):
    """ Render '404.html' """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """ Renders '500.html'"""
    return render_template('500.html'), 500


@app.route('/add', methods=['GET', 'POST'])
def add():
    """ If a post request happened, gets the values from the from in the template 'add.html'.
        Updates the data in the json file and redirects to the app.route(/),
        which re-renders the template index.html.
    """
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        blog_posts = load_json_file()
        id_new_post = free_id_key(blog_posts)
        new_dict = {'id': id_new_post, 'author': author, 'title': title, 'content': content, 'likes': 0}
        blog_posts += [new_dict]
        write_json(blog_posts)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """ Removes the post with the given id (post_id) from the json file
        and redirects to app.route(/) """
    blog_posts = load_json_file()
    post = fetch_post_by_id(post_id)
    blog_posts.remove(post)
    write_json(blog_posts)
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """ If a post request happened, fetches the post with the given id (post_id)
        gets the date from the form in 'update.html'
        Updates the data in the fetched post dictionary.
        Updates/saves the data in the json file.
        Redirects to the app.route(/).
     """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        # Update the post in the JSON file
        like = post['likes']
        updated_dict = {'id': post_id, 'author': author, 'title': title, 'content': content, 'likes': like}
        blog_posts = load_json_file()
        post_index_in_list = blog_posts.index(post)
        blog_posts[post_index_in_list] = updated_dict
        write_json(blog_posts)
        # Redirect back to index
        return redirect('/')
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/likes/<int:post_id>')
def likes(post_id):
    """ Fetches the post with the given id (post_id)
        Gets the value with the key 'likes' in the post dictionary and adds a like (+1)
        Updates/saves the date in the json file
        Redirects to app.route(/)
    """
    blog_posts = load_json_file()
    post = fetch_post_by_id(post_id)
    post_index_in_list = blog_posts.index(post)
    post_likes = post['likes'] + 1
    post['likes'] = post_likes
    blog_posts = load_json_file()
    blog_posts[post_index_in_list] = post
    write_json(blog_posts)
    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)