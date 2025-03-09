from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.models import Image
from wagtail.images.models import Image
from wagtail.snippets.models import register_snippet


@register_snippet
class TagType(models.Model):
    """Tag type for Bulma CSS styling"""
    NAME_CHOICES = [
        ('is-info', 'Info'),
        ('is-success', 'Success'),
        ('is-warning', 'Warning'),
        ('is-danger', 'Danger'),
        ('is-primary', 'Primary'),
        ('is-link', 'Link'),
        ('is-dark', 'Dark'),
        ('is-light', 'Light'),
    ]
    
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=20, choices=NAME_CHOICES, default='is-info')
    
    panels = [
        FieldPanel('name'),
        FieldPanel('style'),
    ]
    
    def __str__(self):
        return f"{self.name} ({self.get_style_display()})"


# Portfolio Tag with TagType
@register_snippet
class PortfolioTag(models.Model):
    name = models.CharField(max_length=255)
    tag_type = models.ForeignKey(
        'TagType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('tag_type'),
    ]
    
    def __str__(self):
        return self.name


# Portfolio Item Tags
class PortfolioItemPortfolioTag(models.Model):
    tag = models.ForeignKey(
        'PortfolioTag',
        on_delete=models.CASCADE,
        related_name='+'
    )
    portfolio_item = ParentalKey(
        'PortfolioItem',
        on_delete=models.CASCADE,
        related_name='portfolio_tags'
    )
    
    panels = [
        FieldPanel('tag'),
    ]


# Portfolio Index Page
class PortfolioIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    def get_context(self, request):
        context = super().get_context(request)
        # Get all the direct children of this page that are live
        portfolio_items = self.get_children().live().order_by('-first_published_at')
        context['portfolio_items'] = portfolio_items
        return context
    
    # Allow only PortfolioItem pages as children
    subpage_types = ['portfolio.PortfolioItem']
    
    # Allow this page to be created under HomePage
    parent_page_types = ['home.HomePage']
        
    class Meta:
        verbose_name = "Portfolio Index Page"
        verbose_name_plural = "Portfolio Index Pages"


# Portfolio Item Page
class PortfolioItem(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Buttons
    main_button_text = models.CharField(max_length=50, blank=True)
    secondary_button_text = models.CharField(max_length=50, blank=True, null=True)
    secondary_button_url = models.URLField(blank=True, null=True)
    
    # Only allow this page to be created under PortfolioIndexPage
    parent_page_types = ['portfolio.PortfolioIndexPage']
    
    # Don't allow any children underneath portfolio items
    subpage_types = []
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('thumbnail'),
        ], heading="Portfolio Item Metadata"),
        FieldPanel('intro'),
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('main_button_text'),
            FieldPanel('secondary_button_text'),
            FieldPanel('secondary_button_url'),
        ], heading="Button Links"),
        InlinePanel('portfolio_tags', label="Portfolio Tags"),
    ]
    
    def main_tags(self):
        return self.portfolio_tags.all()