import solara

@solara.component
def Page():
    markdown = "Test"

    solara.Markdown(markdown)
