# E33a Wiki

### Design decisions info

##### Functions 

* html_from_markdown(content) : This function does all conversion from markdowns to html.
* save_entry : saves an updated entry
* new_entry : saves a new entry, instead of merge add and update into the same function, I decided to keep separated. 
* In general, I tried to reuse as much as I could already existing funtions.


##### Views and Template

* When applicable, the same view process the GET and POST method.
* One view for ADD and another for UPDATE. I tried to combine in the same view but I considered too complicaded to implement and probably harder to maintain the code. KISS approach.
* Layout. Not sure if this is the right approach. But I implemented the same template ADD for both views: ADD and UPDATE. It worked, not to complicated to do it, but I believe for complex forms it will be very hard to maintain. 


##### REGEX
* I had the impression that this project was to learn regex, instead of web development using Python. Not sure if I missed some section, but it would be good to have specific session to explain regex for dummies, the documentation is tough to follow, too many options, it isnt't a natural reading, but really powerful when you learn it.
* The section were fundamental to solve some regex for the project.
* The one to add <p>, my apologizes but I copied this from Vlad´s example, published at Ed´s, my one was using string compare for the first two characters, his aproach was much better. 