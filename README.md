#### Introduction

Avg.80 mins per day is allocated for this personal project.

----------------
###### Previous:

>Until Commits on Jul 13, 2019, cb68b60

This script will read off from .txt file which contains macro actions. But currently only supports image-search based macros, no 'wait' or 'keypress' kinda things yet. Will eventually be implemented when I'm out of army. Got motif from android app 'Frep' by strai.

[Example Usage](https://youtu.be/_ichOg5tf8Y)

-----------------
###### New:

>After Commits on Feb 21, 2020, 5bdc73d

Completely rewriting with GUI, OOP.

Now has separated Macro Editor & Player window. Many functions are not implemented yet.
But basic functions works without significant issue. (Variables, Loops don't work yet)


**Current State:** (v0.0.3)
![Imgur](https://imgur.com/JSpTtFS.jpg) 
[Demo video - v0.0.3](https://youtu.be/X6gr9fZ5Vk8)


###### Features (Will format this later):

Support on-Success / on-Fail conditional macro sequencing.
With this, one can easily make IF-like branching sequence or infinite loop too.
This is demonstrated in demo video above.

FYI, uses json serialization to save & load macro sequence, too.

Still working on other macro components.
