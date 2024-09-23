import re
import markdown

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """

    # to remove the trailing white space
    content = content.strip()

    filename = f"entries/{title}.md"
    formatted_content = f"# {title}\n\n{content}"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(formatted_content))


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
    

def convert_md(title):
    """
    Converts the title and it's content from MD
    to HTML file for rendering 
    """

    file = default_storage.open(f"entries/{title}.md", "r")
    file= file.read()
    # spliting the file into lines
    lines= file.splitlines()

    if lines and lines[0].startswith("#"):
        html_title= lines[0].lstrip("# ").strip()
        lines=lines[1:]

    else:
        html_title= lines[0].strip()
        lines=lines[1:]


    html_body = "\n".join(lines)

    html_body= markdown.markdown(html_body)

    return html_body, html_title


def exact_match(query):
    """Takes a query, and checks for a exact match against
    the exisiting list of entries"""

    entry_list = list_entries()

        
    for entry in entry_list:
        if query.lower() == entry.lower():
            return entry



def partial_match(query):
    """
    Takes a query, and checks for a partial pattern match against the 
    list of entries, and return a list of entry 
    """

    entry_list = list_entries()

    matches=[]

    for entry in entry_list:
        if query.lower() in entry.lower():
            matches.append(entry)

    return(matches)
    

def separate_content(title):
    """
    Separates the content from the Title for rendering
    """
    
    file = default_storage.open(f"entries/{title}.md", "r")
    file= file.read()

    # spliting the file into lines
    lines= file.splitlines(True)

    if lines and lines[0].startswith("#"):
        lines=lines[1:]

    return ''.join(lines)


