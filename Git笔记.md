# Git学习

## 相关资料
[Avoid 80% of Git merge conflicts][1]

[Learn Git with Bitbucket Cloud][2]

[Git简明教程][3]

[Git教程 廖雪峰][4]

[Merge vs Rebase][5]


[1]:https://medium.com/front-end-hacking/avoid-80-of-merge-conflicts-with-git-rebase-b5d755a082a6               
[2]:https://www.atlassian.com/git/tutorials/learn-git-with-bitbucket-cloud
[3]:http://rogerdudler.github.io/git-guide/index.zh.html  
[4]:https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/
[5]:https://mislav.net/2013/02/merge-vs-rebase/

## 笔记


### 相关指令

* ### 拉取远端
    * ***从远端分支pull 到本地分支***  
    `git pull origin dev:remotedev`

* ### 添加和提交  
    * ***git add***
        * _将文件的修改，文件的删除，文件的新建，添加到暂存区_  
        `git add -A`
        * _将文件的修改、文件的删除，添加到暂存区_  
        `git add -u`
        * _将文件的修改，文件的新建，添加到暂存区。_  
        `git add .`
    * ***git commit***
        * `git commit -m “”`
        * `git commit -a`

* ### 推送改动
    * ***远端不存在该分支时***      
      `git  push origin dev:remotedev`     
    * ***与远端进行追踪***      
      `git branch --set-upstream dev origin/removedev`
    * ***进行推送***       
      `git push`
   

* ### 分支
    * ***查看本地分支***        
    `git branch`
    * ***查看远程分支***  
    `git branch -r`
    * ***新建分支***  
    `git branch dev`
    * ***切换分支***  
    `git checkout dev`
    * ***新建并切换分支***  
    `git checkout -b dev`
    * ***从远程分支pull下来并新建一个分支***  
    `git checkout -b dev origin/remotedev`
    * ***删除分支***  
    `git branch -d dev`
    * ***跟新远程分支***    
    `git remote update origin --prune`
    

* ### 多人协作模式下进行推送
    1. _尝试使用push推送自己的修改_  
     `git push`
    2. _如果失败，说明远端分支更新，需先pull进行合并_  
     `git pull`
    3. _如果有冲突先解决冲突，使用merge或rebase（区别：merge只是合并另外一个分支的内容，rebase也合并另外一个分支的内容，但是会把本分支的commits顶到最顶端）_  
     `git merge dev`  
     `git rebase dev`
      
        * _rebase还可以合并commit(HEAD~2表示两个commit)_   
        `git rebase -i HEAD～2`
        * _rebase回到之前的状态_  
        `git reset HEAD --hard`
        * _merge回到之前的状态_  
        `git merge --abort`
    4. _解决完冲突在push_  
     `git push`


* ### 日志和状态
    * ***查看日志***  
    `git log`
    * ***查看状态***  
    `git status`