import json
import re
from pathlib import Path
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render


def landing(request):
    return render(request, "teachers/landing.html")

# ---------------------------------------------------------------------------
# Resource library (reads metadata from teachers/data/resources.json,
# serves the actual files from Google Drive / Docs / Slides / Sheets)
# ---------------------------------------------------------------------------
 
def _drive_urls(raw):
    """
    Given a Drive/Docs/Slides/Sheets link OR a bare file ID,
    return (view_url, download_url).
 
    Handles:
      - Google Slides   (/presentation/d/ID)  -> view in Slides, download as .pptx
      - Google Docs     (/document/d/ID)      -> view in Docs,   download as .pdf
      - Google Sheets   (/spreadsheets/d/ID)  -> view in Sheets, download as .xlsx
      - Regular Drive files (/file/d/ID)      -> view in Drive,  direct download
      - A bare file ID                        -> treated as a Drive file
    """
    raw = (raw or "").strip()
    if not raw:
        return "#", "#"
 
    # Google Workspace files (Slides / Docs / Sheets) keep their native type
    m = re.search(r"(presentation|document|spreadsheets)/d/([A-Za-z0-9_-]+)", raw)
    if m:
        kind, fid = m.group(1), m.group(2)
        view = f"https://docs.google.com/{kind}/d/{fid}/preview"
        export = {"presentation": "pptx", "document": "pdf", "spreadsheets": "xlsx"}[kind]
        download = f"https://docs.google.com/{kind}/d/{fid}/export?format={export}"
        return view, download
 
    # Regular Drive file: a /file/d/ID link, or a bare ID
    m = re.search(r"/file/d/([A-Za-z0-9_-]+)", raw)
    fid = m.group(1) if m else raw
    view = f"https://drive.google.com/file/d/{fid}/view"
    download = f"https://drive.google.com/uc?export=download&id={fid}"
    return view, download
 
 
def resources(request):
    # Load the metadata JSON (small file, loaded per request — no database)
    data_path = Path(settings.BASE_DIR) / "teachers" / "data" / "resources.json"
    with open(data_path, encoding="utf-8") as f:
        items = json.load(f)
 
    # --- Filtering, from the checkbox form's ?level=&subject=&resource= params ---
    levels = request.GET.getlist("level")
    subjects = request.GET.getlist("subject")
    types = request.GET.getlist("resource")
 
    if levels:
        items = [r for r in items if r.get("level") in levels]
    if subjects:
        items = [r for r in items if r.get("subject") in subjects]
    if types:
        items = [r for r in items if r.get("resource_type") in types]
 
    # --- Build view/download URLs for each resource (and its optional answer key) ---
    for r in items:
        r["view_url"], r["download_url"] = _drive_urls(r.get("drive_id"))
        ak = r.get("answer_key_id") or r.get("answer_key_url")
        if ak:
            _, r["answer_key_url"] = _drive_urls(ak)
        else:
            r["answer_key_url"] = ""
 
    # --- Paginate ---
    paginator = Paginator(items, 6)
    page = paginator.get_page(request.GET.get("page"))
 
    return render(request, "teachers/resources.html", {
        "current_page": "teachers",
        "page_obj": page,
        "sel_levels": levels,
        "sel_subjects": subjects,
        "sel_types": types,
    })