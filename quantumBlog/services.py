# QuantumIndex/quantumBlog/services.py

import datetime
from django.db.models import Count
from .models import Post

def get_trending_posts(days=7, limit=5):
    return Post.objects.filter(
        published=True,
        created_at__gte=datetime.now() - datetime.timedelta(days=days)
    ).annotate(
        review_count=Count('reviews')
    ).order_by('-review_count', '-created_at')[:limit]