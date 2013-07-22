from blogm.utils import purge_template_cache

def purge_comment_cache(post_id):
    purge_template_cache(cache_name="comment", identify=post_id)

def sort_replies(replies):
    """
    Return replies with groupped by parent_id

    key = comment_id|reply_id
    value = reply's replies object
    {key:value, key:value,..}

    example return data:
    {
        2:  [<Comment: 49>, 
             <Comment: 50>, 
             <Comment: 51>
            ],
        3:  [<Comment: 4>],
        4:  [<Comment: 44>],
        44: [<Comment: 46>],
        46: [<Comment: 47>],
        47: [<Comment: 48>],
        50: [<Comment: 52>]
    }
    """
    # create empty dict
    _replies = {}

    for r in replies:
        # if reply's parent_id is not in the dict
        if not r.parent_id in _replies:
            # add reply's parent_id as a dict key and make empty list
            _replies[r.parent_id] = []
        # add reply to parent_id's list
        _replies[r.parent_id].append(r)

    # return new dict
    return _replies