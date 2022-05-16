

# Implementation of a key exchange protocol with an online trusted third-party
This is the implementation of a key exchange protocol with an online trusted third-party for the Cryptography class in Universidad del Norte first semester of 2022.

## Getting Started

These instructions will get the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this program you will need the latest version of python, you're also going to need to install PyCryptodome:
```
!pip install pycryptodome
```

## Manual

### Break down of the communication process

The process that a user P should follow to register with the TTP is as follows:
1.	Send the message idp  (identity of user P) to the TTP to indicate that the user is requesting to be registered.
2.	The TTP generates a random long term secret key
kP ←R (kenc,P , kmac,P ) ∈ Ke × Km
	and stores the pair (idp , kp) in a private table.
3.	Then, the TTP sends the message kp to P.

This process must be done by every user that wishes to communicate with other users through the TTP. After this point, if users P and Q wish to communicate with each other, they must complete the following steps:
1.	P computes rP: a nonce*
2.	Q computes rQ: a nonce*
3.	TTP checks if it has a secret key kP and kQ and aborts if not. Otherwise, computes:
 
![alt text](https://i.ibb.co/8dTghJs/imagen-2022-05-15-194356399.png "Formula")

4.	TTP sends (cQ , tQ) to Q and sends (cP , tP , idQ , rQ) to P.
5.	P and Q perform the following steps as X (self) and Y (other):
a) X verifies that tX is a valid MAC on the message (idY , rP , rQ, cX), and aborts if not.
b)	X decrypts the ciphertext cX and verifies that cX decrypts to a message k, which is a valid key from the space of keys, and aborts if not.
c)	X terminates successfully.
* Nonce: arbitrary random number that is used once in a cryptographic communication.

## Code
The code is brief and very well documented. Please feel free to ask any questions.

## Running the project

First run the trusted third party script (ttp.py) in one terminal window, then run the client script in two separate terminal windows.

A successful run should look like this:
![alt text](https://i.ibb.co/BBPc4DK/Whats-App-Image-2022-05-14-at-10-35-17-PM.jpg "Succesful test run")
```
$cd /../proyectlocation/
$python tty.py
```
```
$cd /../proyectlocation/
$python client.py
```


## Built With

* [Python](https://www.python.org) 
* [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/) 
* [Socket](https://docs.python.org/3/library/socket.html) 

## Contributing

Please read [Contributing.md](Contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Version 1.0

## Authors

* **Krissten J. Martínez F.** - fuenmayork@uninorte.edu.co
* **Carlos A. Venencia S.** - cvenencia@uninorte.edu.co
* **Daniel G. Marquez A.** - dgmarquez@uninorte.edu.co
