import os
import shutil
import sys

from markdowntohtml import markdown_to_html_node
from extracttitle import extract_title


def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_static(src_path, dst_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(content_dir, template_path, dest_dir, basepath):
    for item in os.listdir(content_dir):
        src_path = os.path.join(content_dir, item)
        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dest_path = os.path.join(dest_dir, item.replace(".md", ".html"))
                generate_page(src_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(src_path, template_path, os.path.join(dest_dir, item), basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
