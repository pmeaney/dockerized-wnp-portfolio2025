from django import forms
from django.utils.safestring import mark_safe
from wagtail.admin.widgets import ChooserWidget
from .models import TagCategory, PortfolioTag

class TagCreationWidget(ChooserWidget):
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
                        <a href="/admin/snippets/portfolio/tagcategory/add/" 
                           class="button button-small button-primary tag-category-create-btn">
                            Create Tag Category
                        </a>
                    </div>
                </div>
            ''')
        
        # Check if any tags exist
        tags_exist = PortfolioTag.objects.exists()
        if not tags_exist:
            # Categories exist but no tags - provide guidance for creating tags
            return mark_safe(f'''
                <div class="tag-creation-guidance">
                    <p class="help">
                        <strong>No Tags Available</strong>
                    </p>
                    <div class="help-block">
                        <p>You have categories, but no tags have been created yet.</p>
                        <a href="/admin/snippets/portfolio/portfoliotag/add/" 
                           class="button button-small button-primary tag-create-btn">
                            Create New Tag
                        </a>
                    </div>
                </div>
            ''')
        
        # If categories and tags exist, render normal tag selection
        return super().render_html(name, value, attrs)

    def render_js_init(self, id_, name, value):
        # Custom JavaScript initialization if needed
        return f'createTagWidget("{id_}", "{name}", {value or "null"})'