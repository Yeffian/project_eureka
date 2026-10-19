import json
import re
from pathlib import Path

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render

def _drive_urls(raw):
    """
    Given a Drive/Docs/Slides/Sheets link OR a bare file ID, return
    (view_url, download_url, thumb_url).
 
    Handles:
      - Google Slides   (/presentation/d/ID)  -> preview, download .pptx, first-slide thumb
      - Google Docs     (/document/d/ID)      -> preview, download .pdf,  first-page thumb
      - Google Sheets   (/spreadsheets/d/ID)  -> preview, download .xlsx, first-page thumb
      - Regular Drive files (/file/d/ID)      -> view, direct download, thumb
      - A bare file ID                        -> treated as a Drive file
    """
    raw = (raw or "").strip()
    if not raw:
        return "#", "#", ""
 
    m = re.search(r"(presentation|document|spreadsheets)/d/([A-Za-z0-9_-]+)", raw)
    if m:
        kind, fid = m.group(1), m.group(2)
        view = f"https://docs.google.com/{kind}/d/{fid}/preview"
        export = {"presentation": "pptx", "document": "pdf", "spreadsheets": "xlsx"}[kind]
        download = f"https://docs.google.com/{kind}/d/{fid}/export?format={export}"
        thumb = f"https://drive.google.com/thumbnail?id={fid}&sz=w800"
        return view, download, thumb
 
    m = re.search(r"/file/d/([A-Za-z0-9_-]+)", raw)
    fid = m.group(1) if m else raw
    view = f"https://drive.google.com/file/d/{fid}/view"
    download = f"https://drive.google.com/uc?export=download&id={fid}"
    thumb = f"https://drive.google.com/thumbnail?id={fid}&sz=w800"
    return view, download, thumb
 
 
def resources(request):
    data_path = Path(settings.BASE_DIR) / "teachers" / "data" / "resources.json"
    with open(data_path, encoding="utf-8") as f:
        items = json.load(f)
 
    subjects = request.GET.getlist("subject")
    types = request.GET.getlist("resource")
 
    if subjects:
        items = [r for r in items if r.get("subject") in subjects]
    if types:
        items = [r for r in items if r.get("resource_type") in types]
 
    for r in items:
        r["view_url"], r["download_url"], r["thumb_url"] = _drive_urls(r.get("drive_id"))
        ak = r.get("answer_key_id") or r.get("answer_key_url")
        if ak:
            _, r["answer_key_url"], _ = _drive_urls(ak)
        else:
            r["answer_key_url"] = ""
 
    paginator = Paginator(items, 6)
    page = paginator.get_page(request.GET.get("page"))
 
    return render(request, "teachers/resources.html", {
        "current_page": "teachers",
        "page_obj": page,
        "sel_subjects": subjects,
        "sel_types": types,
    })

def landing(request):
    return render(request, "teachers/landing.html", {"current_page": "teachers"})