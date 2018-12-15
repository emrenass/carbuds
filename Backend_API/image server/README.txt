to be ran at a different server


/get_pfp : POST
  
request:
{
	"user_id" : int,
	"target_id": int,
  	"session_token" : string
}

resp:

session does not exist , string: SESSION DOES NOT EXIST

no image for the target_user exists, string: NONE

success, string: base64 encoded hex string

db connection problems, string: UNHANDLED ERROR AT GET_PFP


/set_pfp 

request:
{
  	"user_id" : int,
    	"bitmap" : base64 encoded hex string,
   	"session_token" : string
}

session does not exist , string: SESSION DOES NOT EXIST

success, string: 0

db connection problems, string: UNHANDLED ERROR AT GET_PFP
