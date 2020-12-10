# Photogram, my capstone project

Photogram is the name of my CS50 Web capstone project. It's a mobile-responsive website for online photo-sharing application and social network platform, similar to the famous app Instagram.
In Photogram, you can upload a post with an image and a caption. The users can like and comment on the posts. In addition to this, they can also follow each other's accounts, allowing them to see all their friend's posts easily on a timeline page. Photogram's users can also see each other profiles and edit their own. I decided to make this application as my final project because I believe it is more complex and challenging than Project 4 due to three big reasons, first, the post has an image; second, the users can like and comment on the posts; and third, the application is mobile-responsive. 

For this project, I used PIL/Pillow to help me do the image processing to my Python interpreter. This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities. The core image library is designed for fast access to data stored in a few basic pixel formats. It provides me a solid foundation for general image processing. 

Inside the "photogram" folder you can find all the essential files for this Django project. The first thing the user sees when accessing the Photogram website is the index page containing the menu on the top with buttons to login and register, and below it, a timeline displaying all posts from all users. The unsigned user can see the posts but he can't like or comment on them. The user will have to sign in to interact and create posts. Inside the 'view.py' file, the view function that deals with this part is named 'allPosts'. 

The register and login pages follow the same Project 4 sign in and sign up protocol. 

After the registration and log-in process, the user can edit his account and change the username, email, and the default profile image. By clicking on the 'Profile' button inside the top menu, the user will be redirected to his account page and find the button called 'Edit'. This 'Edit' button will take the user to a form page to edit his account information and upload a profile picture of his choice. The view function that handles this part is called 'profileEdit'. 

At the top menu, there is a button called 'Post Image', this button takes the user to another form page, but in this case, it's to create a new post for the user. First, you upload a image file from your device, and then, write a caption for that image. After clicking the 'Upload' button, you will able to see your newly created post at the timeline display. The view that handles all that is called 'createPost'. 

The like process is similar to Project 4's liking protocol. To like a post, you just have to click the heart image below every post, to unlike you just have to click it again. The view that handles this is called 'likePost'. 

To see and send comments on the posts, you just have to click the 'comments' button right next to the heart button. After clicking it, you'll see all the comments that other users have made before and send your own too. The 'comments' view function handle this process. The liking and commenting requests are AJAXs. 

By clicking on the post's username, you will be redirected to this user's account page. There you can see all his posts and follow him by clicking 'Follow'. You can not follow yourself. The view functions responsible for these processes are the 'profile' and 'follow'. 

And finally, the 'Following' page. It can be accessed by clicking on the 'Following' button at the top menu. There you can see the posts from the users that you are following. The view that handles it is the 'followingPosts' function. 

So there it is the Photogram website application, where you can upload photos with captions. You can add a caption to each of your posts and make them be seen by other users. Each post by a user appears on their follower's feeds and can also be viewed by the public. Users also have the option to customize their own profile picture. As with other social networking platforms, Photogram users can like and comment on others' posts.
