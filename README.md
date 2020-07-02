# Python_MD25
Robot-Electronics sell a convenient and easy to live with motor driver, [the MD25](https://www.robot-electronics.co.uk/products/drive-systems/motor-boards/md25-12v-2-8a-dual-h-bridge.html). Python_MD25 provides a way to make use of this driver board from Python code.

## Usage
You'll need the smbus package installed.
Copy drive.py into your project directory and do something like the following:

```python
import drive

md = drive.md25()
md.drive(100,100) #drives both motors at speed 100 using the default mode
```

