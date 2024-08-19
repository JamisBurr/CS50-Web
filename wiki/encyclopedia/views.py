from django.shortcuts import render, redirect
from django import forms
from . import util
import random
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Store the current title in the session
    request.session['current_title'] = title

    # Get the content of the entry
    entry_content = util.get_entry(title)
    
    # If the entry doesn't exist, return an error page
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": "The requested page was not found."
        })
    
    # Convert the Markdown content to HTML
    entry_content_html = markdown2.markdown(entry_content)
    
    # If the entry exists, render the entry page
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content_html,
    })

def search(request):
    query = request.GET.get('q')
    
    # Check if the query exactly matches an entry title
    if query:
        entry_content = util.get_entry(query)
        if entry_content:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": entry_content
            })
    
        # If no exact match, search for partial matches
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)
        
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })

    # If no query is provided, return to the index page
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="")

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if the entry with the same title already exists
            if util.get_entry(title):
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error_message": "An entry with this title already exists."
                })

            # Save the new entry
            util.save_entry(title, content)
            return redirect("entry", title=title)
    
    # If the request method is GET, display the form
    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")

def edit(request, title):
    # Get the current content of the entry
    current_content = util.get_entry(title)

    if current_content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": "The requested page was not found."
        })

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            # Save the updated entry
            util.save_entry(title, new_content)
            return redirect("entry", title=title)

    # If GET request, pre-populate the form with the current content
    form = EditPageForm(initial={'content': current_content})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    # Get the list of all entries
    entries = util.list_entries()
    
    # Get the current entry title from the session
    current_title = request.session.get('current_title')

    # If there are entries and the current page is not the homepage
    if entries:
        if current_title:
            # Filter out the current page from the list of entries
            entries = [entry for entry in entries if entry != current_title]
        
        # If after filtering, we still have entries left
        if entries:
            # Select a random entry from the filtered list
            random_entry = random.choice(entries)
            # Redirect to the randomly selected entry's page
            return redirect("entry", title=random_entry)
    
    # If no entries exist or only one entry exists that matches the current page, redirect to the index page
    return redirect("index")

