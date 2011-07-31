#! /usr/bin/python

import datetime
import git
import optparse
import os
import subprocess
import sys

post_file_format = '%s-%s.markdown'

def dprint(inString):
    '''debug print'''
    if True:
        print inString

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
    # grab the post title as the first line from the file
    lines = open(post, 'r').readlines()
    title = lines.pop(0).rstrip()
    body = ''.join(lines)
    # make sure the post doesn't already exist
    rename_slug = False
    slug = title.lower().replace(' ', '-')
    date_string = datetime.datetime.now().strftime('%Y-%m-%d')
    target_post_file = post_file_format % (date_string, slug)
    if os.path.exists(os.path.join(opts.blog_root, 'source', '_posts', target_post_file)):
        rename_slug = True
        print "WARNING: target post file '%s' exists, renaming new post file." % target_post_file
        count = 0
        target_post_file = post_file_format % (date_string, slug + '-' + str(count))
        while os.path.exists(os.path.join(opts.blog_root, 'source', '_posts', target_post_file)):
            count += 1
            target_post_file = post_file_format % (date_string, slug + '-' + str(count))
        # we have a good file to use, change the title
        title += ' %s' % count
    # create a new post with 'rake new_post'
    new_post = subprocess.Popen("rake new_post['%s']" % title, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    n_stdout, n_stderr = new_post.communicate()
    if n_stderr:
        print "ERROR: new post generation failed\n%s" % n_stderr
        sys.exit(1)
    # grab the file name from the rake process
    post_file = n_stdout.rstrip().split('source/_posts/')[-1]
    # open the file to edit it
    post_file_path = os.path.join(opts.blog_root, 'source', '_posts', post_file)
    pf_handle = open(post_file_path, 'a')
    # copy the text into the body of the markdown file
    pf_handle.write(body)
    pf_handle.close()
    # add and commit file to git if desired
    if opts.commit:
        repo = git.Repo(opts.blog_root)
        repo.index.add([post_file_path.replace(opts.blog_root,'')])
        repo.index.commit('added post %s\ncommited automatically by the octomars script' % post_file)
        # push to remote if desired
        if opts.push:
            repo.remotes.origin.push()
    # rake generate
    if opts.generate:
        generate = subprocess.Popen('rake generate', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        g_stdout, g_stderr = generate.communicate()
    # rake deploy
    if opts.generate:
        deploy = subprocess.Popen('rake deploy', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        d_stdout, d_stderr = deploy.communicate()
    # go back to the directory we started in
    os.chdir(old_pwd)

def main():
    """The main functionality and entry point for OctoMars."""
    parser = optparse.OptionParser(usage='Publish blog posts from MarsEdit in the Octopress blog system.')
    parser.add_option('--no-generate', action='store_false', dest='generate', default=True, help='Do not generate static pages. Implies --no-deploy.')
    parser.add_option('--no-deploy', action='store_false', dest='deploy', default=True, help='Do not deploy after generating static pages.')
    parser.add_option('--commit', action='store_true', dest='commit', default=False, help='Add and commit file to git repo.')
    parser.add_option('--push', action='store_true', dest='push', default=False, help='Push git repo to the origin. Implies --commit.')
    parser.add_option('--blog-root', action='store', dest='blog_root', default=None, help='The root directory of the Octopress repository.')

    (opts, args) = parser.parse_args()

    # if we're not generating we're not deploying (I mean really, why are we running this 
    # without generating in the first place? Mostly for testing I guess.)
    if not opts.generate:
        opts.deploy = False
    
    if opts.push:
        opts.commit = True
    
    # work on all files passed in
    for post in args:
        process_post(post, opts)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
