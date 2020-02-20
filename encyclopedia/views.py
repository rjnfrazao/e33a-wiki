from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util


class NewEntryForm(forms.Form):
    name = forms.CharField(label="name")
    content = forms.CharField(label="content")
    oper = forms.CharField(label="oper")

#
# List all items, but in case param random is 'Y', return a random encyclopedia entry page.
#
def index(request):
    
    # In case random param is set to 'Y', return a random entry item page.
    if request.GET.get('random','') == "Y":     
        entry = util.random_entry()
        return redirect("encyclopedia_detail", encyclopedia_name=entry)

    # Return a list of entries.
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#
# Displays the detailed page from the encyclopedia item (name) 
#
def detail(request, encyclopedia_name):
    return render(request, "encyclopedia/detail.html", {
        "detail": util.get_entry(encyclopedia_name),
        "encyclopedia_name": encyclopedia_name
    })


#
# Displays the result of the search
# Case 1: Displays direct the detailed information from the item found.
# Case 2: Displays the list of similar items, in case an exactly match doesn't happen.
# (PENDING) Case 3: Nothing is found
#
def search(request):

    result_search = util.search_entries(request.GET['q'])

    # The exactly match was found.
    if isinstance(result_search,str):            
         return redirect("encyclopedia_detail", encyclopedia_name=result_search)

    # More than one entry was found.                
    else:                                   
        return render(request, "encyclopedia/index.html", {
            "entries": result_search
        })

    # (PENDING) nOTHING WAS FOUND


#
# View to add a new entry.
# Displays the item details page, when the new encyclopedia is saved.
# Displays an error message, when the new one already exists.
#
def add(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():
            # Post -> Add entry operation
            if util.new_entry(form.cleaned_data["name"], 
                form.cleaned_data["content"]):
                # Entry saved. Redirect to the entry page.
                return HttpResponseRedirect(reverse("encyclopedia_detail", 
                    args=[form.cleaned_data["name"]]))
            else:
                # Entry already exits. Display an error message
                return render(request, "encyclopedia/add.html", {
                    "form": form,
                    "message": "Entry name already exists.",
                    "oper": "add",
                    "oper_title": "Add New Entry"})
              
        else: 
            # Form wasn't valid.
            return render(request, "encyclopedia/add.html", {
                "form": form,
                "message": "Form wasn't a valid one.",
                "oper": "add",
                "oper_title": "Add New Entry"
                })
    else:
            # Get -> Open blank page to add an entry.
            return render(request, "encyclopedia/add.html", {
                "form": NewEntryForm(),
                "oper": "add",
                "oper_title": "Add New Entry"
                })


#
# View to update an encyclopedia entry.
# 
# 

def update(request, encyclopedia_name):

    if request.method == "POST":
        print("post ok")
        form = NewEntryForm(request.POST)
        if form.is_valid():
            print("Form Is Valid ok")
            if util.save_entry(form.cleaned_data["name"], 
                form.cleaned_data["content"]):
                print("Saved Entry")
                # Entry updated. Redirect to the entry page.
                return HttpResponseRedirect(reverse("encyclopedia_detail", 
                    args=[form.cleaned_data["name"]]))
            
                # else: Entry does't exit. Error when updating
                 
        else: 
            # Form wasn't valid.
            return render(request, "encyclopedia/add.html", {
                "form": form,
                "message": "Form wasn't a valid one.",
                "oper": "edit",
                "oper_title": "Edit Entry"
                })
    else:
        print("Get -> Edit operation")  
        #form = NewEntryForm(request.GET)
        #form.name = encyclopedia_name
        content = util.get_entry(encyclopedia_name)
        print(">>>", encyclopedia_name)   
        print(">>>", content)
       
        return render(request, "encyclopedia/add.html", {
            "name": encyclopedia_name,
            "content": content,
            "oper":"edit",
            "oper_title": "Edit Entry"
            })

