document.getElementById('landingForm').addEventListener('submit', function(event) {
  event.preventDefault();

  fetch('/', {
    method: 'POST',
    body: new FormData(this)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      document.getElementById('successMessage').textContent = `Your username is ${data.username} and your PIN is ${data.pin}. You will be redirected to the login page.`;
      new bootstrap.Modal(document.getElementById('successModal')).show();
      let countdownTime = 5; // Change this value to set countdown time
      let countdown = setInterval(function() {
        document.getElementById('timer').innerHTML = countdownTime + " seconds remaining before redirection.";
        countdownTime--;
        if(countdownTime < 0 ){
          clearInterval(countdown);
          window.location.href = "/login";
        }
      }, 1000);
    } else {
      document.getElementById('failureMessage').textContent = data.message;
      new bootstrap.Modal(document.getElementById('failureModal')).show();
    }
  });
});


document.getElementById('startOver').addEventListener('click', function() {
  location.reload();
});

document.getElementById('refresh').addEventListener('click', function() {
  fetch('/new-operation', {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    // Update the operation on the page
    document.querySelector('h3').textContent = data.operation;
  });
});


