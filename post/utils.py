from utils import purge_template_cache

def purge_comment_cache(post_id):
    purge_template_cache(cache_name="comment", identify=post_id)