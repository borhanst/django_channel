from django.http import FileResponse
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML, default_url_fetcher, CSS
from django.core.exceptions import ImproperlyConfigured
from io import BytesIO


class PDFGenerateMixin:
    template_name = None
    attachment = True
    stylesheets = [settings.BASE_DIR / "static/main.css"]
    file_name = None

    css = CSS(
        string="""
              @page {
                  size: 30mm 44mm;
                  margin: 0;
                  
              }
              
              """
    )

    def get_html(self, *args, **kwargs):
        """
        Get the HTML template for generating the PDF.
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The HTML template.
        """
        if not self.template_name:
            return ImproperlyConfigured("template_name must be set")
        return self.template_name

    def get_document(self, context={}, *args, **kwargs):
        """
        Generate the PDF document.
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bytes: The generated PDF document.
        """
        template = get_template(self.get_html())
        html = template.render(context)
        pdf = HTML(
            string=html,
            base_url=self.request.build_absolute_uri("/"),
            url_fetcher=default_url_fetcher,
        ).write_pdf(stylesheets=self.stylesheets + [self.css])
        return pdf

    def get_filename(self):
        """
        Get the filename for the PDF document.
        Returns:
            str: The filename for the PDF document.
        """
        return self.file_name or "report.pdf"

    def render_pdf(self, context={}, *args, **kwargs):
        """
        Render the PDF document and return the HTTP response.
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response containing the PDF document.
        """

        pdf = BytesIO(self.get_document(context, *args, **kwargs))
        return FileResponse(
            pdf,
            content_type="application/pdf",
            as_attachment=self.attachment,
            filename=self.get_filename(),
        )
