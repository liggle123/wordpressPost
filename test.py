from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo

wp = Client('http://ali.baldachin.cc/xmlrpc.php', 'baldachin', 'HanSh19781014')
getPost = wp.call(GetPosts())
for post in getPost:
    print(post)
