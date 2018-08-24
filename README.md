spiderForLianJia
===
It is designed to crawl the data  from <a href="https://bj.lianjia.com">LianJia</a> in order to get the specific information of the housing estate in certain city

* Usage:
run main.py with command ``` python main.py ```,you can just adjust the city you want to get information from by modifying code in main.py line3. And you will get the data stored in the ```./doc/data.xlsx```.Please be sure you empty the file at first. And I used bj(北京) as an example.
* Structure:
  - \__pycache__
  - doc
    - error
      - errLink.txt  # links failed to crawl
      - error.txt  # links failed to crawl and corresponding error
    - link
      - bj.txt # links needed to crawl further
    - data.xlsx # the file to store the result of crawling
    - rethink.md
  - main.py # entry
  - spiderForLianJia.py # the class of spider
  - demo.py #just use it during the process of writing
