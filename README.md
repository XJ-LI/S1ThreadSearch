# S1ThreadSearch 

stage1st 根据关键词楼内搜索

I have no idea what Im doing......kinda works, barely......do whatever you want with it, and let me know if the code does not function properly.

## How To
run the following 
```
# python test.py
```
here the config.json file should include all necessary info needed for processing the request. 

*  **username** and **password** should be your own login credentials, needed to access some locked threads.
*  **page_number** is the desired stopping point, the code will filter through all posts frfom page 1 up to the given page number.
*  **keywords** contains a list of keywords that will be filtered through.
*  **target_url** is an indicator for the thread of interest,  found as part of the target link.
