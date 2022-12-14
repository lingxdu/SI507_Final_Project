# SI507_Final_Project

How to supply API keys
  API Key is a private one, so you need to apply for a key for Yelp Fusion API, and Google Places API separately. Your API Key will be automatically generated after you create your app in those two APIs.
  	Yelp Fusion API: You can click this link to apply the Yelp Fusion API key: https://docs.developer.yelp.com/docs/fusion-authentication. First, you need to sign in your Yelp account (sign up for one if you do not have!). Remember to verify your email, otherwise, you can't proceed! And then, following the guides shown in the link above: “Create APP”, fill in the necessary information, and click the button “save changes”, then the key will show up in a few minutes! Now you can copy your key to the variable named “yelp_api_key”.
  	Google Places API: first register for a Google Cloud account, and go to this page: https://console.cloud.google.com/welcome?project=protean-torus-371102 to find the “API & Services > Credentials” in the drop-down navigation, and then click “Create Credentials”, (remember to create a project before this step, otherwise, the page don’t show up). The key will also be generated in less than a second. Next, follow the instruction shown in this link: https://developers.google.com/maps/documentation/places/web-service/cloud-setup, to add billing info, and enable the Places API. Finally, copy the key to the variable “google_api_key”, and it's ready to run.

○	a brief description of how to interact with your program
  	Just click on this link http://127.0.0.1:5000 and the form will pop up automatically, students can first choose one university and one cuisine, and then they can not only decide whether to look at the price, rating, or distance but also the sort direction. Finally, restaurants that match their chosen best are displayed in sorted form. Also, a graph, table, and scatter chart will pop up when opening those HTML files in a browser.
  
  
Data Structure
  I organized the data into a tree. Showing below.
○	I would like to offer students of 8 universities in Michigan an optional choice of restaurants in terms of 6 cuisines.
○	The 8 universities are Central Michigan University, Eastern Michigan University, Michigan State University, Michigan Technological University, Oakland University, University of Michigan, Wayne State University, and Western Michigan University. 
○	The 6 types of cuisine are American, Chinese, Italian, Japanese, Mexican, and Thai.
○	For each university and cuisine, there are 30 restaurants with info like name, price, rating, distance, location, phone, coordinates, and nearby parks with it.
○	For each nearby park, the name, rating, type, vicinity, and user rating total are provided.

