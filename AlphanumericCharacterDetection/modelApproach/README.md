<h1 align="center"> Alphanumeric character classification (Model - B)</h1>

### Over View :- 

    Alphanumeric character classification using easy-ocr.

### usage :-

#### Install virtual enviroment Using pip installation after creating the enviroment

```bash
pip install -r requirments\\requirements.txt
```
#### import the module in your code
```bash
import alphanum_B
```

#### download the model from :-
(https://drive.google.com/open?id=1ajONZOgiG9pEYsQ-eBmgkVbMDuHgPCaY)

### operation :-
<ol>
<li> apply east text-detection on th input frame.</li>
<li><ul><li>if a new character has been detected.
<ol>
		<li>capture the coordinates of the detected character</li>
		<li>add a new thread that will be assigned the duty of handling the text-recognition using easy ocr.</li>
		<li>create an array which contains many copies of the input frame but rotated in different angles.</li>
		<li>start the thread which will run text-recogntion using the array provided in the previous step.</li>
		<li>return that text has been detected and return its coordinates.</li>
</ol></li>
	<li>else
    <br>
		return the input frame and that no text has been detected.</li></ul></li>
<li>wait for all threads to finish and join them with the main thread.</li>
<li>return an array containing the objects detected and what is the character that this object represents.</li>
</ol>

### Limitations :-
#### Using multi-threading puts much work on the processor so a strong CPU + GPU is highly recommended

### Notes :-

#### Tried using multiple ocrs (tesseract , easy ocr ) but easy ocr proved its self to be the best offline free ocr

### what is next :-
<ul>
<li>over come false positives (EX: F is sometimes confused with K) by 2 techniques.
<ul>
<li>Add weights to characters in the frequency table to make upper case characters wait more than lower case characters.</li>
</ul>
</li>
<li>Testing the final code on a platform that has a graphical proccessing unit ( GPU ).</li>
</ul>


install torch :

conda install pytorch==1.2.0 torchvision==0.4.0 cpuonly -c pytorch