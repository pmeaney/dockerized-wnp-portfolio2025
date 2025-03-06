from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from django.utils.translation import gettext_lazy as _
from .models import TagCategory, PortfolioTag

@register_snippet
class TagCategorySnippetViewSet(SnippetViewSet):
    """
    Enhanced Wagtail admin experience for Tag Categories
    """
    model = TagCategory
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add helpful context for empty states
        if not self.model.objects.exists():
            context['empty_message'] = _(
                "No tag categories exist yet. "
                "Create your first tag category to start organizing tags!"
            )
        
        return context

@register_snippet
class PortfolioTagSnippetViewSet(SnippetViewSet):
    """
    Enhanced Wagtail admin experience for Portfolio Tags
    """
    model = PortfolioTag
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if categories exist
        if not TagCategory.objects.exists():
            context['empty_message'] = _(
                "⚠️ Cannot create tags: No categories exist. "
                "Please create a Tag Category first!"
            )
        
        return context

# Optional: Add some CSS to style the guidance
def add_tag_creation_styles(request):
    return '''
    <style>
    .tag-creation-guidance {
        background-color: #f0f0f0;
        border: 1px solid #ddd;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 4px;
    }
    .tag-creation-guidance .help {
        color: #333;
        margin-bottom: 10px;
    }
    .tag-creation-guidance .help-block {
        text-align: center;
    }
    .tag-creation-guidance .button {
        display: inline-block;
        margin-top: 10px;
    }
    </style>
    '''

# Register the hook to add custom styles
from wagtail.admin.views.home import home_page
from wagtail.admin.views.generic import add_global_panel
from wagtail.admin.views.home import side_panels

add_global_panel(home_page, side_panels, add_tag_creation_styles)