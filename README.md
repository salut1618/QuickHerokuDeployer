# QuickHerokuDeployer
A script which allows for quick automatic deployment of big projects by avoiding reinstallation of build packs and packages and simply just updating the changed files


# Installation
1) Paste either python(make sure to include flask and requests in requirements.txt) or nodejs file onto the main directory of the big project
2) Put in your github token, repository name, branch
3) Put in the command which would be used to start the bigger project such as "node index.js"
4) Make sure the proc file would initiate the newly added file and not the big project
5) Important: Disable auto deploy in Heroku project settings>deploy.
6) Make sure the desired buildpacks are available
7) Important: Create a push event webhook from github
  a) go to your github repo
  b) go to settings
  c) go to webhook
  d) create a new webhook with the url of   https://HEROKU_PROJECT_NAME.herokuapp.com/payload
  e) select content-type of application/json
  f) make sure "just the push event" is selected in "Which events would you like to trigger this webhook?"
  
