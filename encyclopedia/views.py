from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import random

from . import util

class NewFormSubmit(forms.Form):

    new_search = forms.CharField(label= "", 
                                 widget=forms.TextInput(attrs={"placeholder":"Search Wikipedia", "id":"search_form"}))
    
    
class NewEntrySubmit(forms.Form):

    new_title= forms.CharField(label= "Entry Title", 
                                 widget=forms.TextInput(attrs={"placeholder":"", "id":"title_form"}))
    
    new_content= forms.CharField(label= "Entry Content", 
                                 widget=forms.Textarea(attrs={"placeholder":"", "id":"content_form"}))


class EditEntryForm(forms.Form):

    entry_content = forms.CharField(label= "Entry Content", 
                                 widget=forms.Textarea(attrs={"placeholder":"", "id":"content_form"}))
    

def index(request):

    """
    To show all current list of entries 
    """

    if request.method =="GET":
        entries = util.list_entries()

        return render(request, "encyclopedia/index.html", {
            "entries": entries, 
            "form" : NewFormSubmit()
        })


def wiki(request, title):

    """
    Converts md to html and returns the entry if it exists
    """

    if request.method == "GET":

        entry = util.get_entry(title)

        if entry:

            html_body, html_title= util.convert_md(title)

            return(render(request, "encyclopedia/entry.html", {
                "title":html_title, 
                "main_body":html_body, 
                "form" : NewFormSubmit(),
            }))
        
        # in cases user uses the url tab
        elif util.get_entry(title) is None:
            return render(request, "encyclopedia/error.html", {
                "form": NewFormSubmit()
            })


    # for the search bar
    else:
    
        return render(request, "wiki:search", {
            "query":title
        }) 
    

def search(request):

    """
    Searches for a entry file in the search bar
    """

    if request.method == "POST":

        form = NewFormSubmit(request.POST)

        if form.is_valid(): 
            query= form.cleaned_data["new_search"] 

            # check if the entered search within the list of entries

            exact_match = util.exact_match(query)

            # exact match

            if exact_match:
                return(redirect(reverse("wiki:wiki", kwargs={
                    "title":exact_match
                })))
            
            # for partial search 

            partial_matches = util.partial_match(query)

            if partial_matches is not None and len(partial_matches) > 0:
                    return render(request, "encyclopedia/search.html", {
                        "form":NewFormSubmit(),
                        "matches": partial_matches, 
                        "query": query})


            else:

                return render(request, "encyclopedia/search.html", {
                    "form":NewFormSubmit(),
                    "query":query.capitalize()
                })
            

def random_page(request):

    """
    Randomly selects an entry title and directs the user to 
    the selected entry page
    """
    
    if request.method =="GET":

        entry_list = util.list_entries()

        selected_title = random.choice(entry_list)

        return redirect(reverse("wiki:wiki", kwargs={
            "title":selected_title
        }))
    

def new_page(request):

    """
    Accepts a new entrty from the user
    """

    #if the user wants to just get the page

    if request.method =="GET":

        entry_form = NewEntrySubmit()

        return render(request, "encyclopedia/new_page.html", {
            "form" : NewFormSubmit(), 
            "entry_form_title":entry_form['new_title'],
            "entry_form_content":entry_form['new_content']

        })
    
    # submitting a new entry
    if request.method == "POST":

        new_entry = NewEntrySubmit(request.POST)

        if new_entry.is_valid(): 

            entry_title= new_entry.cleaned_data["new_title"].capitalize() 
            entry_content= new_entry.cleaned_data["new_content"]

            # if the entry exisits 
            if util.exact_match(entry_title):
                return render(request, "encyclopedia/result.html", {
                    "results": "Error, An exact match has been found!",
                    "form" : NewFormSubmit()})
            
            # if the entry does not exisits
            elif util.exact_match(entry_title) is None:

                util.save_entry(entry_title, entry_content)

                return redirect(reverse("wiki:wiki", kwargs={
                    "title":entry_title
                    }))
            

def edit(request, title): 

    """
    To edit an existing entry content
    """

    content = util.separate_content(title)

    if request.method == "GET":

        entry_form= EditEntryForm(initial={
            "entry_content":content
        })

        return(render(request, "encyclopedia/edit.html", {
            "title":title,
            "body":entry_form,
            "form" : NewFormSubmit()

        }))
    
    elif request.method == "POST":
        
        new_submit=EditEntryForm(request.POST)

        if new_submit.is_valid():
            
            content=new_submit.cleaned_data["entry_content"]

            util.save_entry(title, content)

            return HttpResponseRedirect(reverse('wiki:wiki', kwargs={
                            "title":title
                            }))
