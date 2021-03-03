<?php	
	if (empty($_POST['name_21678']) && strlen($_POST['name_21678']) == 0 || empty($_POST['email_21678']) && strlen($_POST['email_21678']) == 0 || empty($_POST['email_21678']) && strlen($_POST['email_21678']) == 0 || empty($_POST['email_21678']) && strlen($_POST['email_21678']) == 0)
	{
		return false;
	}
	
	$name_21678 = $_POST['name_21678'];
	$email_21678 = $_POST['email_21678'];
	$email_21678 = $_POST['email_21678'];
	$email_21678 = $_POST['email_21678'];
	
	$to = 'receiver@yoursite.com'; // Email submissions are sent to this email

	// Create email	
	$email_subject = "Message from a Blocs website.";
	$email_body = "You have received a new message. \n\n".
				  "Name_21678: $name_21678 \nEmail_21678: $email_21678 \nEmail_21678: $email_21678 \nEmail_21678: $email_21678 \n";
	$headers = "MIME-Version: 1.0\r\nContent-type: text/plain; charset=UTF-8\r\n";	
	$headers .= "From: contact@yoursite.com\n";
	$headers .= "Reply-To: $email_21678";	
	
	mail($to,$email_subject,$email_body,$headers); // Post message
	return true;			
?>