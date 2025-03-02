# CV-human-pose
A computer vision-based action recognition system to assist human-action password, project for UIUC cs 222

The system is going to detect people's actions under the camera and recognize some special body movements that can be used to set action passwords (such as raising hands to open the door) and other scenes that require action detection.

- Users can input videos in mp4 format for the program to recognize.
- Users can input png, jpeg and other formats for the program to recognize.
- If the input is a video, the program will mark the recognized human actions, such as running, jumping, etc., with squares on each frame, and annotate them with language. Finally, a marked video is output for users to watch. 
- The program can also label a single image in the same way for user to look at. 
- The program can identify what kind of posture is taken in the picture, like running, jumping, mark the position it takes place using rectangle lines and comments it, so that the users can see clearly.
- The program can learn automatically. When the user tells them to mark a kind of posture or movement it didn’t know, such as waving, it will try to understand and mark it when it sees similar movements in the upcomming pictures. 
- The program can make up a passcode that relates to the movements user have provided, and inform the users. 
- If the program is going to output a video, users can check to have the program output a word file. The file will contain a description of the entire set of actions recognized, such as what action a person performed at what minute and second.
- Users would have an interface that does the following: 
   - Provide users with some trained and recognizable actions in the form of an arrangement as a password.
   - After users have set the password, switch to the camera to check whether the actions are in the correct order.
- The program will calculate the password represented by the images and videos sent by the user on the back end and store it securely.
