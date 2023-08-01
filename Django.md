# Registering the Application in the settings.py File

With Django, you can create as many applications as you want within a project, but each project must be registered so that the project knows about it. In Django all the applications are registered in a file called ``settings.py``

This file is responsible for all the configurations of the project, be careful when editing it because one messed-up line of code could break your whole project. Open it and scroll down to the INSTALLED_APPS list, add the assistant application like this:


```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # registering the new app
    'assistant',
]
```

# Creating the Views for the Application in the views.py File

In Django the ``views.py`` file plays an important role, it handles all the business logic of the application like capturing and validating form data, authenticating users, sending requests to an API, etc.

Our application will have two views, the home() and error_handler(), open the ``views.py`` file and make it look like this:

```python
from django.shortcuts import render
# import HttpResponse from django.urls
from django.http import HttpResponse


# this is the home view for handling home page logic
def home(request):
    return HttpResponse('The Home Page')


# this is the view for handling errors
def error_handler(request):
    return HttpResponse('404 Page')
```

# Configuring the URLs for the Application

Now that we have our views ready, let us register the URLs. Create a file named urls.py inside the assistant folder

The main purpose of the urls.py file is to register the views in the ``views.py`` file, open it and paste this code:

```python
from django.contrib import admin
from django.urls import path, include

# a list of all the projects urls
urlpatterns = [
    # the url to the admin site
    path('admin/', admin.site.urls),
    # registering all the assistant application urls
    path('', include('assistant.urls')),
]
```

# Creating and Rendering Templates

Our application will have three templates, <code>home.html</code>, <code>404.html</code>, and <code>base.html</code>.<br>

Let us start with the <code>base.html</code> template, open it, and paste the following code:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Assistant | {% block title %}  {% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```
<br>

Open the <code>home.html</code> template and paste this code:

```html
{% extends 'assistant/base.html' %}
{% block title %} Home {% endblock %}
{% block content %}
<div class="row justify-content-center my-4">
    <div class="col-md-7 mt-4">
        <div class="card">
            <h1 class="card-header text-center">A.I WEB ASSISTANT</h1>
            <div class="card-body">
              <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-primary mb-3" onclick="location.href='{% url 'new_chat' %}'">New Chat +</button>
              </div>
              <div class="chat-history mb-3">
                {% for message in messages %}
                  <div class="card mb-2 {% if message.role == 'assistant' %}bg-success text-white{% endif %}">
                    <div class="card-body p-2">
                      <strong>{{ message.role|title }}:</strong> {{ message.content|linebreaksbr }}
                    </div>
                  </div>
                {% endfor %}
              </div>
              <form action="." method="POST">
                <!-- this secures the form from malicious attacks during submission -->
                {% csrf_token %}
                <input class="form-control mb-2" required type="text" autofocus="autofocus" name="prompt" value="{{ prompt }}" id="">
                <label for="temperature" class="form-label">Temperature:</label>
                <input class="form-control mb-2" type="number" step="0.01" min="0" max="2" name="temperature" value="{{ temperature }}" id="temperature">
                <button class="btn btn-success fw-bold" type="submit">
                     GENERATE
                </button>
              </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

```
<br>

Open the ``404.html`` template and paste this code:

```html
{% extends 'assistant/base.html' %}
{% block title %} 404 {% endblock %}
{% block content %}
<div class="row justify-content-center my-4">
    <div class="col-md-7 mt-4">
        <h1>Page Not Found</h1>
        <p>Make sure you are connected to the internet or your query is correct</p>
        <a href="{% url 'home' %}" class="btn btn-secondary">Go Home</a>
    </div>
</div>
{% endblock %}
```
<br>

# Getting the OpenAI API Key

When have API Keys, we create a new file called `secret_key.py`.

```python
API_KEY = 'put your API key here'
```
<br><br>
# Implementing the Send Prompt Functionality

We have designed the interface for the web assistant and that we have successfully generated our API key, let us now integrate this API with our Django application. Open the ``views.py`` file and make it look like this:

```python
# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY

# this is the home view for handling home page logic
def home(request):
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')

# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')
```

