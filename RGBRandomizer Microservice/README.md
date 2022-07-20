Communication Contract for RGBRandomizer Microservice  
CS 361  
Christopher Felt  

-----------------------------------------------------
How to REQUEST data:
-----------------------------------------------------

The client will send a JSON file to the microservice using ZeroMQ on tcp://localhost:7077.
The JSON sent in the request must be a dictionary in the following format:
```
{
	"status":"run",
	"data":
	[
		{"r":40, "g":55, "b":70},
		{"r":40, "g":55, "b":70},
		{"r":33, "g":66, "b":120},
	]
}
```
Where the "status":"run" line tells the microservice to randomize the RGB combinations in the "data" section.


-----------------------------------------------------
How to RECEIVE data:
-----------------------------------------------------

The microservice will send a JSON to the client using ZeroMQ on the same port at tcp://localhost:7077.

The JSON sent in the response will be a dictionary in the following format:
```
{
	"status":"done",
	"data":
	[
		{"r":155, "g":0, "b":25},
		{"r":155, "g":0, "b":25},
		{"r":197, "g":235, "b":71},
	]
}
```
Where the "status":"done" line tells the client that the "data" section has been successfully randomized.


-----------------------------------------------------
UML Sequence Diagram:
-----------------------------------------------------

![UML sketch](https://user-images.githubusercontent.com/54368648/180090719-173436d9-339d-4f3b-994a-6eab797890fb.png)
