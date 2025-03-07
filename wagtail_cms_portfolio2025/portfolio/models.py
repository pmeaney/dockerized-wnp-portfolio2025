from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from .widgets import TagCreationWidget 

class Tag(models.Model):
    """
    Model for tags with explicit value and category
    """
    CATEGORY_CHOICES = [
        ('year', 'Year'),
        ('framework', 'Framework'),
        ('programming_language', 'Programming Language'),
        ('topic', 'Topic'),
        ('subtopic', 'Subtopic'),
        ('default', 'Default')
    ]
    
    value = models.CharField(
        max_length=255, 
        help_text="Tag value"
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='default',
        help_text="Category of the tag"
    )
    
    def __str__(self):
        return f"{self.value} ({self.get_category_display()})"
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        unique_together = ('value', 'category')

class PortfolioItem(Page):
    """
    Individual portfolio project page with tags and buttons.
    """
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    # Featured image (thumbnail)
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Button fields
    main_button_text = models.CharField(
        max_length=50,
        blank=False,
        help_text="Text for the main call-to-action button"
    )
    
    secondary_button_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Text for the secondary button (optional)"
    )
    
    secondary_button_url = models.URLField(
        blank=True,
        help_text="URL for the secondary button"
    )
    
    # Tags relationship
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='portfolio_items'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('thumbnail'),
        MultiFieldPanel([
            FieldPanel('main_button_text'),
            FieldPanel('secondary_button_text'),
            FieldPanel('secondary_button_url'),
        ], heading="Buttons"),
        FieldPanel('tags', widget=TagCreationWidget),
    ]
    
    # This restricts where this page type can be created
    parent_page_types = ['portfolio.PortfolioIndexPage']
    
    # This prevents any page types from being created beneath portfolio items
    subpage_types = []

    def get_main_button_url(self):
        """Returns the page slug to use as the main button URL"""
        return self.slug
    
    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"

class PortfolioIndexPage(Page):
    """
    Index page for listing portfolio items.
    """
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    # This restricts what page types can be created beneath this index page
    subpage_types = ['portfolio.PortfolioItem']
    
    class Meta:
        verbose_name = "Portfolio Index Page"
        verbose_name_plural = "Portfolio Index Pages"
    
    def get_context(self, request):
        context = super().get_context(request)
        context['portfolio_items'] = PortfolioItem.objects.child_of(self).live().order_by('-date')
        return context