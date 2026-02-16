project = "NMT High Performance Computing\nNew Mexico Tech"

master_doc = 'index'

extensions = ['myst_parser', 'sphinx_copybutton', 'sphinx_design', 'sphinx.ext.extlinks']

myst_enable_extensions = ["colon_fence", "attrs_inline", "attrs_block", "tasklist", "substitution"]
myst_enable_checkboxes = True

myst_substitutions = {
   # NMT HPC system specifications
   'nmthpc_total_cpu_nodes': '16',
   'nmthpc_total_gpu_nodes': '2',
   'nmthpc_gpu_type': 'NVIDIA H100',
   'nmthpc_filesystem_1': 'zfs',
   'nmthpc_filesystem_2': 'beegfs',
}

source_suffix = {
    '.txt': 'markdown',
    '.md': 'markdown',
}

html_theme = 'sphinx_book_theme'

myst_heading_anchors=6

html_static_path = ['_static']
html_css_files = ["custom.css"]

html_theme_options = {
   "logo": {
      "image_light": "_static/NMT_LOGO.png",
      "image_dark": "_static/NMT_LOGO.png",
   },
   "repository_url": "https://github.com/nmtech/nmthpc_docs",
   "use_repository_button": True,
}

html_context = {
   "default_mode": "light"
}

copybutton_prompt_text = r'^\$ '
copybutton_prompt_is_regexp = True
