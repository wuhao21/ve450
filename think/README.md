<<<<<<< HEAD
=======
Thinking Algorithm
-------------
#How to Build Keras Environment
* You should have installed proper version of python
* Install pip using easy_install @$PYTHON_HOME/Scripts
```
sudo easy_install pip
```
* Install numpy, scipy, theano and keras
```
sudo pip install numpy
sudo pip install scipy
sudo pip install theano
sudo pip install keras
```
* Change backend of Keras to theano
```
vim ~/.keras/keras.json
#change "backend":"tensorflow" to "backend":"theano"	
```
* Import keras in python to check

#Demo
* Use 4-layer fully connected NN to recognize SIN, LINEAR, QUADRATIC, TRIANGLE signals. Signal fluctuation and lose are considered. 
```
python demo_train.py
```
* To adjust config, just open the demo_config.py and change corresponding parameters.
```
vim demo_config.py
```
#Benmark
* Refer to more details in nn_benchmark.py

>>>>>>> c2c0f1ffdf32293ba6b5f35726e7ea190655e6a0
