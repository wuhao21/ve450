Thinking Algorithm
-------------
#How to Build Keras Environment
* You should have installed proper version of python
* Install pip using easy_install @$PYTHON_HOME/Scripts
	```bash
	sudo easy_install pip
	```
* Install numpy, scipy, theano and keras
	```bash
        sudo pip install numpy
        sudo pip install scipy
        sudo pip install theano
        sudo pip install keras
	```
* Change backend of Keras to theano
	```bash
	vim ~/.keras/keras.json
	#change "backend":"tensorflow" to "backend":"theano"	
	```
* Import keras in python to check

#Demo1
	Use 4-layer fully connected NN to recognize SIN, LINEAR, QUADRATIC signals. Signal fluctuation and lose are considered. 
