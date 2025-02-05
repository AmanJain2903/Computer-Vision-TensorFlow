# Deploying API to Heroku

This guide will walk you through the steps to deploy your API to Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed
- A completed API project

## Steps

### 1. Prepare Your Project

Ensure your project has the following files:
- `requirements.txt` - List of dependencies
- `Procfile` - Specifies the commands that are executed by the app on startup

Example `Procfile`:
```
web: python app.py
```

### 2. Log in to Heroku

Open your terminal and log in to Heroku:
```sh
heroku login
```

### 3. Create a New Heroku App

Navigate to your project directory and create a new Heroku app:
```sh
cd /path/to/your/project
heroku create your-app-name
```

### 4. Deploy Your Code

Initialize a git repository, add your files, and deploy to Heroku:
```sh
git init
git add .
git commit -m "Initial commit"
git push heroku master
```

### 5. Scale the App

Ensure at least one instance of the app is running:
```sh
heroku ps:scale web=1
```

### 6. Open Your App

Open your deployed app in the browser:
```sh
heroku open
```

### 7. View Logs

To view the logs of your app, use:
```sh
heroku logs --tail
```

## Conclusion

You have successfully deployed your API to Heroku. For more advanced configurations and management, refer to the [Heroku documentation](https://devcenter.heroku.com/).
