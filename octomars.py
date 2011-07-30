#! /usr/bin/python

import optparse
import os
import subprocess
import sys

def find_blog_root(inFilePath):
    """find the path of the blog repository so it can be known where to run commands and put files."""
    blog_root = None
    (dir_path, file_name) = os.path.split(inFilePath)
    # confirm a source directory as a parent of both _posts and where this file comes from
    if dir_path.count('source'):
        # get the part of the path before 'source'
        test_path = dir_path.split('source')[0]
        # see if we have the config file
        if os.path.exists(os.path.join(test_path, '_config.yml')):
            # we have our path, make it the blog_root
            blog_root = test_path
    # need to add more tests here, bail out for now if we can't find the path
    if not blog_root:
        print "ERROR: cannot determine blog root path, stopping."
        sys.exit(1)
    return blog_root

def process_post(post, opts):
    if not os.path.exists(post):
        print "ERROR: file does not exist '%s'" % post
        sys.exit(1)
    # find the blog root from the file path if it's not set
    if not opts.blog_root:
        opts.blog_root = find_blog_root(post)
    old_pwd = os.getcwd()
    os.chdir(opts.blog_root)
    # discover the post slug
    # - make sure '_' is changed to '-'
    slug = os.path.splitext(os.path.basename(post))[0]
    slug = slug.replace('_', '-')
    # grab the post title as the first line from the file
    lines = open(post, 'r').readlines()
    title = lines.pop(0)
    body = ''.join(lines)
    # create a new post with 'rake new_post'
            
    # copy the text into the body of the markdown file
    # commit file to git if desired
    # push to remote if desired
    # rake generate
    # rake deploy
    # go back to the directory we started in
    os.chdir(old_pwd)

def main():
    """The main functionality and entry point for OctoMars."""
    parser = optparse.OptionParser(usage='Publish blog posts from MarsEdit in the Octopress blog system.')
    parser.add_option('--no-generate', action='store_false', dest='generate', default=True, help='Do not generate static pages. Implies --no-deploy.')
    parser.add_option('--no-deploy', action='store_false', dest='deploy', default=True, help='Do not deploy after generating static pages.')
    parser.add_option('--commit', action='store_true', dest='commit', default=False, help='Add and commit file to git repo.')
    parser.add_option('--push', action='store_true', dest='commit', default=False, help='Push git repo to the origin.')
    parser.add_option('--blog-root', action='store', dest='blog_root', default=None, help='The root directory of the Octopress repository.')

    (opts, args) = parser.parse_args()

    # if we're not generating we're not deploying (I mean really, why are we running this 
    # without generating in the first place? Mostly for testing I guess.)
    if not opts.generate:
        opts.deploy = False
    
    # work on all files passed in
    for post in args:
        process_post(post, opts)
        
    # 
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
