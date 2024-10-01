let currentMailbox = 'inbox'; // Global variable to track the current mailbox

document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  const inboxButton = document.querySelector('#inbox');
  const sentButton = document.querySelector('#sent');
  const archivedButton = document.querySelector('#archived');
  const composeButton = document.querySelector('#compose');

  // Log the buttons to verify they are correctly found in the DOM
  console.log(inboxButton, sentButton, archivedButton, composeButton);

  // Set up event listeners for mailbox buttons
  if (inboxButton) inboxButton.addEventListener('click', () => select_tab('inbox'));
  if (sentButton) sentButton.addEventListener('click', () => select_tab('sent'));
  if (archivedButton) archivedButton.addEventListener('click', () => select_tab('archived'));
  if (composeButton) composeButton.addEventListener('click', () => select_tab('compose'));

  // Load the inbox by default when the page is loaded
  select_tab('inbox');

  // Set up event listener for the compose email form submission
  document.querySelector('#compose-form').addEventListener('submit', send_email);
});


/**
 * Function to handle tab selection and load the corresponding view.
 * @param {string} tab - The tab name ('inbox', 'sent', 'archived', or 'compose')
 */
function select_tab(tab) {
  // Remove 'selected' class from all buttons to reset their state
  document.querySelectorAll('.button').forEach(button => button.classList.remove('selected'));

  // Find the button element corresponding to the selected tab
  const tabButton = document.querySelector(`#${tab}`);

  // Check if the button exists before trying to add a class
  if (tabButton) {
    tabButton.classList.add('selected'); // Highlight the selected tab
  } else {
    console.error(`Button with ID #${tab} not found. Please check the ID.`);
    return; // Stop execution if the button is not found
  }

  // Handle tab-specific behavior
  switch (tab) {
    case 'compose':
      compose_email(); // Show the compose form
      break;
    case 'inbox':
    case 'sent':
    case 'archived':
      load_mailbox(tab); // Load the respective mailbox view
      break;
    default:
      console.error(`Unsupported tab: ${tab}`); // Log error for unsupported tabs
  }
}


/**
 * Function to display the compose email form, with optional fields pre-filled for replies.
 * @param {object} replyToEmail - The email object containing reply details, or null for new emails.
 */
function compose_email(replyToEmail = null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Clear out fields to prepare for a new email composition
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Pre-fill fields if composing a reply
  if (replyToEmail && replyToEmail.subject) {
    document.querySelector('#compose-recipients').value = replyToEmail.sender;

    // Prepend "Re:" only if it's not already part of the subject line
    document.querySelector('#compose-subject').value = replyToEmail.subject.startsWith('Re:')
      ? replyToEmail.subject
      : `Re: ${replyToEmail.subject}`;

    // Format the body to include the original message as part of the reply
    document.querySelector('#compose-body').value = `\n\nOn ${formatTimestamp(replyToEmail.timestamp)}, ${replyToEmail.sender} wrote:\n${replyToEmail.body}`;
  }
}


/**
 * Helper function to format a timestamp into a more readable string format.
 * @param {string} timestamp - The original timestamp string from the email data.
 * @returns {string} - A human-readable formatted timestamp.
 */
function formatTimestamp(timestamp) {
  // Create a new Date object from the timestamp
  const date = new Date(timestamp);
  
  // Format the date to a readable string format
  return date.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
    hour12: true,
  });
}


/**
 * Function to load and display emails from the specified mailbox.
 * @param {string} mailbox - The name of the mailbox to load ('inbox', 'sent', 'archived').
 */
function load_mailbox(mailbox) {
  currentMailbox = mailbox; // Update the current mailbox state

  // Show the emails view and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Set the title of the mailbox being viewed
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch and display emails from the selected mailbox
  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      // Clear any existing emails in the view
      document.querySelector('#emails-view').innerHTML += '';

      // Loop through each email and render it on the page
      emails.forEach(email => {
        const emailDiv = document.createElement('div');
        emailDiv.className = 'email-item';
        emailDiv.innerHTML = `<b>${email.sender}</b> ${email.subject} <span class="timestamp">${email.timestamp}</span>`;
        emailDiv.style.backgroundColor = email.read ? '#aaaaaa' : 'white';
        emailDiv.style.padding = '10px';
        emailDiv.style.border = email.read ? '1px solid #333333' : '1px solid #aaaaaa';
        emailDiv.style.margin = '10px 0';

        // Add click event to open and view the email
        emailDiv.addEventListener('click', () => {
          // Remove 'selected' class from all other emails
          document.querySelectorAll('.email-item').forEach(item => item.classList.remove('selected'));

          // Highlight the clicked email
          emailDiv.classList.add('selected');

          // Display the email details
          view_email(email.id);
        });

        // Append the email element to the emails view
        document.querySelector('#emails-view').append(emailDiv);
      });
    });
}


/**
 * Function to handle sending an email when the form is submitted.
 * @param {Event} event - The form submission event.
 */
function send_email(event) {
  event.preventDefault(); // Prevent the form from submitting the default way

  // Gather form data
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send the email data to the server via a POST request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(result => {
    if (result.error) {
      console.error(result.error); // Log any errors received from the server
    } else {
      select_tab('sent'); // Focus the "Sent" tab, visually and logically
    }
  })
  .catch(error => {
    console.error('Error:', error); // Log any network or other errors
  });
}


/**
 * Function to display the details of a selected email.
 * @param {number} email_id - The ID of the email to view.
 */
function view_email(email_id) {
  // Clear the email detail view and show a loading message while fetching data
  const emailDetailView = document.querySelector('#email-detail-view');
  emailDetailView.innerHTML = '<p>Loading email...</p>'; // Display a loading message

  // Show the email details view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'block';
  

  // Fetch the details of the selected email
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Format the email body with better separation for replies
      const formattedBody = formatEmailBody(email.body);

      // Display the email details with formatted body
      document.querySelector('#email-detail-view').innerHTML = `
        <div><strong>From:</strong> ${email.sender}</div>
        <div><strong>To:</strong> ${email.recipients.join(', ')}</div>
        <div><strong>Subject:</strong> ${email.subject}</div>
        <div class="email-timestamp"><strong>Timestamp:</strong> ${email.timestamp}</div>
        <div class="email-body">${formattedBody}</div>
        ${currentMailbox !== 'sent' ? `<button id="archive">${email.archived ? 'Unarchive' : 'Archive'}</button>` : ''}
        ${currentMailbox !== 'sent' ? `<button id="reply">Reply</button>` : ''}
      `;

      // Set up archive/unarchive functionality if the email is not from the Sent mailbox
      if (currentMailbox !== 'sent') {
        document.querySelector('#archive').addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: !email.archived
            })
          })
          .then(() => {
            // Reload the inbox to reflect changes
            select_tab('inbox'); // Visually focus the inbox tab
          });
        });

        // Set up reply functionality
        document.querySelector('#reply').addEventListener('click', () => {
          compose_email(email); // Populate the compose form with reply details
        });
      }

      // Mark the email as read upon viewing
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      });
    });
}

/**
 * Function to format the email body to make replies and original messages distinct.
 * @param {string} body - The email body to format.
 * @returns {string} - Formatted email body with separations and styles.
 */
function formatEmailBody(body) {
  // Replace common reply markers with styled blockquote elements for indentation
  return body.replace(
    /(On .* wrote:)/g,
    '<blockquote style="margin-top: 0px; margin: 5px 0; padding-left: 10px;"><strong>$1</strong>'
  ).replace(
    /(?:\r\n|\r|\n)/g,
    '<br>'
  ) + '</blockquote>';
}


