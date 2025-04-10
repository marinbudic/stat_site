from textnode import TextNode, TextType, split_nodes_delimiter
from block_markdown import markdown_to_html_node
from extract import extract_title

import os
import shutil
import sys

def move_files(stat, pub):
    if os.path.exists(pub):
        shutil.rmtree(pub)
    
    os.mkdir(pub)

    to_copy = os.listdir(stat)

    for child in to_copy:
        path = os.path.join(stat, child)
        if os.path.isfile(path):
            print(f"Copying {path}, to {pub}")
            shutil.copy(path, pub)
        else:
            pub_path = os.path.join(pub, child)
            os.mkdir(pub_path)
            print(f"Copying {path} to {pub_path}")
            move_files(path, pub_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    template = ""

    with open(from_path, encoding="utf-8") as f:
        md = f.read()

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    html_node = markdown_to_html_node(md)
    html = html_node.to_html()
    heading = extract_title(md)

    template = template.replace("{{ Title }}", heading)
    new_html = template.replace("{{ Content }}", html)

    new_html = new_html.replace('href="/', f'href="{basepath}')
    new_html = new_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w",  encoding="utf-8") as f:
        f.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    children = os.listdir(dir_path_content)

    for child in children:
        path = os.path.join(dir_path_content, child)
        
        if os.path.isfile(path):
            filename_without_ext = os.path.splitext(child)[0]
            html_filename = filename_without_ext + ".html"
            dest_file_path = os.path.join(dest_dir_path, html_filename)
            generate_page(path, template_path, dest_file_path, basepath)
        else:
            pub_path = os.path.join(dest_dir_path, child)
            os.mkdir(pub_path)
            generate_pages_recursive(path, template_path, pub_path, basepath)

def main():
    static = "/home/marinbudic/bootprojs/stat_site/static/"
    docs = "/home/marinbudic/bootprojs/stat_site/docs/"

    move_files(static, docs)

    content = "/home/marinbudic/bootprojs/stat_site/content/"
    template = "/home/marinbudic/bootprojs/stat_site/template.html"
    destination = "/home/marinbudic/bootprojs/stat_site/docs/"
        
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_pages_recursive(content, template, destination, basepath)

main()
