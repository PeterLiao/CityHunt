from django.contrib import admin
from LeaderBoard.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(City)
admin.site.register(CommentLike)
admin.site.register(PostLike)
