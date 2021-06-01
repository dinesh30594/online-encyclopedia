from random import randint

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    content = util.get_entry(entry.strip())
    if content is None:
        content = "## Page was not found"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': entry})


def search(request):
    int_value = request.GET.get('q').strip()
    if int_value in util.list_entries():
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': int_value}))
    else:
        substring = []
        for val in util.list_entries():
            if int_value in val:
                substring.append(val)
        return render(request, "encyclopedia/search.html", {
                "entries": substring,
                "value": int_value
            })


def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': random_title}))


def edit(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html",
                          {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", entry=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})


def create(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()
        if title == "" or content == "":
            return render(request, "encyclopedia/add.html",
                          {"message": "Can't save with empty field.", "title": title, "content": content})
        if title in util.list_entries():
            return render(request, "encyclopedia/add.html",
                          {"message": "Title already exist. Try another.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", entry=title)
    return render(request, "encyclopedia/add.html")
