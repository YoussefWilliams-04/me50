from logging import PlaceHolder
from django.shortcuts import render
from django import forms 
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import re
import random
import markdown2


class SearchForm(forms.Form):
    query=forms.CharField(label="Search")
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":SearchForm()
    })

def search(request):
    query=request.POST["query"]

    if util.get_entry( query ):
        # perfect match
         return entry(request,query)

    else:
        #match substring
        matches=[]
        pattern= re.compile(query) #query
        for i in util.list_entries():
            if pattern.search(i):
                matches.append(i)

        return render(request, "encyclopedia/searchResults.html", {
        "matches": matches,
        "form":SearchForm()
    })



def entry(request,entry):
    
    
    message=""
    if util.get_entry(entry)==None: 
        message="No entry found"
        return render(request,"encyclopedia/entry.html",{  
            "message": message
       
        })
    return render(request,"encyclopedia/entry.html",{  
        "entry":markdown2.markdown(util.get_entry(entry))
        ,"title": entry
        
        })


def random_entry(request):
    
    random_entry=random.choice(util.list_entries())
    return entry(request,random_entry)


def add(request):
    message=""
    if request.method=="POST":
        if util.get_entry(request.POST["title"]):
            message="ERROR: Entry already exists"
            return render(request,"encyclopedia/addEntry.html",{
                "message": message})
        else:
            util.save_entry(request.POST["title"], request.POST["content"])
            return entry(request,request.POST["title"])
            

    return render(request,"encyclopedia/addEntry.html")

def edit(request,entry):
    message=""
    if request.method=="POST":
        util.save_entry(entry, request.POST["content"])
        message=" Entry succesfully edited"
        
        return render(request,"encyclopedia/entry.html",{  
        "entry":markdown2.markdown(util.get_entry(entry))
        ,"title": entry
        
        })
        
    return render(request,"encyclopedia/edit.html",{
        "entry":entry,
        "content": markdown2.markdown(util.get_entry(entry))
        ,"message":message
        })