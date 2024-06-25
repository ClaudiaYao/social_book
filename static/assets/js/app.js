
"use strict"

console.log("start the js");
let alertWrapper = document.querySelector(".alert");
let alertClose = document.querySelector(".alert__close");

if (alertWrapper) {
addEventListener("click", () => {
  alertWrapper.style.display = 'none';
}
)
};

// Django is a synchronized application, so any submit will result into a reloading from the server. To overcome this, we could create Django Rest framework and then use JS to call the API to realized asynchronized updating.
// check this post https://stackoverflow.com/questions/68475595/perform-action-from-a-form-or-link-without-refreshing-the-page-view-with-django

let like_btns = document.getElementsByClassName("like_emoji");
if (like_btns) {
    for (let i = 0; i < like_btns.length; i++) {
        console.log("catch the like btn")
        let like_btn = like_btns[i];
        like_btn.addEventListener("click", (e) => {
            let like_value = 0;
            if (like_btn.getAttribute("fill") == "currentColor") {
                like_btn.setAttribute("fill", "red");
                like_value = 1;
            } else {
                like_btn.setAttribute("fill", "currentColor");
            }

            
            fetch("http://127.0.0.1:8000/api/like_post/" + like_btn.getAttribute("value") + "/", {
              method: "POST",
              headers: {
                Authorization: "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5Mjk2NDEzLCJpYXQiOjE3MTkyOTQ2MTMsImp0aSI6IjEyNTVjZWRkM2VjMzQ4NzFhNzRjZjA1MjNkYzk5M2Y1IiwidXNlcl9pZCI6MX0.Vufl-hXrZPhnFaOR9YTddwkDSJ67SBWRFJqpquCIj_M",
                "Content-Type": "application/json"
              },
              body: JSON.stringify({
                  "like": like_value
              })
          }).then(response => response.json()).then((data) => {
              // use e.currentTarget will generate error
              console.log(data)
          })





        })
    }
};

