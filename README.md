# Hypheny project

## Description

Hypheny is an android real-time messaging application, which allows android users to communicate, send text messages, designed to provide real-time connections without compromising user privacy. Our project focuses on enabling safe communication while strictly protecting user data.

## Technologies

We used xml and kotlin for the frontend development because they are native android languages recommended for android development.  We used Python for back-end development and Flask framework to handle http requests. Regarding the database choice, we used MongoDB for its scalability, in order to be able to handle high amounts of users resulting in large data loads.

## Features

-Authentication system: Users can create accounts and log in with their credentials.

-Profile management: Users can update their profile, changing their username and password.

-Contact list management: Users can add friends, accept requests or block contacts.

-Messaging system: Users can send and receive messages with a few seconds latency.

## Files

| Folder/File| Description
--- | ---
main.py |  It includes API routes for user registration, login, and searching users by username or ID,  profile management, friendship requests, and messaging functionalities, creating and accessing conversations, and sending messages. 
services | Includes helper functions to support API functionalities 
models| Contains the conversation, message and user models for a mongoDB database using mongoengine.
controllers | Handles interaction with the database, as retrieveing conversations by user_id or retrieving messages from a conversation.

## Usage

1.clone the repository
```
git clone https://github.com/ArseneGiriteka/hyphenyApi.git
```
2.Navigate to the directory
3. Install the requirements
```
pip install -r requierments.txt
```
4. Start the flask server
```
python main.py
```

## Architecture

![Blank diagram (1)](https://github.com/user-attachments/assets/526c0916-766c-4010-badf-b8021dc78439)

## Authors
Arsène Giriteka

Leila Louajri
