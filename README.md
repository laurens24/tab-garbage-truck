# Tableau Garbage Truck

Welcome to the Tableau Cloud Garbage Truck Script!

This repository is intended for folks with 0 scripting or coding experience to be able to use a Scripting step in a Tableau Prep flow to move all of your unused workbooks to a single project folder in Tableau Cloud, making it easy to audit and purge stale content.


Before we get started, there are a few steps you'll need to take...

1. Clone this repository to your local machine. If you know what this means, skip to step 2. If not, follow the steps below-

- Create a GitHub account if you do not already have one
- Open the command prompt application of your computer. If you are on a Mac, this should be called "Terminal". On Windows, this should be called Command Prompt.
- Type `git config --global user.name "First Last"` where "First Last" is your first and last name. Press return/enter
- Type `git config --global user.email "your-email-address"` using the email address associated with your GitHub account. Press return/enter
- Type `ls` and press return/enter- this will list the contents of your current directory. You should see `Desktop` listed as one of the options
- Type `cd Desktop` and press return/enter - this will change your current directory to your Desktop, so now any commands will be executed within your Desktop folder
- Type `git clone https://github.com/laurens24/tab-garbage-truck.git` and press return/enter. On your Desktop, you should now see a folder called "tab-garbage-truck"

For more explanation / background about Git and how it's used, [take a look at this](https://info201.github.io/git-basics.html#what-is-this-git-thing-anyway)

2. Create a new Tableau Prep Flow, and be sure you're logged in to your Tableau Cloud site

_Note: You must use the Desktop application of Tableau Prep Builder. Tableau Cloud does not currently support running Python scripts in browser_

3. Connect to the Admin Insights "Site Content" data source from your Cloud site

4. Save your prep flow in the tab-garbage-truck folder that is now on your Desktop

5. Add a "Script" step to the data source in your Prep Flow

6. Edit the {insert value} fields in the xyz.csv to have the correct values in them

- How to get the PAT info
- How to get your POD
- How to get the LUID for your folder
