to be run at a different server


/get_pfp
  
request:
{
	"user_id" : int,
	"target_id": int
  	"session_token" : string
}



/set_pfp 

request:
{
  	"user_id" : int,
    	"bitmap" : base64 encoded hex string,
   	"session_token" : string
}
