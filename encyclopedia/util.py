import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def search_entries(search):
    """
    Returns a list of names of encyclopedia, based on the search string. 
    In case it finds the encyclopedia with exactly the same 
    name being searched, returns only this one, 
    otherwise returns all names which contains the search string.
    In case both conditions above fail, it returns a empty list.
     . 
    """
    _, filenames = default_storage.listdir("entries")
    result = []
    for filename in filenames: 
        if filename.endswith(".md"):
            nameonly = re.sub(r"\.md$", "", filename)
            
            if nameonly == search:
                print("name only :", nameonly)
                print("search :", search)
                return (nameonly)
            elif search in nameonly:
                result.append(nameonly)
    return(result)

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    title.strip                         # Remove the spaces from both sides.
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    return

def new_entry(title, content):
    """
    Saves an new encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    the entry is not saved.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return False
    default_storage.save(filename, ContentFile(content))
    return True


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
