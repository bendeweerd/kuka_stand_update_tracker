# Stand Update Tracker

This is a small program to help track changes made to Kuka KMP rack models (stored in .xml format).

It takes 2 directories of stands as input & displays a list of all stands that were added, removed, or edited from the first directory to the second.

## Usage:

```python update_tracker.py -o {original_directory} -n {new_directory}```

## Example Output:
```
Stands Added:
        B01_PS19.xml
        B01_PS20.xml
        B01_PS42.xml
        B02_PS11.xml
        B03_PS02.xml
        B03_PS03.xml
        B04_PS106.xml
        B05_LS41.xml
No Stands Removed.
Stands Edited:
        B04_PS91.xml
                detectMaxDisL: 2040 => 2000
                reflectorDisL: 1275 => 1273
Comparison Complete.
```
***
Written by Ben DeWeerd