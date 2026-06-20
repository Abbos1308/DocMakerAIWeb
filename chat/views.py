from django.shortcuts import render,get_object_or_404 , redirect
from django.http import HttpResponse
from docmakerai.generator import generate
import markdown
import time
from config.settings import git_token, groq_api_key
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Repo
from groq import chat
import time

# Create your views here.

# views.py
def home(request):
    if request.method == "POST":
        url = request.POST.get("url")
        try:
            obj = Repo.objects.get(url=url)
        except Repo.DoesNotExist:
            doc = generate(url, git_token, groq_api_key)
            doc = markdown.markdown(doc, extensions=["fenced_code", "codehilite"],
                extension_configs={"codehilite": {"css_class": "codehilite"}})
            if doc[3:].startswith("ERROR"):
                return render(request, "error.html")
            obj = Repo(url=url, doc=doc)
            obj.save()
        return redirect('repo_view', repo=obj.shortcut)
    return render(request, "home.html")

def repo_view(request, repo):
    obj = get_object_or_404(Repo, shortcut=repo)  # ✅
    repo_name = obj.shortcut.split("_")[-1]
    return render(request, "doc_preview.html", {"doc": obj.doc, "obj_id": obj.id, "repo": repo_name})
def chat_view(request):
    messages = []
    obj_id = request.POST.get("obj_id")
    key = f'history_{obj_id}' 
    if key not in request.session:
        request.session[key] = []
    if request.method == 'POST':
        for msg in request.session[key]:
            user_msg = msg["user_msg"]
            ai_resp = msg["ai_resp"]
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": ai_resp})
        obj = Repo.objects.get(id=obj_id)
        doc = obj.doc
        shortcut = obj.shortcut
        user_msg = request.POST.get("user_msg")
        ai_resp = chat(messages,user_msg,doc)
        ai_resp =  markdown.markdown(
            ai_resp,
            extensions=["fenced_code", "codehilite"],
            extension_configs={
                "codehilite": {
                    "css_class": "codehilite"
                }
            }
        )
        print(ai_resp)
        request.session[key].append({
            "user_msg":user_msg,
            "ai_resp":ai_resp,
            "timestamp":int(time.time())
        })
        request.session.modified = True
        return render(request,"chat.html",{
            "history" : request.session[key],
            "obj_id":  obj_id,
            "shortcut" : shortcut,
        })
    return render(request,"chat.html")