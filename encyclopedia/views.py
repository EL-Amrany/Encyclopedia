from cProfile import label
from logging import PlaceHolder
from traceback import format_exc
import markdown2
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from . import util
from django import forms
from django.urls import reverse

class NewTaskForm(forms.Form):
    title=forms.CharField(label='Title')
    content=forms.CharField(
                            widget=forms.Textarea())

class form_edit(forms.Form):
    content=forms.CharField(label='',widget=forms.Textarea())
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    title=request.GET['q']
    if title.strip()=="":
            return redirect("encyclopedia:index")
    return redirect('encyclopedia:wiki', entry=title.upper())  
    
        

def wiki(request,entry):

    content=util.get_entry(entry)

    if content==None:
        return render(request,"encyclopedia/error.html")
    content=markdown2.markdown(content)
    
    return render(request,"encyclopedia/article.html",{
        "content":content,
        "title":entry
    })
                                

        
def add(request):
    
    if request.method=='POST':
        form=NewTaskForm(request.POST)
        if form.is_valid():
            title  = form.cleaned_data['title']
            content= form.cleaned_data['content']
            util.save_entry(title,content)
            return redirect('encyclopedia:index')
        return render(request,'encyclopedia/add.html',{'form':form})
        

    return render(request,"encyclopedia/add.html",{"form":NewTaskForm()})   

def edit(request,entry):
    if request.method=='POST':
        form=form_edit(request.POST)
        if form.is_valid():
            title=entry
            content=form.cleaned_data['content']
            util.save_entry(title,content)
            return redirect('encyclopedia:wiki',entry=entry)
        return render(request,'encyclopedia/edit.html',
                 {"form":form}  )

    return render(request,'encyclopedia/edit.html',
                 {"form":form_edit({"content":util.get_entry(entry)})}  )

def delete(request,entry):
    util.delete_entry(entry)
    return redirect("encyclopedia:index")
def random(request):
    entry,content=util.random_entry()
    #return redirect('encyclopedia:wiki', entry=entry.upper()) 
    return render(request,"encyclopedia/article.html",{
        "content":content,
        "title":entry
    })


#