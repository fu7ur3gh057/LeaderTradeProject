from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import mark_safe, format_html

def image_div(image_url, file_name):
    return f"""
        <div style="flex-direction: row; display: flex;">
            <a href="{image_url}" style="display: inline" target="_blank">
            <img src="{image_url}" alt="%s" width="70" height="70"
                style="object-fit: cover; border: 3px dashed #eee; margin: 0 10px;"/></a>
    """


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(image_div(image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        output.append("</div>")
        return mark_safe("".join(output))
