import solara

@solara.component
def Page():
  with solara.Column(align="center"):
    markdown = """
    ## Justin's Mapping Corner

    Welcome to Justin's Mapping Corner! Here you can view the interactive web maps that I have created as personal projects. You may also
    view the source code in this [GitHub repository](https://github.com/jntp/HTC-for-Parkour). If you have any questions or feedback, please
    see the left sidebar for contact information. 🙂
    """

    solara.Markdown(markdown)

# Where's the toolbar? Figure that out
