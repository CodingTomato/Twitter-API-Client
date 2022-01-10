console.log("Hello from main.js!");

const usernameTextfield = document.getElementById('usernameInput');

document.getElementById('searchTweets').addEventListener('click', () => {
  window.location.href = '/user/'+usernameTextfield.value+"/tweets";
});

document.getElementById('searchFollowers').addEventListener('click', () => {
  window.location.href = '/user/'+usernameTextfield.value+"/followers";
});