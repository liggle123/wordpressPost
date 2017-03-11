#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, GetPost, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies
import markdown

os.chdir(sys.path[0])


def article_handle(filename):
    with open(filename, encoding='utf-8') as input_file:
        md_file = input_file.readlines()
    md_content = ''.join(md_file[1:])  # 配置第二行以后内容为正文
    if '<!--more-->' not in md_content:
        if input("文章内无分页符，确认请按‘y’，其他任意键取消： ") != 'y':
            sys.exit(0)
    html_content = markdown.markdown(md_content)  # 转换markdown为html

    post_title = ''.join(md_file[:1])  # 配置首行为标题
    # 手动输入文章英文地址及标签
    post_slug = input('请输入文章%s地址（英文）：\n' % (post_title.split()))
    post_tag = input('请输入文章tag标签，以空格分隔：\n').encode('utf-8').decode('utf-8').split()
    # 分类暂定为“随笔”
    while True:
        choice = int(input("请选择文章分类：\n1、随笔；2、产品工作\n"))
        if choice == 1:
            post_category = ['随笔']
            break
        elif choice == 2:
            post_category = ['产品工作']
            break
        else:
            print('输入错误！请重新输入')
    # 定义post内容
    post = WordPressPost()
    post.title = post_title
    post.content = html_content
    post.terms_names = {
        'post_tag': post_tag,
        'category': post_category
    }
    post.slug = post_slug
    post.post_status = 'publish'
    print("Article Content: \n%s\n\n\n"
          "Article Title: %s - %s\n"
          "Article Category: %s\n"
          "Article Tag: %s\n" % (
              post.content, post.title, post.slug, post.terms_names['category'], post.terms_names['post_tag']
          ))
    confirm = input("确认请按‘y’，其他任意键取消： ")
    if confirm == 'y':
        return post
    else:
        return None
    # print("%s\n%s" % (post_title, html_content))


# article_handle("test.md")
account_me = {
    'xmlrpc_url': 'https://baldachin.me/xmlrpc.php',
    'username': 'baldachin',
    'password': 'HanSh19781014'
}
account_ali = {
    'xmlrpc_url': 'http://ali.baldachin.cc/xmlrpc.php',
    'username': 'baldachin',
    'password': 'HanSh19781014'
}


def new_post(account, post):
    wp = Client(account['xmlrpc_url'], account['username'], account['password'])
    post.id = wp.call(NewPost(post))
    tmp = wp.call(GetPost(post.id))
    print("GetPost: %s - %s - %s" % (tmp.id, tmp.title, tmp.link))
    # wp.call(NewPost(post)) # 提交post内容


# 测试获取文章，两种方式
# getPost = wp.call(GetPosts())
# for post in getPost:
#     print("%s - %s - %s" %(post.id, post.title, post.link))
# tmppost = wp.call(GetPost(915))
# print("GetPost: %s - %s - %s" %(tmppost.id, tmppost.title, tmppost.link))

# wp.call(EditPost(781, post))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("请将文件拖曳到本脚本！")
        sys.exit(0)
    elif len(sys.argv) >= 3:
        print("本脚本仅支持单一文件发布！")
        sys.exit(0)
    file = sys.argv[1:]
    post = article_handle(file[0])
    if post:
        new_post(account_me, post)
        new_post(account_ali, post)

    input("发布完成，按任意键关闭")
