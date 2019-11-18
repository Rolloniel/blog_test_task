def get_model():
    from custom_comments.models import CustomComment
    return CustomComment

def get_form():
    from custom_comments.forms import CustomCommentForm
    return CustomCommentForm