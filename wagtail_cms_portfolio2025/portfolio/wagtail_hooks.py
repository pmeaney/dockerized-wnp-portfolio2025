from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from django.utils.translation import gettext_lazy as _
from .models import TagCategory, PortfolioTag
from wagtail import hooks
from django.utils.html import format_html

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
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .tag-creation-guidance:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .tag-creation-guidance .help {
        color: #333;
        margin-bottom: 12px;
        font-size: 16px;
        font-weight: 600;
    }
    
    .tag-creation-guidance .help strong {
        color: #0c536e;
    }
    
    .tag-creation-guidance .help-block {
        text-align: center;
    }
    
    .tag-creation-guidance .help-block p {
        margin-bottom: 15px;
        color: #555;
        font-size: 14px;
    }
    
    .tag-creation-guidance .button {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 18px;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .tag-creation-guidance .button:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .tag-creation-guidance .tag-category-create-btn {
        background-color: #43b1b0;
    }
    
    .tag-creation-guidance .tag-create-btn {
        background-color: #0c536e;
    }
    </style>
    '''

# Register the hook to add custom styles
from wagtail.admin.views.home import home_page
from wagtail.admin.views.generic import add_global_panel
from wagtail.admin.views.home import side_panels

add_global_panel(home_page, side_panels, add_tag_creation_styles)

@hooks.register('insert_global_admin_js')
def tag_creation_widget_js():
    """Add JavaScript for the tag creation widget workflow"""
    return format_html(
        """
        <script>
        function createTagWidget(id, name, value) {
            // Initialize tag creation workflow
            document.addEventListener('DOMContentLoaded', function() {
                // Get the widget container
                const widgetContainer = document.getElementById(id);
                
                if (!widgetContainer) return;
                
                // Find any creation buttons within the widget
                const createButtons = widgetContainer.querySelectorAll('.tag-creation-guidance a');
                
                createButtons.forEach(button => {
                    button.addEventListener('click', function(e) {
                        e.preventDefault();
                        
                        // Open the creation page in a new browser tab
                        const createUrl = this.getAttribute('href');
                        window.open(createUrl, '_blank');
                        
                        // Determine message based on button type
                        let message = 'After creating, please return to this page and refresh to continue.';
                        
                        if (button.classList.contains('tag-category-create-btn')) {
                            message = 'After creating a Tag Category, please return to this page and refresh to continue.';
                        } else if (button.classList.contains('tag-create-btn')) {
                            message = 'After creating a Tag, please return to this page and refresh to continue.';
                        }
                        
                        // Remind the user to refresh this page after creating
                        alert(message);
                    });
                });
            });
        }
        </script>
        """
    )