import re
import random

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
            
            if nameonly.lower() == search.lower():
                #print("name only :", nameonly)
                #print("search :", search)
                return (nameonly)
            elif search.lower() in nameonly.lower():
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
    return True


def new_entry(title, content):
    """
    Saves an new encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    the entry is not saved.
    """

    title.strip                         # Remove the spaces from both sides.
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

def random_entry():
    """
    Retrive an random encyclopedia entry
    """    

    files = list_entries()
    return random.choice(files)


def html_from_markdown(content):
    """
    Convert a markdown content into html
    """    

    """
    Bold 
    """   
    # Convert to <strong></strong>
    regx = re.compile(r"^\*\*(.*?)\*\*", re.MULTILINE)
    content = regx.sub(r"<strong>\1</strong>",content)   

    """
    Link 
    """   
    # Convert to <a>
    regx = re.compile(r"\[(.*)\]\((.*)\)", re.MULTILINE)
    content = regx.sub(r"<a href=\2>\1</a>",content)   

    """
    Paragraph 
    """   
    new_content = ""
    for line in content.splitlines():
        line = re.sub(r'^(?!#|\*)(.+)', r'<p>\1</p>', line)
        new_content = new_content + line + "\n"
    content = new_content

    """
    Unordered lists
    """     
    new_content = ""    
    u_list = False
    for line in content.splitlines():

        if len(line) > 0:       # Check the line is not empty

            l = line[:2]
            if u_list and l!="* ":                      # check if there and unordered list to be closed.
                new_content = new_content + "</ul>"
                u_list =  False                         # Flag indicates the unordered list has finished

            #if line[0]!="#" and line[0]!="*":           # Add the paragraph to the line
            #    line = "<p>" + line + "</p>\n"

            if line[:2]=="* ":                          # Check if the lins is an unordered list
                if not u_list:                          # Check if it´s the first item of the list
                    line = "<ul><li>" + line [2:] + "</li>"
                    u_list = True                       # Flag indicates the unordered list has started.
                else:
                    line = "<li>" + line [2:] + "</li>"

        new_content = new_content + line + "\n"

    if u_list :     # in case still have an unordered list to be closed.
        new_content = new_content + "</ul>"

    content = new_content

    """
    Headers 
    """ 
    # Convert to h1
    regx = re.compile(r"^#\s(.*?)\n", re.MULTILINE)
    content = regx.sub(r"<h1>\1</h1>\n",content)                 

    # Convert to h2
    regx = re.compile(r"^##\s(.*?)\n", re.MULTILINE)
    content = regx.sub(r"<h2>\1</h2>\n",content)                 

    # Convert to h3
    regx = re.compile(r"^###\s(.*?)\n", re.MULTILINE)
    content = regx.sub(r"<h3>\1</h3>\n",content)                 

    # Convert to h4
    regx = re.compile(r"^####\s(.*?)\n", re.MULTILINE)
    content = regx.sub(r"<h4>\1</h4>\n",content)                 

    # Convert to h5
    regx = re.compile(r"^#####\s(.*?)\n", re.MULTILINE)
    content = regx.sub(r"<h5>\1</h5>\n",content)                 

    # Convert to h6
    regx = re.compile(r"^######\s(.*?)\n", re.MULTILINE) 
    content = regx.sub(r"<h6>\1</h6>\n",content)                            


    return content
