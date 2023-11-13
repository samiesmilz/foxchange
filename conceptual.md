### Conceptual Exercise

Answer the following questions below:

- What are important differences between Python and JavaScript?

  - Python is primarily used to develop the back end of applications,  
    While JavaScript is primarily used for front-end development.
  - Python uses whitespace indetation for code blocks
    While Javascript uses curly bracktes for code blocks
  - Python is strongly typed, meaning the type of the variable is enforced and stricly adhered to during execution.
    While JavaScript is weakly typed therefore has more flexibity in how varibales are treated with respect to types.

- Given a dictionary like `{"a": 1, "b": 2}`: , list two ways you
  can try to get a missing key (like "c") _without_ your programming
  crashing.

  - l would use a .get() method, with "what to retrieve" and defualt value as parameters.
  - Or run the code in a try: and except KeyError: block.

- What is a unit test?  
  It is where small componets of a program like functions are tested in isolataion to ensure their correctness.

- What is an integration test?  
  This is where multiple componests of the software are tested together to see if their interaction works as expected.

- What is the role of web application framework, like Flask?

* Web frameworks combine and provide reusable components, utilities and design patterns
  that help developers develop faster following good structure and practives.
* A framework like flask abstracts away alot of the complexities in web development
  allowing developers to write applications logic using high level constructs

- You can pass information to Flask either as a parameter in a route URL
  (like '/foods/pretzel') or using a URL query param (like
  'foods?type=pretzel'). How might you choose which one is a better fit
  for an application?

  - I would choose a URL query for essential / required information that identifies the resource
  - And l would choose a query parameter for option / additional information that doesn't directly identify the resource.

- How do you collect data from a URL placeholder parameter using Flask?
  By defining a route in flask with a variable path `@app.route('/profile/<username>')`
  And then defining a function that takes that parameter `def profile(username):`

- How do you collect data from the query string using Flask?
  By using `request.args.get('parameter_name')`

- How do you collect data from the body of the request using Flask?
  Accesing form data from the body using `request.form.get("key")` for POST requests
  And accessing JSON data using `request.get_json()`

- What is a cookie and what kinds of things are they commonly used for?
  A cookie is a small piece of information stored on the clients browser
  and sent back to the server in future request to help the server know something about the client request.

- What is the session object in Flask?
  A session object is a dictionary that is available to the application through the session attribute of the request object..
  used to store information on the server and as a cookie on the client that can persist across multiple user requests

- What does Flask's `jsonify()` do?
  It is a Flask function that is used to convert a Python dictionary or list into a JSON reponse with the appropreate conetnt type.
