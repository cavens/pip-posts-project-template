import json

from flask import request, Response, url_for
from jsonschema import validate, ValidationError

import models
import decorators
from posts import app
from database import session


@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
  
    # Figure out if there's a title_like and/or body_like
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
    
    # Get the posts from the database
    posts = session.query(models.Post)
    if title_like:
      posts = posts.filter(models.Post.title.contains(title_like))
      print posts[0].body
      print posts[1].body

    if title_like and body_like:
      print posts[0].body
      print posts[1].body
      posts = posts.filter(models.Post.body.contains(body_like))
      print posts[0].body
    posts = posts.all()

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
  

@app.route("/api/posts/<int:id>", methods=["GET"])
def post_get(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(post.as_dictionary())
    return Response(data, 200, mimetype="application/json")  
  
  
@app.route("/api/posts/<int:id>", methods=["DELETE"])
@decorators.accept("application/json")
def post_delete(id):
    """ Single post endpoint """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Delete post
    session.delete(post)
    session.commit()
    message = "Delete of post successful"
    data = json.dumps({"message": message})
    return Response(data,200, mimetype="application/json")