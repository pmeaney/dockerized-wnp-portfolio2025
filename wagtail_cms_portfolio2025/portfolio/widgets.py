from django import forms
from django.utils.safestring import mark_safe
from wagtail.admin.widgets import AdminChooser
from .models import TagCategory, PortfolioTag

class TagCreationWidget(AdminChooser):
    """
    A custom widget that provides guided tag creation workflow
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = PortfolioTag

    def render_html(self, name, value, attrs):
        # Check if any tag categories exist
        tag_categories = TagCategory.objects.exists()
        
        if not tag_categories:
            # No categories exist - provide guidance
            return mark_safe(f'''
                <div class="tag-creation-guidance">
                    <p class="help">
                        <strong>No Tag Categories Exist</strong>
                    </p>
                    <div class="help-block">
                        <p>Before creating tags, you must first create at least one Tag Category.</p>
                        <a href="/admin/portfolio/tagcategory/add/" 
                           class="button button-small button-primary">
                            Create Tag Category
                        </a>
                    </div>
                </div>
            ''')
        
        # If categories exist, render normal tag selection
        return super().render_html(name, value, attrs)

    def render_js_init(self, id_, name, value):
        # Custom JavaScript initialization if needed
        return f'createTagWidget("{id_}", "{name}", {value or "null"})'