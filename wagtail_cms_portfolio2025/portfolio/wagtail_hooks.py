from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from django.utils.translation import gettext_lazy as _
from .models import Tag
from wagtail import hooks
from django.utils.html import format_html
from django.templatetags.static import static

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    """
    Enhanced Wagtail admin experience for Tags
    """
    model = Tag
    menu_label = "Tags"
    icon = "tag"
    add_to_settings_menu = False
    list_display = ["value", "category"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add helpful context for empty states
        if not self.model.objects.exists():
            context['empty_message'] = _(
                "No tags exist yet. "
                "Create your first tag to start organizing portfolio items!"
            )
        
        return context

# Register custom CSS
@hooks.register('insert_global_admin_css')
def tag_creation_styles():
    """Add CSS for the tag creation widget workflow"""
    return format_html(
        """
        <style>
        .tag-creation-guidance {{
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .tag-creation-guidance:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .tag-creation-guidance .help {{
            color: #333;
            margin-bottom: 12px;
            font-size: 16px;
            font-weight: 600;
        }}
        
        .tag-creation-guidance .help strong {{
            color: #0c536e;
        }}
        
        .tag-creation-guidance .help-block {{
            text-align: center;
        }}
        
        .tag-creation-guidance .help-block p {{
            margin-bottom: 15px;
            color: #555;
            font-size: 14px;
        }}
        
        .tag-creation-guidance .button {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 18px;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .tag-creation-guidance .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .tag-creation-guidance .tag-create-btn {{
            background-color: #0c536e;
        }}
        </style>
        """
    )

@hooks.register('insert_global_admin_js')
def tag_creation_widget_js():
    """Add JavaScript for the tag creation widget modal workflow"""
    # Ensure Wagtail's modal workflow script is loaded
    return format_html(
        """
        <script src="{}"></script>
        <script>
        // Make sure modal workflow is initialized
        document.addEventListener('DOMContentLoaded', function() {{
            // Reference to Wagtail's ModalWorkflow
            var ModalWorkflow = window.ModalWorkflow;
            
            // If not available, try to import it
            if (!ModalWorkflow) {{
                try {{
                    // This is a fallback for newer Wagtail versions
                    ModalWorkflow = window.wagtail.admin.modalWorkflow;
                }} catch(e) {{
                    console.error('Modal workflow not found:', e);
                }}
            }}
            
            // Define a global to make it available to inline scripts
            window.PortfolioModalWorkflow = ModalWorkflow || function(options) {{
                // Fallback: just open in a new tab if modal not available
                console.warn('Modal workflow not available, opening in new tab');
                window.open(options.url, '_blank');
                if (options.onload && options.onload.close) {{
                    // Still provide a way to refresh when returning
                    alert('After creating, please return to this page and refresh to continue.');
                }}
            }};
        }});
        </script>
        """,
        static('wagtailadmin/js/modal-workflow.js')
    )