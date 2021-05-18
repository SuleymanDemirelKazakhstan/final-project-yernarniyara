<?php	
	if (empty($_POST['name_22229']) && strlen($_POST['name_22229']) == 0 || empty($_POST['name_22229']) && strlen($_POST['name_22229']) == 0 || empty($_POST['email_22229']) && strlen($_POST['email_22229']) == 0 || empty($_POST['email_22229']) && strlen($_POST['email_22229']) == 0)
	{
		return false;
	}
	
	$name_22229 = $_POST['name_22229'];
	$name_22229 = $_POST['name_22229'];
	$email_22229 = $_POST['email_22229'];
	$email_22229 = $_POST['email_22229'];
	
	$to = 'receiver@yoursite.com'; // Email submissions are sent to this email

	// Create email	
	$email_subject = "Message from a Blocs website.";
	$email_body = "You have received a new message. \n\n".
				  "Name_22229: $name_22229 \nName_22229: $name_22229 \nEmail_22229: $email_22229 \nEmail_22229: $email_22229 \n";
	$headers = "MIME-Version: 1.0\r\nContent-type: text/plain; charset=UTF-8\r\n";	
	$headers .= "From: contact@yoursite.com\n";
	$headers .= "Reply-To: $email_22229";	
	
	mail($to,$email_subject,$email_body,$headers); // Post message
	return true;			
?>