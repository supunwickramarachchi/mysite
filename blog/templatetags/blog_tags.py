from django import template
from ..models import Post, Comment
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.xhtml')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def total_comments():
    return Comment.active_comments.count()

@register.inclusion_tag('blog/post/post_with_comment.xhtml')
def show_comment_posts(limit=3):
    comment_posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .annotate(comment_count=Count('comments'))
        .filter(comment_count__gt=0)
        .order_by('-comment_count')[:limit]
    )
    return {'comment_posts': comment_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))